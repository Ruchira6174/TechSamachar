
from fastapi.testclient import TestClient


def test_get_preferences(client: TestClient):
    response = client.get("/api/v1/preferences")

    assert response.status_code == 200
    assert response.json()["preferred_sort"] == "relevance"


def test_update_preferences(client: TestClient):
    # Initialize preferences before updating them.
    initial_response = client.get("/api/v1/preferences")
    assert initial_response.status_code == 200

    payload = {
        "preferred_sort": "published_time",
        "topic_preferences": [
            {"topic_id": 1, "weight": 2.0, "is_enabled": True}
        ],
    }
    response = client.put("/api/v1/preferences", json=payload)

    assert response.status_code == 200
    assert response.json()["preferred_sort"] == "published_time"
    assert len(response.json()["topic_preferences"]) == 1


def test_add_remove_bookmark(client: TestClient):
    response = client.post("/api/v1/bookmarks/999")
    assert response.status_code == 400

    response = client.delete("/api/v1/bookmarks/999")
    assert response.status_code == 204


def test_submit_feedback(client: TestClient):
    payload = {"article_id": 999, "feedback_type": "relevant"}
    response = client.post("/api/v1/feedback", json=payload)

    assert response.status_code == 400