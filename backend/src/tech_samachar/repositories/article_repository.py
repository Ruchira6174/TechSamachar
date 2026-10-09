from typing import List, Tuple, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, or_, text
from tech_samachar.db.models.article import Article, Topic, ArticleSummary
from tech_samachar.db.models.source import Source
from sqlalchemy.sql import func

class ArticleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_article_by_id(self, article_id: int) -> Optional[Article]:
        return self.db.query(Article)\
            .options(joinedload(Article.source), joinedload(Article.topics), joinedload(Article.summary))\
            .filter(Article.id == article_id).first()

    def get_articles(
        self, skip: int = 0, limit: int = 20, topic_id: Optional[int] = None, 
        source_id: Optional[int] = None, search_query: Optional[str] = None, sort_by: str = "published_time"
    ) -> Tuple[List[Article], int]:
        
        query = self.db.query(Article).options(
            joinedload(Article.source), 
            joinedload(Article.topics), 
            joinedload(Article.summary)
        )
        
        if topic_id:
            query = query.filter(Article.topics.any(id=topic_id))
            
        if source_id:
            query = query.filter(Article.source_id == source_id)
            
        if search_query:
            search_term = f"%{search_query}%"
            query = query.filter(or_(
                Article.title.ilike(search_term),
                Article.description.ilike(search_term)
            ))
            
        # Sorting
        if sort_by == "published_time":
            query = query.order_by(desc(Article.published_time))
        elif sort_by == "created_at":
            query = query.order_by(desc(Article.created_at))
        else:
            query = query.order_by(desc(Article.published_time))

        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total

    def get_featured_articles(self, limit: int = 5) -> List[Article]:
        # Simple placeholder for featured logic
        return self.db.query(Article)\
            .options(joinedload(Article.source), joinedload(Article.topics), joinedload(Article.summary))\
            .order_by(desc(Article.published_time)).limit(limit).all()
