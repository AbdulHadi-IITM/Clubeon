"""repair columns missed during the two-head migration window

While two migration heads existed, a database could upgrade along one branch
and silently skip the other — alembic then records both as applied. Databases
in that state are missing courts.sport_type even though its migration is marked
done. Every step here is guarded, so this is a no-op on healthy databases.

Revision ID: 2e7c9a4f1b05
Revises: 1d4ae3b7d398
Create Date: 2026-08-23

"""
from alembic import op
import sqlalchemy as sa

revision = '2e7c9a4f1b05'
down_revision = '1d4ae3b7d398'
branch_labels = None
depends_on = None


def _columns(table):
    insp = sa.inspect(op.get_bind())
    if not insp.has_table(table):
        return set()
    return {c['name'] for c in insp.get_columns(table)}


def upgrade():
    if 'sport_type' not in _columns('courts'):
        with op.batch_alter_table('courts') as batch_op:
            batch_op.add_column(sa.Column(
                'sport_type', sa.String(length=30),
                nullable=False, server_default='multi-purpose'))


def downgrade():
    # Owned by a91c4d7e2b10; nothing to undo here.
    pass
