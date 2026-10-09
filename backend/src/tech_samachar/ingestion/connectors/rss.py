import feedparser
import httpx
from typing import List, Dict, Any
import logging
from tech_samachar.ingestion.connectors.base import BaseConnector

logger = logging.getLogger(__name__)

class RSSConnector(BaseConnector):
    def fetch(self) -> List[Dict[str, Any]]:
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(self.source_url)
                response.raise_for_status()
                feed = feedparser.parse(response.text)
                
                if feed.bozo:
                    logger.warning(f"Malformed feed detected for {self.source_url}: {feed.bozo_exception}")
                    
                return feed.entries
        except Exception as e:
            logger.error(f"Error fetching RSS from {self.source_url}: {e}")
            raise
