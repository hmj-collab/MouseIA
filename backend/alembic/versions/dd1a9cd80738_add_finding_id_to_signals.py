"""add_finding_id_to_signals

Revision ID: dd1a9cd80738
Revises: 257167865ef7
Create Date: 2026-07-16 21:42:21.914199

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd1a9cd80738'
down_revision = '257167865ef7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('signals', sa.Column('finding_id', sa.Integer(), nullable=True))
    with op.batch_alter_table('signals', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_signals_finding', 'findings', ['finding_id'], ['id'])
        batch_op.create_index('ix_signals_finding_id', ['finding_id'])


def downgrade() -> None:
    with op.batch_alter_table('signals', schema=None) as batch_op:
        batch_op.drop_index('ix_signals_finding_id')
        batch_op.drop_column('finding_id')

