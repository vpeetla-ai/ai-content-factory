"""Content REST routes — /api/v1/content"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import ContentDraft, PipelineRun, PublishedPost, User
from app.schemas import DraftResponse, DraftUpdateRequest, PublishedResponse

router = APIRouter(prefix="/content", tags=["Content"])


@router.get("/{run_id}/drafts", response_model=list[DraftResponse])
async def get_drafts(
    run_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    run_result = await db.execute(
        select(PipelineRun).where(PipelineRun.id == run_id, PipelineRun.user_id == user.id)
    )
    if not run_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Pipeline run not found")

    result = await db.execute(select(ContentDraft).where(ContentDraft.run_id == run_id))
    return result.scalars().all()


@router.put("/{draft_id}", response_model=DraftResponse)
async def update_draft(
    draft_id: UUID,
    body: DraftUpdateRequest,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(
        select(ContentDraft)
        .join(PipelineRun)
        .where(ContentDraft.id == draft_id, PipelineRun.user_id == user.id)
    )
    draft = result.scalar_one_or_none()
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")

    draft.edited_content = body.edited_content
    draft.char_count = len(body.edited_content)
    await db.flush()
    return draft


@router.get("/{run_id}/published", response_model=list[PublishedResponse])
async def get_published(
    run_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    run_result = await db.execute(
        select(PipelineRun).where(PipelineRun.id == run_id, PipelineRun.user_id == user.id)
    )
    if not run_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Pipeline run not found")

    result = await db.execute(
        select(PublishedPost)
        .join(ContentDraft)
        .where(ContentDraft.run_id == run_id)
    )
    posts = result.scalars().all()
    return [
        PublishedResponse(
            platform=p.platform,
            external_post_id=p.external_post_id,
            post_url=p.post_url,
            published_at=p.published_at,
        )
        for p in posts
    ]
