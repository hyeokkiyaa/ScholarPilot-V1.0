from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal
from app.schemas.analysis import AnalysisRequest
from app.models.project import Project
from app.models.paper import Paper
from app.models.settings import Settings
from app.models.result import Result
from app.models.column import ColumnDef
from app.agents.orchestrator import OrchestratorAgent
from app.adapters.model_adapter import get_model_adapter
import logging
import json
from typing import List

router = APIRouter()
logger = logging.getLogger(__name__)

async def process_paper_task(paper_id: str, project_id: str):
    """
    Background task to process a single paper.
    Creates its own DB session.
    """
    db = SessionLocal()
    try:
        # 1. Fetch Paper
        paper = db.query(Paper).filter(Paper.id == paper_id).first()
        if not paper:
            logger.error(f"Paper {paper_id} not found during processing")
            return
            
        # Update status to processing
        paper.status = "processing"
        paper.error_message = None
        db.commit()
        
        # 2. Setup Agent
        # Fetch settings to get API Key
        # Settings are stored as key/value rows.
        # We need to query for 'model_provider' and 'api_key'
        model_provider_setting = db.query(Settings).filter(Settings.key == 'model_provider').first()
        api_key_setting = db.query(Settings).filter(Settings.key == 'api_key').first()
        
        provider = model_provider_setting.value if model_provider_setting else 'claude'
        api_key = api_key_setting.value if api_key_setting else ''
        
        if not api_key:
            raise ValueError("API Key not found in settings. Please configure settings first.")

        # Initialize Adapter and Agent
        adapter = get_model_adapter(provider, api_key)
        agent = OrchestratorAgent(adapter)
        
        # 3. Fetch Columns (Schema)
        columns = db.query(ColumnDef).filter(ColumnDef.project_id == project_id).all()
        if not columns:
             logger.warning(f"No columns defined for project {project_id}")
             # Nothing to do, but mark done?
             paper.status = "done"
             db.commit()
             return

        # 4. Run Analysis
        # Ensure raw_content exists
        if not paper.raw_content:
             raise ValueError("Paper has no content to analyze. Please re-upload the PDF.")

        # Agent returns Dict[column_id, dict(status, value, error)]
        results_map = await agent.analyze_paper(paper.raw_content, columns)
        
        # 5. Save Results
        for col_id, res_data in results_map.items():
            # Check if result exists
            existing_result = db.query(Result).filter(
                Result.paper_id == paper.id, 
                Result.column_id == col_id
            ).first()
            
            value = res_data['value']
            if value is None:
                value_str = None
            elif isinstance(value, (dict, list)):
                value_str = json.dumps(value)
            else:
                value_str = str(value)
            
            if existing_result:
                existing_result.value = value_str
                existing_result.status = res_data['status']
                existing_result.error_message = res_data['error_message']
            else:
                new_result = Result(
                    paper_id=paper.id,
                    column_id=col_id,
                    value=value_str,
                    status=res_data['status'],
                    error_message=res_data['error_message']
                )
                db.add(new_result)
        
        # 6. Final Status Update
        # If any column failed, we might mark paper as partial error?
        # Current logic: 'done' if process finished, even if individual cols failed.
        paper.status = "done"
        db.commit()
        
    except Exception as e:
        logger.error(f"Error processing paper {paper_id}: {e}")
        # Re-fetch paper in case session detached (though we re-use 'paper' obj attached to 'db')
        # If transaction failed, rollback and start fresh for error update
        db.rollback()
        paper = db.query(Paper).filter(Paper.id == paper_id).first()
        if paper:
            paper.status = "error"
            paper.error_message = str(e)
            db.commit()
            
    finally:
        db.close()


@router.post("/analyze")
async def trigger_analysis(
    request: AnalysisRequest, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    project_id = request.project_id
    
    # 1. Determine papers to analyze
    target_papers = []
    
    if project_id:
        # Fetch all QUEUED (or error/processing?) papers for project
        # Usually we only pick 'queued'. If user wants retry, they can manually reset to queued.
        # But 'Run Analysis' implies running pending work.
        target_papers = db.query(Paper).filter(
            Paper.project_id == project_id,
            Paper.status == 'queued'
        ).all()
        
    elif request.paper_ids:
        target_papers = db.query(Paper).filter(Paper.id.in_(request.paper_ids)).all()
        project_id = target_papers[0].project_id if target_papers else None 
        # Note: if mixed projects, we assume same project context or handle per paper.
        # But for 'process_paper_task', we pass project_id.
    
    if not target_papers:
        return {"status": "ignored", "message": "No queued papers found to analyze."}

    # 2. Queue Background Tasks
    count = 0
    for paper in target_papers:
        # We pass paper.id and paper.project_id
        # Note: paper object might be detached if we don't use IDs
        background_tasks.add_task(process_paper_task, paper.id, paper.project_id)
        count += 1
        
    return {"status": "accepted", "message": f"Analysis started for {count} papers"}
