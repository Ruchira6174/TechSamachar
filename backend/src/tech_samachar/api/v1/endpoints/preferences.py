from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from tech_samachar.api.deps import get_db
from tech_samachar.services.preference_service import PreferenceService
from tech_samachar.schemas.preference import PreferenceResponse, PreferenceBase

router = APIRouter()

@router.get("", response_model=PreferenceResponse)
def get_preferences(db: Session = Depends(get_db)):
    service = PreferenceService(db)
    return service.get_preferences(user_id=1)

@router.put("", response_model=PreferenceResponse)
def update_preferences(data: PreferenceBase, db: Session = Depends(get_db)):
    service = PreferenceService(db)
    return service.update_preferences(data, user_id=1)
