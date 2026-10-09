from abc import ABC, abstractmethod
from typing import Dict, Any, List

class AIProvider(ABC):
    @abstractmethod
    def generate_summary(self, title: str, content: str) -> str:
        pass
        
    @abstractmethod
    def classify_topics(self, title: str, content: str, available_topics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        pass
