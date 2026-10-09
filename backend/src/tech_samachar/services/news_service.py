from typing import List, Tuple, Optional
from sqlalchemy.orm import Session
from tech_samachar.repositories.article_repository import ArticleRepository
from tech_samachar.db.models.article import Article
from tech_samachar.services.ranking_service import RankingService

class NewsService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ArticleRepository(db)
        self.ranking = RankingService(db)

    def get_articles(
        self, page: int = 1, page_size: int = 20, topic_id: Optional[int] = None, 
        source_id: Optional[int] = None, search: Optional[str] = None, sort: str = "published_time"
    ) -> Tuple[List[Article], int]:
        
        # Max page size to avoid massive DB load
        if page_size > 100:
            page_size = 100
        
        skip = (page - 1) * page_size
        items, total = self.repo.get_articles(skip, page_size, topic_id, source_id, search, sort)
        
        # Apply ranking if requested
        if sort == "relevance" and not search:
            items = self.ranking.rank_articles(items)
            
        return items, total

    def get_article(self, article_id: int) -> Optional[Article]:
        return self.repo.get_article_by_id(article_id)

    def get_featured_articles(self, limit: int = 5) -> List[Article]:
        return self.repo.get_featured_articles(limit)

    def get_latest_articles(self, limit: int = 10) -> List[Article]:
        items, _ = self.repo.get_articles(skip=0, limit=limit, sort_by="published_time")
        return items
