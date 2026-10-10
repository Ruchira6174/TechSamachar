
"""create core tables

Revision ID: 5b4c1a2d3e4f
Revises:
Create Date: 2026-10-10
"""

from alembic import op
import sqlalchemy as sa

revision = "5b4c1a2d3e4f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Sources
    op.create_table(
        "sources",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("feed_url", sa.String(), nullable=False),
        sa.Column("source_type", sa.String(), nullable=True),
        sa.Column("is_enabled", sa.Boolean(), nullable=True),
        sa.Column("quality_score", sa.Integer(), nullable=True),
        sa.Column("last_successful_fetch", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("feed_url"),
    )
    op.create_index("ix_sources_id", "sources", ["id"])
    op.create_index("ix_sources_name", "sources", ["name"])
    op.create_index("ix_sources_feed_url", "sources", ["feed_url"], unique=True)

    # 2. Topics
    op.create_table(
        "topics",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("default_priority", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("slug"),
    )
    op.create_index("ix_topics_id", "topics", ["id"])
    op.create_index("ix_topics_name", "topics", ["name"], unique=True)
    op.create_index("ix_topics_slug", "topics", ["slug"], unique=True)

    # 3. Articles
    op.create_table(
        "articles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("canonical_url", sa.String(), nullable=False),
        sa.Column("source_id", sa.Integer(), nullable=False),
        sa.Column("author", sa.String(), nullable=True),
        sa.Column("published_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("content_hash", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["source_id"], ["sources.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("canonical_url"),
    )
    op.create_index("ix_articles_id", "articles", ["id"])
    op.create_index("ix_articles_canonical_url", "articles", ["canonical_url"], unique=True)
    op.create_index("ix_articles_content_hash", "articles", ["content_hash"])

    # 4. Article summaries
    op.create_table(
        "article_summaries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("article_id", sa.Integer(), nullable=False),
        sa.Column("summary_text", sa.Text(), nullable=False),
        sa.Column("provider", sa.String(), nullable=True),
        sa.Column("model_name", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["article_id"], ["articles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("article_id"),
    )
    op.create_index("ix_article_summaries_id", "article_summaries", ["id"])

    # 5. Article-topic association
    op.create_table(
        "article_topic",
        sa.Column("article_id", sa.Integer(), nullable=False),
        sa.Column("topic_id", sa.Integer(), nullable=False),
        sa.Column("confidence", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["article_id"], ["articles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["topic_id"], ["topics.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("article_id", "topic_id"),
    )


def downgrade() -> None:
    op.drop_table("article_topic")

    op.drop_index("ix_article_summaries_id", table_name="article_summaries")
    op.drop_table("article_summaries")

    op.drop_index("ix_articles_content_hash", table_name="articles")
    op.drop_index("ix_articles_canonical_url", table_name="articles")
    op.drop_index("ix_articles_id", table_name="articles")
    op.drop_table("articles")

    op.drop_index("ix_topics_slug", table_name="topics")
    op.drop_index("ix_topics_name", table_name="topics")
    op.drop_index("ix_topics_id", table_name="topics")
    op.drop_table("topics")

    op.drop_index("ix_sources_feed_url", table_name="sources")
    op.drop_index("ix_sources_name", table_name="sources")
    op.drop_index("ix_sources_id", table_name="sources")
    op.drop_table("sources")