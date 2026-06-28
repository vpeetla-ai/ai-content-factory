"""Pipeline REST routes — /api/v1/pipelines"""

import asyncio
import json
import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sse_starlette.sse import EventSourceResponse

from app.core.database import get_db
from app.core.pipeline_events import subscribe_pipeline_events
from app.core.rate_limit import check_rate_limit
from app.core.security import get_current_user
from app.models import PipelineRun, User
from app.schemas import PipelineRunRequest, PipelineRunResponse, PipelineStateResponse, PipelineStatusEnum
from app.services.pipeline import PipelineService, _execute_pipeline_background

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/pipelines", tags=["Pipeline"])


@router.post("/run", response_model=PipelineRunResponse, status_code=status.HTTP_201_CREATED)
async def start_pipeline(
    body: PipelineRunRequest,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    await check_rate_limit(str(user.id))
    service = PipelineService(db)
    platforms = [p.value for p in body.platforms]
    run = await service.create_run(user.id, body.topic, platforms, body.config)
    run.state_snapshot = {"platforms": platforms, "config": body.config or {}}
    await db.flush()

    task = asyncio.create_task(_execute_pipeline_background(run.id))

    def _log_task_result(t: asyncio.Task) -> None:
        if t.cancelled():
            return
        exc = t.exception()
        if exc:
            logger.exception("Background pipeline %s failed", run.id, exc_info=exc)

    task.add_done_callback(_log_task_result)

    return PipelineRunResponse(
        run_id=run.id,
        status=PipelineStatusEnum(run.status.value),
        topic=run.topic,
        started_at=run.started_at,
    )


@router.get("/{run_id}", response_model=PipelineStateResponse)
async def get_pipeline(
    run_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(
        select(PipelineRun).where(PipelineRun.id == run_id, PipelineRun.user_id == user.id)
    )
    run = result.scalar_one_or_none()
    if not run:
        raise HTTPException(status_code=404, detail="Pipeline run not found")

    state = run.state_snapshot or {}
    return PipelineStateResponse(
        run_id=run.id,
        status=PipelineStatusEnum(run.status.value),
        topic=run.topic,
        research_brief=state.get("research_brief"),
        platform_drafts=state.get("platform_drafts"),
        seo_data=state.get("seo_data"),
        image_prompts=state.get("image_prompts"),
        hitl_approved=state.get("hitl_approved"),
        published_results=state.get("published_results"),
        error=state.get("error"),
    )


@router.get("/{run_id}/stream")
async def stream_pipeline(
    run_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(
        select(PipelineRun).where(PipelineRun.id == run_id, PipelineRun.user_id == user.id)
    )
    run = result.scalar_one_or_none()
    if not run:
        raise HTTPException(status_code=404, detail="Pipeline run not found")

    run_id_str = str(run_id)

    async def event_generator():
        try:
            async for item in subscribe_pipeline_events(run_id_str):
                yield {
                    "event": item.get("event", "message"),
                    "data": json.dumps(item.get("data", {})),
                }
                if item.get("event") in ("pipeline:status", "pipeline:error", "hitl:ready"):
                    if item.get("event") != "hitl:ready":
                        break
        except asyncio.CancelledError:
            return

    return EventSourceResponse(event_generator())


@router.delete("/{run_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_pipeline(
    run_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(
        select(PipelineRun).where(PipelineRun.id == run_id, PipelineRun.user_id == user.id)
    )
    run = result.scalar_one_or_none()
    if not run:
        raise HTTPException(status_code=404, detail="Pipeline run not found")
    await PipelineService(db).cancel_run(run)


@router.get("", response_model=list[PipelineRunResponse])
async def list_pipelines(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    result = await db.execute(
        select(PipelineRun)
        .where(PipelineRun.user_id == user.id)
        .order_by(PipelineRun.started_at.desc())
        .offset(offset)
        .limit(limit)
    )
    runs = result.scalars().all()
    return [
        PipelineRunResponse(
            run_id=r.id,
            status=PipelineStatusEnum(r.status.value),
            topic=r.topic,
            started_at=r.started_at,
        )
        for r in runs
    ]
