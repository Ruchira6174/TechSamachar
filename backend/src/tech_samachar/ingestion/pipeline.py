from sqlalchemy.orm import Session
from tech_samachar.db.models.source import Source
from tech_samachar.db.models.article import Article
from tech_samachar.ingestion.registry import get_connector
from tech_samachar.ingestion.normalizer import Normalizer
from tech_samachar.ingestion.deduplicator import Deduplicator
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

def run_pipeline(db: Session) -> dict:
    stats = {
        "processed_sources": 0,
        "failed_sources": 0,
        "saved_articles": 0,
        "duplicate_articles": 0
    }
    
    sources = db.query(Source).filter(Source.is_enabled == True).all()
    
    for source in sources:
        stats["processed_sources"] += 1
        logger.info(f"Processing source: {source.name} ({source.feed_url})")
        
        try:
            connector = get_connector(source.source_type, source.feed_url)
            entries = connector.fetch()
            
            for entry in entries:
                if not entry.get("title") and not entry.get("link"):
                    continue
                
                normalized = Normalizer.normalize_entry(entry, source.id)
                
                if Deduplicator.is_duplicate(db, normalized):
                    stats["duplicate_articles"] += 1
                    continue
                
                try:
                    article = Article(**normalized)
                    db.add(article)
                    db.commit()
                    stats["saved_articles"] += 1
                    
                    # Safe AI processing
                    try:
                        from tech_samachar.ai.classifier import ClassifierService
                        from tech_samachar.ai.summarizer import SummarizerService
                        classifier = ClassifierService(db)
                        summarizer = SummarizerService(db)
                        classifier.classify_article(article)
                        summarizer.summarize_article(article)
                    except Exception as ai_e:
                        logger.error(f"AI processing failed for article {article.id}: {ai_e}")
                        
                except Exception as e:
                    logger.error(f"Error saving article {normalized.get('title')}: {e}")
                    db.rollback()
            
            # Update last successful fetch
            source.last_successful_fetch = datetime.now(timezone.utc)
            db.commit()
            
        except Exception as e:
            logger.error(f"Source failed {source.name}: {e}")
            stats["failed_sources"] += 1
            db.rollback()
            
    return stats
