from alembic import op
import sqlalchemy as sa


revision = "20260716_create_findings_table"
down_revision = "20260716_create_signals_table"
details = "Create findings table"


def upgrade() -> None:
    op.create_table(
        "findings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("severity", sa.String(length=40), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("signal_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["signal_id"], ["signals.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_findings_id"), "findings", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_findings_id"), table_name="findings")
    op.drop_table("findings")
