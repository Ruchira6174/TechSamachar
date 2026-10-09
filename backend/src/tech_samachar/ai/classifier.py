import logging
from sqlalchemy.orm import Session
from tech_samachar.db.models.article import Article, Topic, article_topic_association
from tech_samachar.ai.provider_factory import get_ai_provider

logger = logging.getLogger(__name__)

class ClassifierService:
    def __init__(self, db: Session):
        self.db = db
        self.provider = get_ai_provider()
        
    def classify_article(self, article: Article):
        if article.topics:
            return # Already classified
            
        topics = self.db.query(Topic).all()
        topics_data = [{"id": t.id, "name": t.name} for t in topics]
        
        try:
            classifications = self.provider.classify_topics(
                article.title, 
                article.description or "", 
                topics_data
            )
            
            for c in classifications:
                topic = self.db.query(Topic).filter(Topic.id == c["topic_id"]).first()
                if topic:
                    # In a real setup, we would insert into the association table with confidence
                    article.topics.append(topic)
                    
            self.db.commit()
        except Exception as e:
            logger.error(f"Classification failed for article {article.id}: {e}")
            self.db.rollback()
