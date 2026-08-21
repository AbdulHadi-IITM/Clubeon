"""add sport type to courts

Revision ID: a91c4d7e2b10
Revises: f05db257887e
"""
from alembic import op
import sqlalchemy as sa

revision = 'a91c4d7e2b10'
down_revision = 'f05db257887e'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('courts') as batch_op:
        batch_op.add_column(sa.Column('sport_type', sa.String(length=30), nullable=False, server_default='multi-purpose'))

def downgrade():
    with op.batch_alter_table('courts') as batch_op:
        batch_op.drop_column('sport_type')
