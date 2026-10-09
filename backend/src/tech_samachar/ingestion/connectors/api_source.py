import httpx
from typing import List, Dict, Any
import logging
from tech_samachar.ingestion.connectors.base import BaseConnector

logger = logging.getLogger(__name__)

class APISourceConnector(BaseConnector):
    def fetch(self) -> List[Dict[str, Any]]:
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(self.source_url)
                response.raise_for_status()
                data = response.json()
                
                # Assuming standard API response. Adjust logic based on API shape.
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict) and "articles" in data:
                    return data["articles"]
                return []
        except Exception as e:
            logger.error(f"Error fetching API from {self.source_url}: {e}")
            raise
