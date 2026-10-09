from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from tech_samachar.db.base import Base

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    url = Column(String, nullable=False)
    feed_url = Column(String, unique=True, index=True, nullable=False)
    source_type = Column(String, default="rss") # rss, api, etc.
    is_enabled = Column(Boolean, default=True)
    quality_score = Column(Integer, default=50) # 0-100
    
    last_successful_fetch = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
