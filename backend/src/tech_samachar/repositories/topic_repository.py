from typing import List, Optional
from sqlalchemy.orm import Session
from tech_samachar.db.models.article import Topic

class TopicRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_topics(self) -> List[Topic]:
        return self.db.query(Topic).order_by(Topic.default_priority.desc(), Topic.name).all()

    def get_topic_by_slug(self, slug: str) -> Optional[Topic]:
        return self.db.query(Topic).filter(Topic.slug == slug).first()
