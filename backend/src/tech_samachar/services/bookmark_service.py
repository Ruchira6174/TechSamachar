from typing import List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from tech_samachar.db.models.preference import Bookmark
from tech_samachar.db.models.article import Article

class BookmarkService:
    def __init__(self, db: Session):
        self.db = db

    def get_bookmarks(self, user_id: int = 1) -> List[Bookmark]:
        return self.db.query(Bookmark)\
            .options(joinedload(Bookmark.article).joinedload(Article.source))\
            .filter(Bookmark.user_id == user_id)\
            .order_by(Bookmark.created_at.desc()).all()

    def add_bookmark(self, article_id: int, user_id: int = 1) -> Bookmark:
        b = self.db.query(Bookmark).filter(Bookmark.user_id == user_id, Bookmark.article_id == article_id).first()
        if b:
            return b
            
        try:
            b = Bookmark(user_id=user_id, article_id=article_id)
            self.db.add(b)
            self.db.commit()
            return b
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Invalid article ID")

    def delete_bookmark(self, article_id: int, user_id: int = 1):
        b = self.db.query(Bookmark).filter(Bookmark.user_id == user_id, Bookmark.article_id == article_id).first()
        if b:
            self.db.delete(b)
            self.db.commit()
