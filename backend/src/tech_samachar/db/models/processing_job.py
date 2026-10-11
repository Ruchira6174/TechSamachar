
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from tech_samachar.db.base import Base


def utc_now():
    return datetime.now(timezone.utc)


class ArticleProcessingJob(Base):
    __tablename__ = "article_processing_jobs"

    __table_args__ = (
        UniqueConstraint(
            "article_id",
            "job_type",
            name="uq_article_processing_job_type",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    article_id = Column(
        Integer,
        ForeignKey("articles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    job_type = Column(String(30), nullable=False)
    status = Column(String(20), nullable=False, default="pending", index=True)

    attempts = Column(Integer, nullable=False, default=0)
    next_retry_at = Column(DateTime(timezone=True), nullable=True)
    last_error = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )