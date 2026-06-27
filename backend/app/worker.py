"""Celery worker — publish queue (queue:publish)."""

import asyncio

from uuid import UUID

from celery import Celery
from sqlalchemy import select

from app.core.config import get_settings
from app.core.database import async_session_factory
from app.core.redis_keys import PUBLISH_QUEUE
from app.models import ContentDraft, PublishedPost

settings = get_settings()

celery_app = Celery(
    "acf",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_default_queue="queue:publish",
)


@celery_app.task(name="publish_to_platform")
def publish_to_platform(draft_id: str, platform: str, access_token: str = ""):
    """Process publish job — updates analytics stub on published_posts."""

    async def _run():
        async with async_session_factory() as db:
            result = await db.execute(
                select(ContentDraft).where(ContentDraft.id == UUID(draft_id))
            )
            draft = result.scalar_one_or_none()
            if not draft:
                return {"status": "not_found"}

            pub_result = await db.execute(
                select(PublishedPost).where(PublishedPost.draft_id == draft.id)
            )
            post = pub_result.scalar_one_or_none()
            if post:
                post.analytics_data = {
                    "queue": PUBLISH_QUEUE,
                    "platform": platform,
                    "status": "processed",
                }
            await db.commit()
            return {"draft_id": draft_id, "platform": platform, "status": "processed"}

    return asyncio.run(_run())
