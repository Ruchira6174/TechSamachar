import pytest
from tech_samachar.ingestion.deduplicator import Deduplicator
from tech_samachar.db.models.article import Article

def test_duplicate_url(db_session):
    article = Article(
        title="Original", 
        canonical_url="https://example.com/1",
        source_id=1,
        content_hash="hash1"
    )
    db_session.add(article)
    db_session.commit()
    
    # Check duplicate
    is_dup = Deduplicator.is_duplicate(db_session, {
        "canonical_url": "https://example.com/1",
        "content_hash": "hash2"
    })
    assert is_dup == True

def test_duplicate_hash(db_session):
    article = Article(
        title="Original", 
        canonical_url="https://example.com/1",
        source_id=1,
        content_hash="hash_same"
    )
    db_session.add(article)
    db_session.commit()
    
    # Check duplicate
    is_dup = Deduplicator.is_duplicate(db_session, {
        "canonical_url": "https://example.com/different",
        "content_hash": "hash_same"
    })
    assert is_dup == True

def test_not_duplicate(db_session):
    article = Article(
        title="Original", 
        canonical_url="https://example.com/1",
        source_id=1,
        content_hash="hash1"
    )
    db_session.add(article)
    db_session.commit()
    
    # Check not duplicate
    is_dup = Deduplicator.is_duplicate(db_session, {
        "canonical_url": "https://example.com/2",
        "content_hash": "hash2"
    })
    assert is_dup == False
