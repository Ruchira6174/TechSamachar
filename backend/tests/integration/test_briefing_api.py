
from datetime import date, datetime, time, timezone
from unittest.mock import patch

from fastapi.testclient import TestClient

from tech_samachar.db.models.article import Article
from tech_samachar.db.models.source import Source
from tech_samachar.services.briefing_service import BriefingService


def add_test_article(db_session, url: str, title: str):
    source = Source(
        name=f"Source for {title}",
        url=f"{url}/source",
        feed_url=f"{url}/feed",
    )
    db_session.add(source)
    db_session.flush()

    article = Article(
        title=title,
        canonical_url=url,
        source_id=source.id,
        content_hash=f"hash-{title}",
        published_time=datetime.combine(
            date.today(), time.min, tzinfo=timezone.utc
        ),
    )
    db_session.add(article)
    db_session.commit()
    return article


def test_generate_briefing(db_session):
    today = date.today()
    add_test_article(
        db_session,
        "https://example.com/briefing-article",
        "Test Article",
    )

    with patch(
        "tech_samachar.services.briefing_service.get_ai_provider"
    ) as mock_provider_factory:
        mock_provider_factory.return_value.generate_summary.return_value = (
            "A deterministic test briefing."
        )
        service = BriefingService(db_session)
        briefing = service.generate_briefing(today)

    assert briefing is not None
    assert briefing.briefing_date == today
    assert len(briefing.articles) == 1


def test_get_latest_briefing(client: TestClient, db_session):
    today = date.today()
    add_test_article(
        db_session,
        "https://example.org/briefing-article",
        "Briefing API Test Article",
    )

    with patch(
        "tech_samachar.services.briefing_service.get_ai_provider"
    ) as mock_provider_factory:
        mock_provider_factory.return_value.generate_summary.return_value = (
            "A deterministic test briefing."
        )
        briefing = BriefingService(db_session).generate_briefing(today)

    assert briefing is not None

    response = client.get("/api/v1/briefing")

    assert response.status_code == 200
    assert "briefing_date" in response.json()