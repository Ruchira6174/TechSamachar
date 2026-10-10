"""add preferences and bookmarks

Revision ID: 3a2c5d7b9e0f
Revises: 5b4c1a2d3e4f  # Placeholder previous revision
Create Date: 2026-10-09 16:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '3a2c5d7b9e0f'
down_revision = '5b4c1a2d3e4f' # Assuming previous migration id
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Preferences
    op.create_table('preferences',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('preferred_sort', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_preferences_id'), 'preferences', ['id'], unique=False)
    op.create_index(op.f('ix_preferences_user_id'), 'preferences', ['user_id'], unique=True)
    
    # Topic Preferences
    op.create_table('topic_preferences',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('preference_id', sa.Integer(), nullable=False),
        sa.Column('topic_id', sa.Integer(), nullable=False),
        sa.Column('weight', sa.Float(), nullable=True),
        sa.Column('is_enabled', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['preference_id'], ['preferences.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['topic_id'], ['topics.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_topic_preferences_id'), 'topic_preferences', ['id'], unique=False)
    
    # Bookmarks
    op.create_table('bookmarks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('article_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bookmarks_id'), 'bookmarks', ['id'], unique=False)
    op.create_index(op.f('ix_bookmarks_user_id'), 'bookmarks', ['user_id'], unique=False)

    # Feedback
    op.create_table('feedback',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('article_id', sa.Integer(), nullable=False),
        sa.Column('feedback_type', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_feedback_id'), 'feedback', ['id'], unique=False)
    op.create_index(op.f('ix_feedback_user_id'), 'feedback', ['user_id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_feedback_user_id'), table_name='feedback')
    op.drop_index(op.f('ix_feedback_id'), table_name='feedback')
    op.drop_table('feedback')
    op.drop_index(op.f('ix_bookmarks_user_id'), table_name='bookmarks')
    op.drop_index(op.f('ix_bookmarks_id'), table_name='bookmarks')
    op.drop_table('bookmarks')
    op.drop_index(op.f('ix_topic_preferences_id'), table_name='topic_preferences')
    op.drop_table('topic_preferences')
    op.drop_index(op.f('ix_preferences_user_id'), table_name='preferences')
    op.drop_index(op.f('ix_preferences_id'), table_name='preferences')
    op.drop_table('preferences')
