from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.schemas.column import ColumnResponse

class ProjectBase(BaseModel):
    name: str
    template: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    template: Optional[str] = None

class ProjectResponse(ProjectBase):
    id: str
    created_at: datetime
    updated_at: datetime
    # paper_count and status_summary will be computed fields or separate queries usually
    paper_count: Optional[int] = 0
    
    class Config:
        from_attributes = True

class ProjectDetailResponse(ProjectResponse):
    columns: List[ColumnResponse] = []
