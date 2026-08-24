"""add membership plans pricing and durations

Revision ID: c1f92e34d567
Revises: ('b0e318cfb76a', 'a91c4d7e2b10')
Create Date: 2026-08-24
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1f92e34d567'
down_revision = ('b0e318cfb76a', 'a91c4d7e2b10')
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('membership_plans', schema=None) as batch_op:
        batch_op.add_column(sa.Column('price', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('duration_months', sa.Integer(), nullable=True, server_default='1'))
        batch_op.add_column(sa.Column('discount_percentage', sa.Float(), nullable=True, server_default='0.0'))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True))
        batch_op.alter_column('club_id', existing_type=sa.Integer(), nullable=True)

    try:
        op.execute("UPDATE membership_plans SET price = price_monthly WHERE price IS NULL AND price_monthly IS NOT NULL")
    except Exception:
        pass
    try:
        op.execute("UPDATE membership_plans SET price = 499 WHERE price IS NULL")
    except Exception:
        pass

    with op.batch_alter_table('membership_plans', schema=None) as batch_op:
        batch_op.alter_column('price', existing_type=sa.Float(), nullable=False)
        batch_op.alter_column('duration_months', existing_type=sa.Integer(), nullable=False)

    with op.batch_alter_table('memberships', schema=None) as batch_op:
        batch_op.alter_column('club_id', existing_type=sa.Integer(), nullable=True)


def downgrade():
    with op.batch_alter_table('memberships', schema=None) as batch_op:
        batch_op.alter_column('club_id', existing_type=sa.Integer(), nullable=False)

    with op.batch_alter_table('membership_plans', schema=None) as batch_op:
        batch_op.drop_column('created_at')
        batch_op.drop_column('discount_percentage')
        batch_op.drop_column('duration_months')
        batch_op.drop_column('price')
        batch_op.alter_column('club_id', existing_type=sa.Integer(), nullable=False)
