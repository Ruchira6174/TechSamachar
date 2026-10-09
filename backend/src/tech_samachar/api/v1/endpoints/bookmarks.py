from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from tech_samachar.api.deps import get_db
from tech_samachar.services.bookmark_service import BookmarkService
from tech_samachar.schemas.preference import BookmarkResponse

router = APIRouter()

@router.get("", response_model=List[BookmarkResponse])
def get_bookmarks(db: Session = Depends(get_db)):
    service = BookmarkService(db)
    return service.get_bookmarks(user_id=1)

@router.post("/{article_id}", response_model=BookmarkResponse)
def add_bookmark(article_id: int, db: Session = Depends(get_db)):
    service = BookmarkService(db)
    try:
        return service.add_bookmark(article_id, user_id=1)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{article_id}", status_code=204)
def remove_bookmark(article_id: int, db: Session = Depends(get_db)):
    service = BookmarkService(db)
    service.delete_bookmark(article_id, user_id=1)
    return None
