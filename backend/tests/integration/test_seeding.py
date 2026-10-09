import pytest
from tech_samachar.ingestion.seed import seed_topics, seed_sources
from tech_samachar.db.models.article import Topic
from tech_samachar.db.models.source import Source

def test_repeatable_seeding(db_session):
    # First seed
    seed_topics(db_session)
    seed_sources(db_session)
    
    topics_count_1 = db_session.query(Topic).count()
    sources_count_1 = db_session.query(Source).count()
    
    assert topics_count_1 > 0
    assert sources_count_1 > 0
    
    # Second seed
    seed_topics(db_session)
    seed_sources(db_session)
    
    topics_count_2 = db_session.query(Topic).count()
    sources_count_2 = db_session.query(Source).count()
    
    # Assert counts remain the same (no duplicates)
    assert topics_count_1 == topics_count_2
    assert sources_count_1 == sources_count_2
