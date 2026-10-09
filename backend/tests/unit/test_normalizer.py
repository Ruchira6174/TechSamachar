from tech_samachar.ingestion.normalizer import Normalizer
from datetime import datetime, timezone
import pytest

def test_normalize_entry():
    entry = {
        "title": "Test Title",
        "link": "https://example.com/article",
        "author": "John Doe",
        "description": "A test description",
        "published": "Tue, 09 Oct 2026 10:00:00 +0000"
    }
    
    normalized = Normalizer.normalize_entry(entry, 1)
    
    assert normalized["title"] == "Test Title"
    assert normalized["canonical_url"] == "https://example.com/article"
    assert normalized["author"] == "John Doe"
    assert normalized["description"] == "A test description"
    assert normalized["source_id"] == 1
    assert normalized["content_hash"] is not None
    assert normalized["published_time"] is not None
    assert normalized["published_time"].tzinfo == timezone.utc

def test_missing_publication_date():
    entry = {
        "title": "No Date",
        "link": "https://example.com/nodate",
    }
    normalized = Normalizer.normalize_entry(entry, 1)
    assert normalized["published_time"] is None
