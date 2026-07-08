"""Aggregate anonymized production metrics for public ops dashboard."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AgentTrace, InviteCode, PipelineRun, PipelineStatus, User

SLO_TARGET_UPTIME_PCT = 99.5
SLO_PIPELINE_SUCCESS_TARGET_PCT = 95.0


async def collect_ops_metrics(db: AsyncSession) -> dict:
    now = datetime.now(timezone.utc)
    week_ago = now - timedelta(days=7)

    total_runs = await _scalar(db, select(func.count()).select_from(PipelineRun))
    completed_runs = await _scalar(
        db,
        select(func.count())
        .select_from(PipelineRun)
        .where(PipelineRun.status == PipelineStatus.done),
    )
    error_runs = await _scalar(
        db,
        select(func.count())
        .select_from(PipelineRun)
        .where(PipelineRun.status == PipelineStatus.error),
    )
    hitl_runs = await _scalar(
        db,
        select(func.count())
        .select_from(PipelineRun)
        .where(PipelineRun.status == PipelineStatus.hitl_wait),
    )
    runs_last_7d = await _scalar(
        db,
        select(func.count())
        .select_from(PipelineRun)
        .where(PipelineRun.started_at >= week_ago),
    )
    invited_users = await _scalar(db, select(func.count()).select_from(User))
    invite_codes_issued = await _scalar(db, select(func.count()).select_from(InviteCode))

    cost_row = await db.execute(select(func.coalesce(func.sum(PipelineRun.total_cost_usd), 0)))
    total_cost_usd = float(cost_row.scalar_one())

    latency_row = await db.execute(
        select(
            func.avg(AgentTrace.latency_ms),
            func.percentile_cont(0.5).within_group(AgentTrace.latency_ms),
            func.percentile_cont(0.95).within_group(AgentTrace.latency_ms),
        ).where(AgentTrace.latency_ms > 0)
    )
    avg_lat, p50_lat, p95_lat = latency_row.one()

    finished = completed_runs + error_runs
    success_rate = round((completed_runs / finished) * 100, 1) if finished else 100.0

    return {
        "service": "ai-content-factory",
        "collected_at": now.isoformat(),
        "total_runs": total_runs,
        "completed_runs": completed_runs,
        "error_runs": error_runs,
        "hitl_wait_runs": hitl_runs,
        "runs_last_7d": runs_last_7d,
        "invited_users": invited_users,
        "invite_codes_issued": invite_codes_issued,
        "success_rate_pct": success_rate,
        "avg_pipeline_cost_usd": round(total_cost_usd / total_runs, 4) if total_runs else 0.0,
        "total_cost_usd": round(total_cost_usd, 4),
        "avg_node_latency_ms": int(avg_lat) if avg_lat else None,
        "p50_node_latency_ms": int(p50_lat) if p50_lat else None,
        "p95_node_latency_ms": int(p95_lat) if p95_lat else None,
        "slo": {
            "target_uptime_pct": SLO_TARGET_UPTIME_PCT,
            "pipeline_success_target_pct": SLO_PIPELINE_SUCCESS_TARGET_PCT,
            "pipeline_success_meets_slo": success_rate >= SLO_PIPELINE_SUCCESS_TARGET_PCT,
        },
    }


async def _scalar(db: AsyncSession, stmt) -> int:
    result = await db.execute(stmt)
    return int(result.scalar_one() or 0)
