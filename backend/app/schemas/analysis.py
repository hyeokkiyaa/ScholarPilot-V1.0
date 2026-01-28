from pydantic import BaseModel
from typing import Optional, List

class AnalysisRequest(BaseModel):
    project_id: Optional[str] = None
    paper_ids: Optional[List[str]] = None
    column_ids: Optional[List[str]] = None # If null, analyze all columns

class RetryRequest(BaseModel):
    pass
