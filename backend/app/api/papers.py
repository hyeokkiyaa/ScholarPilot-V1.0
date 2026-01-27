from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.paper import Paper
from app.models.project import Project
from app.schemas.paper import PaperCreate, PaperUpdate, PaperResponse
# from app.agents.input_router import InputRouterAgent # Phase 2

router = APIRouter()

@router.get("/projects/{project_id}/papers", response_model=List[PaperResponse])
def list_papers(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project.papers

@router.post("/projects/{project_id}/papers", response_model=PaperResponse)
async def create_paper(
    project_id: str, 
    paper_in: PaperCreate = None, 
    file: UploadFile = File(None), 
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Validation
    if not file and (not paper_in or not paper_in.input_value):
         raise HTTPException(status_code=400, detail="Either file or input_value must be provided")

    # Basic creation logic for now
    db_paper = Paper(project_id=project_id, status="queued")
    
    if file:
        # Save file (Phase 2 implementation details)
        # For now just set name
        db_paper.title = file.filename
        db_paper.source_type = "pdf"
        # In real impl, we'd save to disk and set pdf_path
    elif paper_in:
        db_paper.source_url = paper_in.input_value
        db_paper.source_type = "url" # or detect type logic
        db_paper.title = paper_in.input_value # Temporary
        
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    
    # Trigger analysis task here (background task)
    
    return db_paper

@router.get("/papers/{id}", response_model=PaperResponse)
def get_paper(id: str, db: Session = Depends(get_db)):
    paper = db.query(Paper).filter(Paper.id == id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    return paper

@router.put("/papers/{id}", response_model=PaperResponse)
def update_paper(id: str, paper_update: PaperUpdate, db: Session = Depends(get_db)):
    paper = db.query(Paper).filter(Paper.id == id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    update_data = paper_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(paper, key, value)
    
    db.commit()
    db.refresh(paper)
    return paper

@router.delete("/papers/{id}")
def delete_paper(id: str, db: Session = Depends(get_db)):
    paper = db.query(Paper).filter(Paper.id == id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    db.delete(paper)
    db.commit()
    return {"status": "success"}

@router.post("/papers/{id}/retry")
def retry_paper(id: str, db: Session = Depends(get_db)):
    paper = db.query(Paper).filter(Paper.id == id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    paper.status = "queued"
    paper.error_message = None
    db.commit()
    
    # Trigger analysis again
    
    return {"status": "queued"}
