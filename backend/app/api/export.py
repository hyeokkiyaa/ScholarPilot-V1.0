from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.post("/projects/{id}/export/excel")
def export_excel(id: str, db: Session = Depends(get_db)):
    # Placeholder
    return {"status": "not_implemented"}

@router.post("/projects/{id}/export/csv")
def export_csv(id: str, db: Session = Depends(get_db)):
    # Placeholder
    return {"status": "not_implemented"}

@router.post("/projects/{id}/export/markdown")
def export_markdown(id: str, db: Session = Depends(get_db)):
    # Placeholder
    return {"status": "not_implemented"}

@router.post("/projects/{id}/export/notion")
def export_notion(id: str, db: Session = Depends(get_db)):
    # Placeholder
    return {"status": "not_implemented"}
