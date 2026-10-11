
from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from tech_samachar.db.models.article import Article
from tech_samachar.db.models.preference import Bookmark


class BookmarkService:
    def __init__(self, db: Session):
        self.db = db

    def get_bookmarks(self, user_id: int = 1) -> List[Bookmark]:
        return (
            self.db.query(Bookmark)
            .options(joinedload(Bookmark.article).joinedload(Article.source))
            .filter(Bookmark.user_id == user_id)
            .order_by(Bookmark.created_at.desc())
            .all()
        )

    def add_bookmark(self, article_id: int, user_id: int = 1) -> Bookmark:
        # Validate the article before creating the bookmark.
        article = (
            self.db.query(Article)
            .filter(Article.id == article_id)
            .first()
        )

        if article is None:
            raise ValueError("Invalid article ID")

        existing = (
            self.db.query(Bookmark)
            .filter(
                Bookmark.user_id == user_id,
                Bookmark.article_id == article_id,
            )
            .first()
        )

        if existing:
            return existing

        try:
            bookmark = Bookmark(
                user_id=user_id,
                article_id=article_id,
            )
            self.db.add(bookmark)
            self.db.commit()
            self.db.refresh(bookmark)
            return bookmark
        except IntegrityError as exc:
            self.db.rollback()
            raise ValueError("Unable to create bookmark") from exc

    def delete_bookmark(self, article_id: int, user_id: int = 1):
        bookmark = (
            self.db.query(Bookmark)
            .filter(
                Bookmark.user_id == user_id,
                Bookmark.article_id == article_id,
            )
            .first()
        )

        if bookmark:
            self.db.delete(bookmark)
            self.db.commit()