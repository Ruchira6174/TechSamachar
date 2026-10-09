import pytest
from datetime import date
from fastapi.testclient import TestClient
from tech_samachar.main import app
from tech_samachar.services.briefing_service import BriefingService
from tech_samachar.db.models.article import Article
from tech_samachar.db.models.source import Source

client = TestClient(app)

def test_generate_briefing(db_session):
    service = BriefingService(db_session)
    # Add dummy source and article
    source = Source(name="Test Source", url="test", feed_url="test")
    db_session.add(source)
    db_session.flush()

    article = Article(title="Test", canonical_url="test", source_id=source.id, content_hash="hash")
    db_session.add(article)
    db_session.commit()

    briefing = service.generate_briefing(date.today())
    assert briefing is not None
    assert briefing.briefing_date == date.today()
    assert len(briefing.articles) == 1

def test_get_latest_briefing(db_session):
    response = client.get("/api/v1/briefing")
    assert response.status_code == 200
    assert "briefing_date" in response.json()
