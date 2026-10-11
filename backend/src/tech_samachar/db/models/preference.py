
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from tech_samachar.db.base import Base


def utc_now():
    return datetime.now(timezone.utc)


class Preference(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, default=1, index=True, unique=True)
    preferred_sort = Column(String, default="relevance")

    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )

    topic_preferences = relationship(
        "TopicPreference",
        back_populates="preference",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class TopicPreference(Base):
    __tablename__ = "topic_preferences"

    id = Column(Integer, primary_key=True, index=True)
    preference_id = Column(
        Integer,
        ForeignKey("preferences.id", ondelete="CASCADE"),
        nullable=False,
    )
    topic_id = Column(
        Integer,
        ForeignKey("topics.id", ondelete="CASCADE"),
        nullable=False,
    )
    weight = Column(Float, default=1.0)
    is_enabled = Column(Boolean, default=True)

    preference = relationship(
        "Preference",
        back_populates="topic_preferences",
    )


class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, default=1, index=True)
    article_id = Column(
        Integer,
        ForeignKey("articles.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at = Column(DateTime(timezone=True), default=utc_now)

    article = relationship("Article")


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, default=1, index=True)
    article_id = Column(
        Integer,
        ForeignKey("articles.id", ondelete="CASCADE"),
        nullable=False,
    )
    feedback_type = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), default=utc_now)