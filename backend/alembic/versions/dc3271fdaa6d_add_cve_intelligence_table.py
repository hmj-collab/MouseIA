"""add_cve_intelligence_table

Revision ID: dc3271fdaa6d
Revises: dd1a9cd80738
Create Date: 2026-07-16 21:49:01.947423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc3271fdaa6d'
down_revision = 'dd1a9cd80738'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'cve_intelligence',
        sa.Column('cve_id', sa.String(40), primary_key=True, nullable=False),
        sa.Column('cvss_score', sa.Float(), nullable=True),
        sa.Column('severity', sa.String(40), nullable=True),
        sa.Column('epss_score', sa.Float(), nullable=True),
        sa.Column('is_kev', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('last_fetched_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_cve_intelligence_cve_id', 'cve_intelligence', ['cve_id'])


def downgrade() -> None:
    op.drop_index('ix_cve_intelligence_cve_id', table_name='cve_intelligence')
    op.drop_table('cve_intelligence')

