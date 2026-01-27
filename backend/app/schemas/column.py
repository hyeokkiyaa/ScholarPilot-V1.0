from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ColumnBase(BaseModel):
    name: str
    tool_name: str
    custom_prompt: Optional[str] = None
    order_index: int = 0

class ColumnCreate(ColumnBase):
    pass

class ColumnUpdate(BaseModel):
    name: Optional[str] = None
    custom_prompt: Optional[str] = None
    order_index: Optional[int] = None

class ColumnResponse(ColumnBase):
    id: str
    project_id: str
    created_at: datetime

    class Config:
        from_attributes = True
