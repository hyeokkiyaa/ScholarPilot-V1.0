from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Union
from datetime import datetime

# Result Schemas
class ResultBase(BaseModel):
    column_id: str
    value: Optional[Union[str, List[Any], Dict[str, Any]]] = None # Value can be parsed JSON
    status: str = "pending"
    error_message: Optional[str] = None

class ResultResponse(ResultBase):
    id: str
    paper_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Paper Schemas
class PaperBase(BaseModel):
    title: Optional[str] = None
    source_url: Optional[str] = None
    source_type: Optional[str] = None

class PaperCreate(BaseModel):
    input_value: Optional[str] = None # URL, Title, DOI, empty if file upload
    
class PaperUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None

class PaperResponse(PaperBase):
    id: str
    project_id: str
    status: str
    pdf_path: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    # We might want to include results or fetch them separately. 
    # For list views, having a dictionary of results is useful.
    results: Dict[str, ResultResponse] = {} 

    class Config:
        from_attributes = True
