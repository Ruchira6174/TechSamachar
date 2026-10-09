from sqlalchemy.orm import Session
from tech_samachar.db.models.article import Article
from typing import Dict, Any

class Deduplicator:
    @staticmethod
    def is_duplicate(db: Session, article_data: Dict[str, Any]) -> bool:
        """
        Checks if an article is a duplicate based on canonical URL or content hash.
        """
        url = article_data.get("canonical_url")
        content_hash = article_data.get("content_hash")
        
        if not url:
            return True # Cannot process without URL
            
        # Check URL
        exists_url = db.query(Article).filter(Article.canonical_url == url).first()
        if exists_url:
            return True
            
        # Check hash
        exists_hash = db.query(Article).filter(Article.content_hash == content_hash).first()
        if exists_hash:
            return True
            
        return False
