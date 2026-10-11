
from fastapi.testclient import TestClient

from tech_samachar.db.models.article import Article
from tech_samachar.db.models.source import Source


def test_get_news_empty(client: TestClient):
    response = client.get("/api/v1/news")

    assert response.status_code == 200
    assert response.json()["pagination"]["total"] == 0


def test_get_news_with_data(client: TestClient, db_session):
    source = Source(
        name="Test",
        url="https://example.com",
        feed_url="https://example.com/feed",
    )
    db_session.add(source)
    db_session.commit()
    db_session.refresh(source)

    article = Article(
        title="Test Article",
        canonical_url="https://example.com/article",
        source_id=source.id,
        content_hash="test-content-hash",
    )
    db_session.add(article)
    db_session.commit()

    response = client.get("/api/v1/news")

    assert response.status_code == 200
    data = response.json()
    assert data["pagination"]["total"] == 1
    assert data["items"][0]["title"] == "Test Article"


def test_get_article_not_found(client: TestClient):
    response = client.get("/api/v1/news/999")
    assert response.status_code == 404


def test_search_validation(client: TestClient):
    response = client.get("/api/v1/search?q=")
    assert response.status_code == 422