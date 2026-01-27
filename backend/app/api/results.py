from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List, Any
from app.database import get_db
from app.models.result import Result
from app.models.paper import Paper
from app.schemas.paper import ResultResponse
# from app.schemas.result import ResultUpdate # Create if needed

router = APIRouter()

@router.get("/papers/{id}/results", response_model=List[ResultResponse])
def get_paper_results(id: str, db: Session = Depends(get_db)):
    # Verify paper exists first?
    return db.query(Result).filter(Result.paper_id == id).all()

@router.put("/results/{id}", response_model=ResultResponse)
def update_result(id: str, value: Any = Body(..., embed=True), db: Session = Depends(get_db)):
    result = db.query(Result).filter(Result.id == id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    
    # Store as string (json dump if complex)
    import json
    if isinstance(value, (dict, list)):
        result.value = json.dumps(value)
    else:
        result.value = str(value)
        
    db.commit()
    db.refresh(result)
    return result

@router.post("/results/{id}/retry")
def retry_result(id: str, db: Session = Depends(get_db)):
    result = db.query(Result).filter(Result.id == id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    
    result.status = "pending"
    result.error_message = None
    db.commit()
    
    # Trigger single column analysis
    
    return {"status": "pending"}
