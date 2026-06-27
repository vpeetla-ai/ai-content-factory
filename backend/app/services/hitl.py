"""HITL Service — human review interrupt handler."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis import get_redis
from app.core.redis_keys import HITL_PENDING
from app.models import ContentDraft, PipelineRun, PipelineStatus
from app.services.pipeline import PipelineService


class HITLService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.pipeline = PipelineService(db)

    async def get_review(self, run_id: uuid.UUID) -> dict | None:
        result = await self.db.execute(select(PipelineRun).where(PipelineRun.id == run_id))
        run = result.scalar_one_or_none()
        if not run:
            return None

        drafts_result = await self.db.execute(
            select(ContentDraft).where(ContentDraft.run_id == run_id)
        )
        drafts = drafts_result.scalars().all()

        return {
            "run_id": run.id,
            "status": run.status,
            "drafts": [
                {
                    "id": str(d.id),
                    "platform": d.platform.value,
                    "draft_content": d.draft_content,
                    "edited_content": d.edited_content,
                    "seo_keywords": d.seo_keywords,
                    "hashtags": d.hashtags,
                    "hook_variant": d.hook_variant,
                    "char_count": d.char_count,
                }
                for d in drafts
            ],
        }

    async def approve(
        self,
        run: PipelineRun,
        decisions: list[dict],
        user_id: uuid.UUID,
    ) -> PipelineRun:
        hitl_approved: dict = {}
        hitl_edits: dict = {}

        for decision in decisions:
            platform_str = decision["platform"]
            if hasattr(platform_str, "value"):
                platform_str = platform_str.value
            hitl_approved[platform_str] = {
                "approved": decision.get("approved", True),
                "skip": decision.get("skip", False),
            }
            if decision.get("edited_content"):
                hitl_edits[platform_str] = decision["edited_content"]

                from app.models import Platform

                draft_result = await self.db.execute(
                    select(ContentDraft).where(
                        ContentDraft.run_id == run.id,
                        ContentDraft.platform == Platform(platform_str),
                    )
                )
                draft = draft_result.scalar_one_or_none()
                if draft:
                    draft.edited_content = decision["edited_content"]
                    draft.approved_by = user_id

        redis = get_redis()
        await redis.delete(HITL_PENDING.format(run_id=str(run.id)))

        return await self.pipeline.resume_after_hitl(run, hitl_approved, hitl_edits)

    async def reject(self, run: PipelineRun) -> PipelineRun:
        run.status = PipelineStatus.error
        run.state_snapshot = {**(run.state_snapshot or {}), "error": "Rejected by reviewer"}
        run.completed_at = datetime.now(UTC)
        redis = get_redis()
        await redis.delete(HITL_PENDING.format(run_id=str(run.id)))
        await self.db.flush()
        return run
