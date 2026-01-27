from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List, Dict
from app.database import get_db
from app.models.column import ColumnDef
from app.models.project import Project
from app.schemas.column import ColumnCreate, ColumnUpdate, ColumnResponse

router = APIRouter()

# Creates are often nested under projects
@router.post("/projects/{project_id}/columns", response_model=ColumnResponse)
def create_column(project_id: str, column: ColumnCreate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db_column = ColumnDef(project_id=project_id, **column.model_dump())
    
    # Auto-assign order_index if not provided or 0? 
    # Usually we want to append.
    if db_column.order_index == 0:
        count = db.query(ColumnDef).filter(ColumnDef.project_id == project_id).count()
        db_column.order_index = count
        
    db.add(db_column)
    db.commit()
    db.refresh(db_column)
    return db_column

@router.put("/columns/{id}", response_model=ColumnResponse)
def update_column(id: str, column_update: ColumnUpdate, db: Session = Depends(get_db)):
    column = db.query(ColumnDef).filter(ColumnDef.id == id).first()
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")
    
    update_data = column_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(column, key, value)
    
    db.commit()
    db.refresh(column)
    return column

@router.delete("/columns/{id}")
def delete_column(id: str, db: Session = Depends(get_db)):
    column = db.query(ColumnDef).filter(ColumnDef.id == id).first()
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")
    
    db.delete(column)
    db.commit()
    return {"status": "success"}

@router.post("/columns/reorder")
def reorder_columns(orders: Dict[str, int] = Body(...), db: Session = Depends(get_db)):
    # orders is {column_id: new_index}
    for col_id, new_index in orders.items():
        column = db.query(ColumnDef).filter(ColumnDef.id == col_id).first()
        if column:
            column.order_index = new_index
    db.commit()
    return {"status": "success"}
