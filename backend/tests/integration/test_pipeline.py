from tech_samachar.ingestion.pipeline import run_pipeline
from tech_samachar.db.models.source import Source
from tech_samachar.db.models.article import Article
from typing import List, Dict, Any
import pytest

class MockConnector:
    def __init__(self, url):
        self.url = url
        
    def fetch(self) -> List[Dict[str, Any]]:
        if "fail" in self.url:
            raise Exception("Mock connection error")
        return [
            {
                "title": f"Article from {self.url}",
                "link": f"{self.url}/article1",
            }
        ]

@pytest.fixture(autouse=True)
def mock_get_connector(monkeypatch):
    def _mock_get(source_type, url):
        return MockConnector(url)
    monkeypatch.setattr("tech_samachar.ingestion.pipeline.get_connector", _mock_get)

def test_pipeline_continues_on_failure(db_session):
    # Create two sources, one designed to fail
    s1 = Source(name="Good", url="https://good.com", feed_url="https://good.com/feed", source_type="rss")
    s2 = Source(name="Bad", url="https://fail.com", feed_url="https://fail.com/feed", source_type="rss")
    
    db_session.add(s1)
    db_session.add(s2)
    db_session.commit()
    
    stats = run_pipeline(db_session)
    
    assert stats["processed_sources"] == 2
    assert stats["failed_sources"] == 1
    assert stats["saved_articles"] == 1
    
    # Check that article was saved from the good source
    article = db_session.query(Article).first()
    assert article is not None
    assert article.canonical_url == "https://good.com/feed/article1"
