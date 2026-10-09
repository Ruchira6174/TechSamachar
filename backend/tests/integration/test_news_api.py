import pytest
from fastapi.testclient import TestClient
from tech_samachar.main import app
from tech_samachar.db.models.article import Article, Topic
from tech_samachar.db.models.source import Source

client = TestClient(app)

def test_get_news_empty(db_session):
    response = client.get("/api/v1/news")
    assert response.status_code == 200
    assert response.json()["pagination"]["total"] == 0

def test_get_news_with_data(db_session):
    # Setup data
    source = Source(name="Test", url="http", feed_url="http/feed")
    db_session.add(source)
    db_session.commit()
    
    article = Article(title="Test Article", canonical_url="http/art", source_id=source.id, content_hash="hash")
    db_session.add(article)
    db_session.commit()
    
    response = client.get("/api/v1/news")
    assert response.status_code == 200
    data = response.json()
    assert data["pagination"]["total"] == 1
    assert data["items"][0]["title"] == "Test Article"

def test_get_article_not_found():
    response = client.get("/api/v1/news/999")
    assert response.status_code == 404

def test_search_validation():
    response = client.get("/api/v1/search?q=") # Empty query
    assert response.status_code == 422 # Validation error
