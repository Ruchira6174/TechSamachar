import pytest
from fastapi.testclient import TestClient
from tech_samachar.main import app

client = TestClient(app)

def test_get_preferences(db_session):
    response = client.get("/api/v1/preferences")
    assert response.status_code == 200
    assert response.json()["preferred_sort"] == "relevance"

def test_update_preferences(db_session):
    # First get to init
    client.get("/api/v1/preferences")
    
    payload = {
        "preferred_sort": "published_time",
        "topic_preferences": [
            {"topic_id": 1, "weight": 2.0, "is_enabled": True}
        ]
    }
    response = client.put("/api/v1/preferences", json=payload)
    assert response.status_code == 200
    assert response.json()["preferred_sort"] == "published_time"
    assert len(response.json()["topic_preferences"]) == 1

def test_add_remove_bookmark(db_session):
    # Requires an article, which we mock in logic or just check 400 for invalid
    response = client.post("/api/v1/bookmarks/999")
    assert response.status_code == 400 # Invalid article ID
    
    response = client.delete("/api/v1/bookmarks/999")
    assert response.status_code == 204 # Deleting non-existent is fine

def test_submit_feedback(db_session):
    payload = {"article_id": 999, "feedback_type": "relevant"}
    response = client.post("/api/v1/feedback", json=payload)
    assert response.status_code == 400 # Invalid article ID
