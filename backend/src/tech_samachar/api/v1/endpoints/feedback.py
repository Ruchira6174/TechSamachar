from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from tech_samachar.api.deps import get_db
from tech_samachar.services.feedback_service import FeedbackService
from tech_samachar.schemas.preference import FeedbackBase, FeedbackResponse

router = APIRouter()

@router.post("", response_model=FeedbackResponse)
def submit_feedback(data: FeedbackBase, db: Session = Depends(get_db)):
    service = FeedbackService(db)
    try:
        return service.add_feedback(data.article_id, data.feedback_type, user_id=1)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
