from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional
from tech_samachar.api.deps import get_db
from tech_samachar.services.briefing_service import BriefingService
from tech_samachar.schemas.briefing import BriefingResponse

router = APIRouter()

@router.get("", response_model=BriefingResponse)
def get_latest_briefing(db: Session = Depends(get_db)):
    service = BriefingService(db)
    briefing = service.get_latest_briefing()
    if not briefing:
        raise HTTPException(status_code=404, detail="No briefings available")
    return briefing

@router.get("/{briefing_date}", response_model=BriefingResponse)
def get_briefing_by_date(briefing_date: date, db: Session = Depends(get_db)):
    service = BriefingService(db)
    briefing = service.get_briefing_by_date(briefing_date)
    if not briefing:
        raise HTTPException(status_code=404, detail="Briefing not found for date")
    return briefing

@router.post("/generate", response_model=BriefingResponse)
def generate_briefing(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # In a real app this would be protected by admin auth
    service = BriefingService(db)
    briefing = service.generate_briefing()
    if not briefing:
        raise HTTPException(status_code=400, detail="Could not generate briefing (maybe no articles?)")
    return briefing
