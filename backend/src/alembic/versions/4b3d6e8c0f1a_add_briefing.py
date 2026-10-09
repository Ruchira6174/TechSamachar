"""add briefing tables

Revision ID: 4b3d6e8c0f1a
Revises: 3a2c5d7b9e0f
Create Date: 2026-10-09 16:40:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4b3d6e8c0f1a'
down_revision = '3a2c5d7b9e0f'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Briefings
    op.create_table('briefings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('briefing_date', sa.Date(), nullable=False),
        sa.Column('summary_text', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_briefings_id'), 'briefings', ['id'], unique=False)
    op.create_index(op.f('ix_briefings_briefing_date'), 'briefings', ['briefing_date'], unique=True)
    
    # Briefing Articles
    op.create_table('briefing_articles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('briefing_id', sa.Integer(), nullable=False),
        sa.Column('article_id', sa.Integer(), nullable=False),
        sa.Column('rank_position', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['briefing_id'], ['briefings.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_briefing_articles_id'), 'briefing_articles', ['id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_briefing_articles_id'), table_name='briefing_articles')
    op.drop_table('briefing_articles')
    op.drop_index(op.f('ix_briefings_briefing_date'), table_name='briefings')
    op.drop_index(op.f('ix_briefings_id'), table_name='briefings')
    op.drop_table('briefings')
