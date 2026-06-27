"""HITL REST routes — /api/v1/hitl"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import PipelineRun, User
from app.schemas import HITLApproveRequest, HITLReviewResponse, PipelineStatusEnum
from app.services.hitl import HITLService

router = APIRouter(prefix="/hitl", tags=["HITL"])


@router.get("/{run_id}/review", response_model=HITLReviewResponse)
async def get_review(
    run_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(
        select(PipelineRun).where(PipelineRun.id == run_id, PipelineRun.user_id == user.id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Pipeline run not found")

    review = await HITLService(db).get_review(run_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    return HITLReviewResponse(
        run_id=review["run_id"],
        status=PipelineStatusEnum(review["status"].value),
        drafts=review["drafts"],
    )


@router.post("/{run_id}/approve")
async def approve_review(
    run_id: UUID,
    body: HITLApproveRequest,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(
        select(PipelineRun).where(PipelineRun.id == run_id, PipelineRun.user_id == user.id)
    )
    run = result.scalar_one_or_none()
    if not run:
        raise HTTPException(status_code=404, detail="Pipeline run not found")

    decisions = [d.model_dump() for d in body.decisions]
    for d in decisions:
        d["platform"] = d["platform"].value if hasattr(d["platform"], "value") else d["platform"]

    updated = await HITLService(db).approve(run, decisions, user.id)
    return {"run_id": str(updated.id), "status": updated.status.value}


@router.post("/{run_id}/reject")
async def reject_review(
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

    updated = await HITLService(db).reject(run)
    return {"run_id": str(updated.id), "status": updated.status.value}
