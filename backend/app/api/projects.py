from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.project import Project
from app.models.column import ColumnDef
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectDetailResponse
from app.schemas.column import ColumnResponse

router = APIRouter()

@router.get("/", response_model=List[ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()

@router.get("/templates")
def list_templates():
    from app.tools.registry import PROJECT_TEMPLATES
    return [
        {"id": key, "name": val["name"], "description": val["description"]}
        for key, val in PROJECT_TEMPLATES.items()
    ]

@router.post("/", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    db_project = Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    # Create default columns based on template
    from app.tools.registry import PROJECT_TEMPLATES, TOOL_INFO
    
    template_id = project.template or "basic"
    template = PROJECT_TEMPLATES.get(template_id)
    
    if template:
        for index, tool_name in enumerate(template["columns"]):
            tool_info = TOOL_INFO.get(tool_name)
            if tool_info:
                col = ColumnDef(
                    project_id=db_project.id,
                    name=tool_info["name"],
                    tool_name=tool_name,
                    order_index=index
                )
                db.add(col)
        db.commit()
        db.refresh(db_project)
    
    return db_project

@router.get("/{id}", response_model=ProjectDetailResponse)
def get_project(id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{id}", response_model=ProjectResponse)
def update_project(id: str, project_update: ProjectUpdate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    update_data = project_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)
    
    db.commit()
    db.refresh(project)
    return project

@router.delete("/{id}")
def delete_project(id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(project)
    db.commit()
    return {"status": "success"}

# Sub-resources (Columns) usually go here or in a separate file if complex
# The requirement says /api/projects/{id}/columns
@router.get("/{id}/columns", response_model=List[ColumnResponse])
def get_project_columns(id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project.columns
