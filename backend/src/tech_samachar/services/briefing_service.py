import logging
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from datetime import date, datetime, timedelta, timezone
from typing import Optional, List
from tech_samachar.db.models.briefing import Briefing, BriefingArticle
from tech_samachar.db.models.article import Article
from tech_samachar.services.ranking_service import RankingService
from tech_samachar.ai.provider_factory import get_ai_provider

logger = logging.getLogger(__name__)

class BriefingService:
    def __init__(self, db: Session):
        self.db = db
        self.ranking = RankingService(db)
        self.ai = get_ai_provider()

    def get_latest_briefing(self) -> Optional[Briefing]:
        return self.db.query(Briefing)\
            .options(joinedload(Briefing.articles).joinedload(BriefingArticle.article).joinedload(Article.source))\
            .order_by(Briefing.briefing_date.desc()).first()

    def get_briefing_by_date(self, target_date: date) -> Optional[Briefing]:
        return self.db.query(Briefing)\
            .options(joinedload(Briefing.articles).joinedload(BriefingArticle.article).joinedload(Article.source))\
            .filter(Briefing.briefing_date == target_date).first()

    def generate_briefing(self, target_date: date = None) -> Optional[Briefing]:
        if target_date is None:
            target_date = date.today()
            
        # Check if already generated
        existing = self.db.query(Briefing).filter(Briefing.briefing_date == target_date).first()
        if existing:
            return existing

        # Get top articles from the last 24-48 hours
        start_time = datetime.combine(target_date - timedelta(days=1), datetime.min.time(), tzinfo=timezone.utc)
        
        recent_articles = self.db.query(Article).filter(Article.published_time >= start_time).all()
        if not recent_articles:
            logger.warning(f"No articles found for briefing on {target_date}")
            return None
            
        # Rank them
        ranked_articles = self.ranking.rank_articles(recent_articles)
        top_articles = ranked_articles[:10] # Top 10 for briefing
        
        if not top_articles:
            return None
            
        # Generate summary
        titles = [a.title for a in top_articles]
        prompt_content = "Today's top stories are: " + ". ".join(titles)
        summary = self.ai.generate_summary(f"Tech Briefing {target_date}", prompt_content)
        
        try:
            briefing = Briefing(briefing_date=target_date, summary_text=summary)
            self.db.add(briefing)
            self.db.flush()
            
            for i, article in enumerate(top_articles):
                ba = BriefingArticle(briefing_id=briefing.id, article_id=article.id, rank_position=i+1)
                self.db.add(ba)
                
            self.db.commit()
            return self.get_briefing_by_date(target_date)
            
        except IntegrityError:
            self.db.rollback()
            logger.error(f"Concurrent generation of briefing for {target_date}")
            return self.get_briefing_by_date(target_date)
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error generating briefing: {e}")
            raise e
