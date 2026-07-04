"""Add invite_codes table for invite-gated signup."""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "002_invite_codes"
down_revision: Union[str, None] = "001_initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "invite_codes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("code", sa.String(64), nullable=False, unique=True),
        sa.Column("max_uses", sa.Integer, nullable=False, server_default="1"),
        sa.Column("uses_count", sa.Integer, nullable=False, server_default="0"),
        sa.Column("note", sa.String(200)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_invite_codes_code", "invite_codes", ["code"])


def downgrade() -> None:
    op.drop_index("ix_invite_codes_code", table_name="invite_codes")
    op.drop_table("invite_codes")
