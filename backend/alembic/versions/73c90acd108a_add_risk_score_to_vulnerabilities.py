"""add_risk_score_to_vulnerabilities

Revision ID: 73c90acd108a
Revises: dc3271fdaa6d
Create Date: 2026-07-16 21:50:55.758765

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73c90acd108a'
down_revision = 'dc3271fdaa6d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('vulnerabilities', sa.Column('risk_score', sa.Float(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('vulnerabilities', schema=None) as batch_op:
        batch_op.drop_column('risk_score')

