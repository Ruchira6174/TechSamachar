import logging
from sqlalchemy.orm import Session
from tech_samachar.db.models.article import Article, ArticleSummary
from tech_samachar.ai.provider_factory import get_ai_provider
from tech_samachar.config import settings

logger = logging.getLogger(__name__)

class SummarizerService:
    def __init__(self, db: Session):
        self.db = db
        self.provider = get_ai_provider()
        
    def summarize_article(self, article: Article):
        if article.summary:
            return # Already summarized
            
        try:
            summary_text = self.provider.generate_summary(article.title, article.description or "")
            if summary_text:
                summary = ArticleSummary(
                    article_id=article.id,
                    summary_text=summary_text,
                    provider=settings.AI_PROVIDER,
                    model_name="default"
                )
                self.db.add(summary)
                self.db.commit()
        except Exception as e:
            logger.error(f"Summarization failed for article {article.id}: {e}")
            self.db.rollback()
