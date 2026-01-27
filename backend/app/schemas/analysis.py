from pydantic import BaseModel
from typing import Optional, List

class AnalysisRequest(BaseModel):
    paper_ids: List[str]
    column_ids: Optional[List[str]] = None # If null, analyze all columns

class RetryRequest(BaseModel):
    pass
