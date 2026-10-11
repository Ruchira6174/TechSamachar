
import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from tech_samachar.db.models.article import Article
from tech_samachar.db.models.preference import Preference

logger = logging.getLogger(__name__)


def _as_utc_aware(value: datetime | None) -> datetime | None:
    """Normalize a datetime to timezone-aware UTC."""
    if value is None:
        return None

    if value.tzinfo is None:
        # SQLite may return naive datetimes even when timezone=True.
        # Treat stored naive values as UTC, consistent with this app's
        # UTC timestamp convention.
        return value.replace(tzinfo=timezone.utc)

    return value.astimezone(timezone.utc)


class RankingService:
    def __init__(self, db: Session):
        self.db = db

    def _get_user_preference(self, user_id: int = 1) -> Preference | None:
        return (
            self.db.query(Preference)
            .filter(Preference.user_id == user_id)
            .first()
        )

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
        topic_score = max(
            [topic.default_priority for topic in article.topics] + [0]
        )
        score += (topic_score / 100.0) * 0.4

        # 2. Relevance (25%) — placeholder until real relevance scoring.
        score += 0.8 * 0.25

        # 3. Freshness (20%) — decay over one week.
        published_time = _as_utc_aware(article.published_time)

        if published_time is not None:
            now = datetime.now(timezone.utc)
            hours_old = (now - published_time).total_seconds() / 3600
            freshness = max(0.0, 1.0 - (hours_old / (24 * 7)))
            score += freshness * 0.20

        # 4. Source quality (10%)
        source_quality = article.source.quality_score if article.source else 50
        score += (source_quality / 100.0) * 0.10

        # 5. Novelty (5%) — placeholder until real novelty scoring.
        score += 0.5 * 0.05

        return score

    def rank_articles(
        self, articles: list[Article], user_id: int = 1
    ) -> list[Article]:
        """Rank articles by score, then publication time."""
        scored = [
            (article, self.score_article(article, user_id))
            for article in articles
        ]

        scored.sort(
            key=lambda item: (
                item[1],
                _as_utc_aware(item[0].published_time)
                or datetime.min.replace(tzinfo=timezone.utc),
            ),
            reverse=True,
        )

        return [article for article, _ in scored]