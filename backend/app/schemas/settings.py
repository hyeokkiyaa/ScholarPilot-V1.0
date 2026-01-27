from pydantic import BaseModel
from typing import Optional, List

class SettingsUpdate(BaseModel):
    settings: List[dict] # List of {key: str, value: str} or similar structure
    
class SettingsResponse(BaseModel):
    key: str
    value: Optional[str] = None

    class Config:
        from_attributes = True
