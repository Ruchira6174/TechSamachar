from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseConnector(ABC):
    def __init__(self, source_url: str):
        self.source_url = source_url

    @abstractmethod
    def fetch(self) -> List[Dict[str, Any]]:
        """Fetch raw articles from the source."""
        pass
