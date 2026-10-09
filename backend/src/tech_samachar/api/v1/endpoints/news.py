from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from tech_samachar.api.deps import get_db
from tech_samachar.services.news_service import NewsService
from tech_samachar.schemas.article import ArticleResponse
from tech_samachar.schemas.common import PaginatedResponse, Pagination

router = APIRouter()

@router.get("", response_model=PaginatedResponse[ArticleResponse])
def get_news(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    topic: Optional[int] = Query(None),
    source: Optional[int] = Query(None),
    sort: str = Query("published_time"),
    db: Session = Depends(get_db)
):
    service = NewsService(db)
    items, total = service.get_articles(page, page_size, topic, source, sort=sort)
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

@router.get("/latest", response_model=List[ArticleResponse])
def get_latest_news(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    service = NewsService(db)
    return service.get_latest_articles(limit)

@router.get("/featured", response_model=List[ArticleResponse])
def get_featured_news(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    service = NewsService(db)
    return service.get_featured_articles(limit)

@router.get("/{article_id}", response_model=ArticleResponse)
def get_article(article_id: int, db: Session = Depends(get_db)):
    service = NewsService(db)
    article = service.get_article(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article
