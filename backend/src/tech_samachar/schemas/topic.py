from pydantic import BaseModel, ConfigDict

class TopicBase(BaseModel):
    name: str
    slug: str
    description: str | None = None
    default_priority: int

class TopicResponse(TopicBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
