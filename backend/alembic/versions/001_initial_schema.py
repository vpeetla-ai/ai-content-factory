"""Initial schema — 6 tables per architecture."""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")

    user_role = postgresql.ENUM("admin", "editor", "viewer", name="userrole", create_type=True)
    pipeline_status = postgresql.ENUM("running", "hitl_wait", "done", "error", name="pipelinestatus", create_type=True)
    platform = postgresql.ENUM("linkedin", "substack", "medium", "instagram", "x", name="platform", create_type=True)

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("name", sa.String(100)),
        sa.Column("clerk_id", sa.String(100)),
        sa.Column("role", user_role, nullable=False, server_default="editor"),
        sa.Column("platform_tokens", postgresql.JSONB),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "pipeline_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("topic", sa.Text, nullable=False),
        sa.Column("status", pipeline_status, nullable=False, server_default="running"),
        sa.Column("langgraph_run_id", sa.String(100)),
        sa.Column("state_snapshot", postgresql.JSONB),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("completed_at", sa.DateTime(timezone=True)),
        sa.Column("total_tokens", sa.Integer, server_default="0"),
        sa.Column("total_cost_usd", sa.Numeric(10, 6), server_default="0"),
    )
    op.create_index("ix_pipeline_runs_topic", "pipeline_runs", ["topic"])

    op.create_table(
        "content_drafts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("run_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("pipeline_runs.id"), nullable=False),
        sa.Column("platform", platform, nullable=False),
        sa.Column("draft_content", sa.Text, nullable=False),
        sa.Column("edited_content", sa.Text),
        sa.Column("seo_keywords", postgresql.ARRAY(sa.Text)),
        sa.Column("hashtags", postgresql.ARRAY(sa.Text)),
        sa.Column("hook_variant", sa.Text),
        sa.Column("char_count", sa.Integer, server_default="0"),
        sa.Column("approved_by", postgresql.UUID(as_uuid=True)),
    )
    op.create_index("ix_content_drafts_platform", "content_drafts", ["platform"])

    op.create_table(
        "published_posts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("draft_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("content_drafts.id"), nullable=False),
        sa.Column("platform", sa.String(50), nullable=False),
        sa.Column("external_post_id", sa.String(200)),
        sa.Column("post_url", sa.Text),
        sa.Column("published_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("analytics_data", postgresql.JSONB),
    )
    op.create_index("ix_published_posts_platform", "published_posts", ["platform"])

    op.create_table(
        "api_keys",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("key_hash", sa.String(64), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("scopes", postgresql.ARRAY(sa.Text)),
        sa.Column("last_used_at", sa.DateTime(timezone=True)),
        sa.Column("expires_at", sa.DateTime(timezone=True)),
    )

    op.create_table(
        "agent_traces",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("run_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("pipeline_runs.id"), nullable=False),
        sa.Column("agent_name", sa.String(50), nullable=False),
        sa.Column("model_used", sa.String(100)),
        sa.Column("input_tokens", sa.Integer, server_default="0"),
        sa.Column("output_tokens", sa.Integer, server_default="0"),
        sa.Column("latency_ms", sa.Integer, server_default="0"),
        sa.Column("langfuse_trace_id", sa.String(100)),
        sa.Column("error_msg", sa.Text),
    )
    op.create_index("ix_agent_traces_agent_name", "agent_traces", ["agent_name"])


def downgrade() -> None:
    op.drop_table("agent_traces")
    op.drop_table("api_keys")
    op.drop_table("published_posts")
    op.drop_table("content_drafts")
    op.drop_table("pipeline_runs")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS platform")
    op.execute("DROP TYPE IF EXISTS pipelinestatus")
    op.execute("DROP TYPE IF EXISTS userrole")
