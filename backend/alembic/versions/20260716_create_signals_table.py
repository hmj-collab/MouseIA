from alembic import op
import sqlalchemy as sa


revision = "20260716_create_signals_table"
down_revision = "7d87bc0d3738"
details = "Create signals table"


def upgrade() -> None:
    op.create_table(
        "signals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("source", sa.String(length=80), nullable=False),
        sa.Column("signal_type", sa.String(length=80), nullable=False),
        sa.Column("severity", sa.String(length=40), nullable=False),
        sa.Column("confidence", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("site_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["site_id"], ["sites.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_signals_id"), "signals", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_signals_id"), table_name="signals")
    op.drop_table("signals")
