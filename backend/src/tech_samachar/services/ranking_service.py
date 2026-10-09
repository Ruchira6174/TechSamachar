import logging
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from tech_samachar.db.models.article import Article
from tech_samachar.db.models.preference import Preference

logger = logging.getLogger(__name__)

class RankingService:
    def __init__(self, db: Session):
        self.db = db
        
    def _get_user_preference(self, user_id: int = 1) -> Preference:
        pref = self.db.query(Preference).filter(Preference.user_id == user_id).first()
        return pref

    def score_article(self, article: Article, user_id: int = 1) -> float:
        """
        Ranking formula:
        Topic preference: 40%
        Article relevance (dummy): 25%
        Freshness: 20%
        Source quality: 10%
        Novelty (dummy): 5%
        """
        score = 0.0
        
        # 1. Topic preference (40%)
        # In a real scenario, lookup topic_preferences for user. Using default_priority for now.
        topic_score = max([t.default_priority for t in article.topics] + [0])
        score += (topic_score / 100.0) * 0.4
        
        # 2. Relevance (25%)
        # Dummy value 0.8
        score += 0.8 * 0.25
        
        # 3. Freshness (20%)
        if article.published_time:
            hours_old = (datetime.now(timezone.utc) - article.published_time).total_seconds() / 3600
            freshness = max(0, 1.0 - (hours_old / (24 * 7))) # Decay over a week
            score += freshness * 0.20
            
        # 4. Source quality (10%)
        source_quality = article.source.quality_score if article.source else 50
        score += (source_quality / 100.0) * 0.10
        
        # 5. Novelty (5%)
        # Dummy value 0.5
        score += 0.5 * 0.05
        
        return score
        
    def rank_articles(self, articles: list[Article], user_id: int = 1) -> list[Article]:
        # Pre-compute scores and sort
        scored = [(a, self.score_article(a, user_id)) for a in articles]
        scored.sort(key=lambda x: (x[1], x[0].published_time), reverse=True)
        return [a for a, _ in scored]
