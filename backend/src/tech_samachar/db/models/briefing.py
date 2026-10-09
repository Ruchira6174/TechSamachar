from datetime import datetime, date, timezone
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from tech_samachar.db.base import Base

class Briefing(Base):
    __tablename__ = "briefings"
    
    id = Column(Integer, primary_key=True, index=True)
    briefing_date = Column(Date, unique=True, index=True, nullable=False, default=date.today)
    summary_text = Column(String, nullable=False)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    articles = relationship("BriefingArticle", back_populates="briefing", cascade="all, delete-orphan")

class BriefingArticle(Base):
    __tablename__ = "briefing_articles"
    
    id = Column(Integer, primary_key=True, index=True)
    briefing_id = Column(Integer, ForeignKey("briefings.id", ondelete="CASCADE"), nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False)
    rank_position = Column(Integer, nullable=False)
    
    briefing = relationship("Briefing", back_populates="articles")
    article = relationship("Article")
