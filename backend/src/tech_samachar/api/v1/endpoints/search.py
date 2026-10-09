from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from tech_samachar.api.deps import get_db
from tech_samachar.services.news_service import NewsService
from tech_samachar.schemas.article import ArticleResponse
from tech_samachar.schemas.common import PaginatedResponse, Pagination

router = APIRouter()

@router.get("", response_model=PaginatedResponse[ArticleResponse])
def search_news(
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    service = NewsService(db)
    items, total = service.get_articles(page, page_size, search=q)
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
