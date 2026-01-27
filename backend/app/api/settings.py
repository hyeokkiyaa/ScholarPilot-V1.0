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

@router.post("/test-connection")
async def test_connection():
    # Placeholder until adapters are implemented
    return {"status": "ok", "message": "Connection test not implemented yet"}
