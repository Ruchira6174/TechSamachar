from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import List
from tech_samachar.schemas.article import ArticleResponse

class BriefingArticleResponse(BaseModel):
    id: int
    rank_position: int
    article: ArticleResponse
    
    model_config = ConfigDict(from_attributes=True)

class BriefingResponse(BaseModel):
    id: int
    briefing_date: date
    summary_text: str
    created_at: datetime
    articles: List[BriefingArticleResponse]
    
    model_config = ConfigDict(from_attributes=True)
