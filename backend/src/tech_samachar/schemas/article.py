from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from tech_samachar.schemas.source import SourceResponse
from tech_samachar.schemas.topic import TopicResponse

class ArticleSummaryResponse(BaseModel):
    id: int
    summary_text: str
    provider: Optional[str]
    model_name: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class ArticleBase(BaseModel):
    title: str
    canonical_url: str
    author: Optional[str] = None
    published_time: Optional[datetime] = None
    description: Optional[str] = None

class ArticleResponse(ArticleBase):
    id: int
    source_id: int
    source: Optional[SourceResponse] = None
    topics: List[TopicResponse] = []
    summary: Optional[ArticleSummaryResponse] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
