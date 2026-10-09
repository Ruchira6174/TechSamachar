from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from tech_samachar.db.base import Base

class Preference(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, default=1, index=True, unique=True) # Single user default
    preferred_sort = Column(String, default="relevance")
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class TopicPreference(Base):
    __tablename__ = "topic_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    preference_id = Column(Integer, ForeignKey("preferences.id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    weight = Column(Float, default=1.0) # 0.0 to 2.0 multiplier
    is_enabled = Column(Boolean, default=True)

class Bookmark(Base):
    __tablename__ = "bookmarks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, default=1, index=True)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    article = relationship("Article")

class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, default=1, index=True)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False)
    feedback_type = Column(String, nullable=False) # 'relevant', 'not_relevant', 'more_like_this', 'less_like_this'
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
