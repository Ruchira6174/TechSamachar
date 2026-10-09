from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
from tech_samachar.api.deps import get_db
from tech_samachar.repositories.topic_repository import TopicRepository
from tech_samachar.services.news_service import NewsService
from tech_samachar.schemas.topic import TopicResponse
from tech_samachar.schemas.article import ArticleResponse
from tech_samachar.schemas.common import PaginatedResponse, Pagination

router = APIRouter()

@router.get("", response_model=List[TopicResponse])
def get_topics(db: Session = Depends(get_db)):
    repo = TopicRepository(db)
    return repo.get_all_topics()

@router.get("/{slug}/news", response_model=PaginatedResponse[ArticleResponse])
def get_topic_news(
    slug: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    repo = TopicRepository(db)
    topic = repo.get_topic_by_slug(slug)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
        
    service = NewsService(db)
    items, total = service.get_articles(page, page_size, topic_id=topic.id)
    total_pages = (total + page_size - 1) // page_size
    
    return PaginatedResponse(
        items=items,
        pagination=Pagination(
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    )
