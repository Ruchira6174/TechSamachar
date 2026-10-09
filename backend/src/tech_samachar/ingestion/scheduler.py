import time
import logging
from tech_samachar.db.session import SessionLocal
from tech_samachar.ingestion.pipeline import run_pipeline

logger = logging.getLogger(__name__)

def start_scheduler(interval_seconds: int = 3600):
    logger.info("Starting lightweight ingestion scheduler...")
    while True:
        db = SessionLocal()
        try:
            logger.info("Running scheduled ingestion pipeline...")
            stats = run_pipeline(db)
            logger.info(f"Ingestion completed. Stats: {stats}")
        except Exception as e:
            logger.error(f"Scheduler pipeline error: {e}")
        finally:
            db.close()
            
        logger.info(f"Sleeping for {interval_seconds} seconds.")
        time.sleep(interval_seconds)
