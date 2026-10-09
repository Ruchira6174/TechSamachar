from pydantic import BaseModel, ConfigDict

class SourceBase(BaseModel):
    name: str
    url: str
    feed_url: str
    source_type: str

class SourceResponse(SourceBase):
    id: int
    is_enabled: bool
    quality_score: int

    model_config = ConfigDict(from_attributes=True)
