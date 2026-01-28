from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any
from app.database import get_db
from app.models.settings import Settings
from app.schemas.settings import SettingsUpdate, SettingsResponse
# We will need the adapter factory for test-connection, but that's in Phase 2.
# For now we'll just stub it or implement basic saving.

router = APIRouter()

@router.get("/", response_model=List[SettingsResponse])
def get_settings(db: Session = Depends(get_db)):
    return db.query(Settings).all()

@router.put("/", response_model=List[SettingsResponse])
def update_settings(settings_update: SettingsUpdate, db: Session = Depends(get_db)):
    updated = []
    for item in settings_update.settings:
        key = item['key']
        value = item['value']
        
        setting = db.query(Settings).filter(Settings.key == key).first()
        if setting:
            setting.value = value
        else:
            setting = Settings(key=key, value=value)
            db.add(setting)
        updated.append(setting)
    
    db.commit()
    return updated

from pydantic import BaseModel
from app.adapters.model_adapter import get_model_adapter

class TestLLMRequest(BaseModel):
    provider: str
    api_key: str

@router.post("/test-llm")
async def test_llm_connection(request: TestLLMRequest):
    try:
        adapter = get_model_adapter(request.provider, request.api_key)
        success = await adapter.test_connection()
        if success:
            return {"status": "ok", "message": f"Successfully connected to {request.provider}"}
        else:
             raise HTTPException(status_code=400, detail=f"Failed to connect to {request.provider}")
    except ValueError as e:
         raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"Connection error: {str(e)}")

@router.post("/test-connection")
async def test_connection():
    # Placeholder until adapters are implemented
    return {"status": "ok", "message": "Connection test not implemented yet"}
