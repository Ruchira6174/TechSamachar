from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from tech_samachar.schemas.article import ArticleResponse

class TopicPreferenceBase(BaseModel):
    topic_id: int
    weight: float
    is_enabled: bool

class TopicPreferenceResponse(TopicPreferenceBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class PreferenceBase(BaseModel):
    preferred_sort: str
    topic_preferences: List[TopicPreferenceBase]

class PreferenceResponse(PreferenceBase):
    id: int
    user_id: int
    topic_preferences: List[TopicPreferenceResponse]
    
    model_config = ConfigDict(from_attributes=True)

class BookmarkBase(BaseModel):
    article_id: int

class BookmarkResponse(BookmarkBase):
    id: int
    user_id: int
    created_at: datetime
    article: Optional[ArticleResponse] = None
    
    model_config = ConfigDict(from_attributes=True)

class FeedbackBase(BaseModel):
    article_id: int
    feedback_type: str

class FeedbackResponse(FeedbackBase):
    id: int
    user_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
