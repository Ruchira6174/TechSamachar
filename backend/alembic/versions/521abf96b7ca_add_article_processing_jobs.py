
"""add article processing jobs

Revision ID: 521abf96b7ca
Revises: 4b3d6e8c0f1a
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "521abf96b7ca"
down_revision: Union[str, Sequence[str], None] = "4b3d6e8c0f1a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "article_processing_jobs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("article_id", sa.Integer(), nullable=False),
        sa.Column("job_type", sa.String(length=30), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("attempts", sa.Integer(), nullable=False),
        sa.Column("next_retry_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["article_id"],
            ["articles.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "article_id",
            "job_type",
            name="uq_article_processing_job_type",
        ),
    )

    op.create_index(
        "ix_article_processing_jobs_article_id",
        "article_processing_jobs",
        ["article_id"],
        unique=False,
    )
    op.create_index(
        "ix_article_processing_jobs_id",
        "article_processing_jobs",
        ["id"],
        unique=False,
    )
    op.create_index(
        "ix_article_processing_jobs_status",
        "article_processing_jobs",
        ["status"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_article_processing_jobs_status",
        table_name="article_processing_jobs",
    )
    op.drop_index(
        "ix_article_processing_jobs_id",
        table_name="article_processing_jobs",
    )
    op.drop_index(
        "ix_article_processing_jobs_article_id",
        table_name="article_processing_jobs",
    )
    op.drop_table("article_processing_jobs")