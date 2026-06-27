"""Publisher Service — platform API adapters."""

from abc import ABC, abstractmethod

from app.models import ContentDraft, PublishedPost


class PlatformAdapter(ABC):
    @abstractmethod
    async def publish(self, draft: ContentDraft, access_token: str) -> dict:
        """Return {external_post_id, post_url}."""


class LinkedInAdapter(PlatformAdapter):
    async def publish(self, draft: ContentDraft, access_token: str) -> dict:
        # TODO: LinkedIn UGC Posts API v2
        content = draft.edited_content or draft.draft_content
        return {
            "external_post_id": f"li_mock_{draft.id}",
            "post_url": "https://linkedin.com/feed/update/mock",
        }


class XAdapter(PlatformAdapter):
    async def publish(self, draft: ContentDraft, access_token: str) -> dict:
        content = draft.edited_content or draft.draft_content
        return {
            "external_post_id": f"x_mock_{draft.id}",
            "post_url": "https://x.com/user/status/mock",
        }


class MediumAdapter(PlatformAdapter):
    async def publish(self, draft: ContentDraft, access_token: str) -> dict:
        return {
            "external_post_id": f"md_mock_{draft.id}",
            "post_url": "https://medium.com/@user/mock",
        }


class SubstackAdapter(PlatformAdapter):
    async def publish(self, draft: ContentDraft, access_token: str) -> dict:
        return {
            "external_post_id": f"ss_mock_{draft.id}",
            "post_url": "https://substack.com/p/mock",
        }


class InstagramAdapter(PlatformAdapter):
    async def publish(self, draft: ContentDraft, access_token: str) -> dict:
        return {
            "external_post_id": f"ig_mock_{draft.id}",
            "post_url": "https://instagram.com/p/mock",
        }


ADAPTERS: dict[str, PlatformAdapter] = {
    "linkedin": LinkedInAdapter(),
    "x": XAdapter(),
    "medium": MediumAdapter(),
    "substack": SubstackAdapter(),
    "instagram": InstagramAdapter(),
}


class PublisherService:
    async def publish_draft(self, draft: ContentDraft, access_token: str = "") -> PublishedPost:
        adapter = ADAPTERS.get(draft.platform.value)
        if not adapter:
            raise ValueError(f"No adapter for platform: {draft.platform}")

        result = await adapter.publish(draft, access_token)
        return PublishedPost(
            draft_id=draft.id,
            platform=draft.platform.value,
            external_post_id=result["external_post_id"],
            post_url=result["post_url"],
        )
