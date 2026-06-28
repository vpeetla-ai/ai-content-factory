"""Scheduled pipeline triggers (Mon/Thu content radar by default)."""

from __future__ import annotations

import logging
import uuid
from datetime import UTC, datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import select

from app.core.config import get_settings
from app.core.database import async_session_factory
from app.integrations.aegis_gateway import authorize_tool
from app.models import User
from app.services.pipeline import PipelineService, _execute_pipeline_background

logger = logging.getLogger(__name__)
_scheduler: AsyncIOScheduler | None = None


async def _run_scheduled_pipeline() -> None:
    settings = get_settings()
    if not settings.cron_pipeline_enabled:
        return

    case_id = f"cron-{datetime.now(UTC).strftime('%Y%m%d%H%M')}"
    authz = await authorize_tool(
        tool_name="publish.linkedin",
        action_type="schedule_pipeline",
        target_system="ai-content-factory",
        case_id=case_id,
        customer_impact=False,
    )
    if authz.blocked:
        logger.warning("Scheduled pipeline blocked by gateway: %s", authz.reason)
        return
    if authz.requires_approval:
        logger.info("Scheduled pipeline paused for gateway approval: %s", authz.case_id)
        return

    async with async_session_factory() as db:
        result = await db.execute(select(User).where(User.email == settings.cron_user_email))
        user = result.scalar_one_or_none()
        if not user:
            logger.warning("Cron user not found: %s", settings.cron_user_email)
            return
        service = PipelineService(db)
        run = await service.create_run(
            user.id,
            topic=settings.cron_topic,
            platforms=settings.cron_platform_list(),
            config={"source": "cron", "gateway_case_id": case_id},
        )
        await db.commit()
        run_id = run.id

    import asyncio

    asyncio.create_task(_execute_pipeline_background(run_id))
    logger.info("Scheduled pipeline started", extra={"run_id": str(run_id), "case_id": case_id})


def start_cron_scheduler() -> AsyncIOScheduler | None:
    global _scheduler
    settings = get_settings()
    if not settings.cron_pipeline_enabled:
        return None
    if _scheduler is not None:
        return _scheduler

    scheduler = AsyncIOScheduler(timezone="UTC")
    trigger = CronTrigger.from_crontab(settings.cron_schedule)
    scheduler.add_job(_run_scheduled_pipeline, trigger, id="content-factory-cron", replace_existing=True)
    scheduler.start()
    _scheduler = scheduler
    logger.info("Cron scheduler started", extra={"schedule": settings.cron_schedule})
    return scheduler


def shutdown_cron_scheduler() -> None:
    global _scheduler
    if _scheduler is not None:
        _scheduler.shutdown(wait=False)
        _scheduler = None
