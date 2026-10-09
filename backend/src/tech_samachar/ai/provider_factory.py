import logging
from typing import Dict, Any, List
from tech_samachar.ai.base import AIProvider
from tech_samachar.config import settings

logger = logging.getLogger(__name__)

class DummyProvider(AIProvider):
    """Deterministic fallback for development"""
    def generate_summary(self, title: str, content: str) -> str:
        return f"This is an automated dummy summary for: {title}. Real AI provider is not configured."
        
    def classify_topics(self, title: str, content: str, available_topics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Dummy classification - just pick the first topic
        if available_topics:
            return [{"topic_id": available_topics[0]["id"], "confidence": 85}]
        return []

def get_ai_provider() -> AIProvider:
    if settings.AI_PROVIDER == "none" or not settings.AI_API_KEY:
        logger.warning("Using Dummy AI Provider. Set AI_PROVIDER and AI_API_KEY for real AI.")
        return DummyProvider()
    
    # Placeholder for real implementations (OpenAI/Anthropic/Gemini)
    return DummyProvider()
