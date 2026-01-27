from fastapi import APIRouter, Depends, BackgroundTasks
from app.schemas.analysis import AnalysisRequest

router = APIRouter()

@router.post("/analyze")
async def trigger_analysis(request: AnalysisRequest, background_tasks: BackgroundTasks):
    # This will be the entry point for bulk analysis
    # For now just return accepted
    return {"status": "accepted", "message": f"Analysis queued for {len(request.paper_ids)} papers"}
