from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from tech_samachar.api.deps import get_db

router = APIRouter()

@router.get("")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "error"

    return {
        "status": "ok", 
        "database": db_status,
        "message": "Tech Samachar Backend is running"
    }
