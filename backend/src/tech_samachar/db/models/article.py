from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from tech_samachar.db.base import Base

# Association table for many-to-many relationship
article_topic_association = Table(
    "article_topic",
    Base.metadata,
    Column("article_id", Integer, ForeignKey("articles.id", ondelete="CASCADE"), primary_key=True),
    Column("topic_id", Integer, ForeignKey("topics.id", ondelete="CASCADE"), primary_key=True),
    Column("confidence", Integer, default=100) # 0-100 score
)

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    default_priority = Column(Integer, default=50) # 0-100 (e.g. Quantum Computing gets 100)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    canonical_url = Column(String, unique=True, index=True, nullable=False)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    author = Column(String, nullable=True)
    published_time = Column(DateTime(timezone=True), nullable=True)
    description = Column(Text, nullable=True)
    content_hash = Column(String, index=True, nullable=False)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    source = relationship("Source")
    topics = relationship("Topic", secondary=article_topic_association, backref="articles")
    summary = relationship("ArticleSummary", back_populates="article", uselist=False, cascade="all, delete-orphan")

class ArticleSummary(Base):
    __tablename__ = "article_summaries"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), unique=True, nullable=False)
    summary_text = Column(Text, nullable=False)
    provider = Column(String, nullable=True)
    model_name = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    article = relationship("Article", back_populates="summary")
