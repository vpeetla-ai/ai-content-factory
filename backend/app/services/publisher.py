"""Publisher Service — platform API adapters with AegisAI gateway authorization."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod

import httpx

from app.integrations.aegis_gateway import authorize_publish
from app.models import ContentDraft, PublishedPost

logger = logging.getLogger(__name__)


class PublishBlockedError(RuntimeError):
    pass


class PlatformAdapter(ABC):
    @abstractmethod
    async def publish(self, draft: ContentDraft, token_data: dict) -> dict:
        """Return {external_post_id, post_url}."""


class LinkedInAdapter(PlatformAdapter):
    async def publish(self, draft: ContentDraft, token_data: dict) -> dict:
        content = draft.edited_content or draft.draft_content
        access_token = token_data.get("access_token") or ""
        person_id = token_data.get("person_id") or ""
        if not access_token:
            return {
                "external_post_id": f"li_mock_{draft.id}",
                "post_url": "https://linkedin.com/feed/update/mock",
            }
        if not person_id:
            logger.warning("LinkedIn publish skipped: missing person_id for draft %s", draft.id)
            return {
                "external_post_id": f"li_error_{draft.id}",
                "post_url": "https://linkedin.com/feed/update/error",
            }
        async with httpx.AsyncClient(timeout=45.0) as client:
            response = await client.post(
                "https://api.linkedin.com/v2/ugcPosts",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json",
                    "X-Restli-Protocol-Version": "2.0.0",
                },
                json={
                    "author": f"urn:li:person:{person_id}",
                    "lifecycleState": "PUBLISHED",
                    "specificContent": {
                        "com.linkedin.ugc.ShareContent": {
                            "shareCommentary": {"text": content[:3000]},
                            "shareMediaCategory": "NONE",
                        }
                    },
                    "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
                },
            )
            if response.status_code >= 400:
                logger.warning("LinkedIn publish failed: %s", response.text)
                return {
                    "external_post_id": f"li_error_{draft.id}",
                    "post_url": "https://linkedin.com/feed/update/error",
                }
            payload = response.json()
            post_id = payload.get("id", f"li_{draft.id}")
            return {"external_post_id": post_id, "post_url": f"https://linkedin.com/feed/update/{post_id}"}


class XAdapter(PlatformAdapter):
    async def publish(self, draft: ContentDraft, token_data: dict) -> dict:
        content = (draft.edited_content or draft.draft_content)[:280]
        access_token = token_data.get("access_token") or ""
        if not access_token:
            return {
                "external_post_id": f"x_mock_{draft.id}",
                "post_url": "https://x.com/user/status/mock",
            }
        async with httpx.AsyncClient(timeout=45.0) as client:
            response = await client.post(
                "https://api.twitter.com/2/tweets",
                headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
                json={"text": content},
            )
            if response.status_code >= 400:
                logger.warning("X publish failed: %s", response.text)
                return {
                    "external_post_id": f"x_error_{draft.id}",
                    "post_url": "https://x.com/user/status/error",
                }
            payload = response.json()
            tweet_id = payload.get("data", {}).get("id", f"x_{draft.id}")
            return {"external_post_id": tweet_id, "post_url": f"https://x.com/i/web/status/{tweet_id}"}


class NotSupportedAdapter(PlatformAdapter):
    """Platform has no viable public posting API today — return the draft for manual copy/paste."""

    post_url_hint: str = ""

    async def publish(self, draft: ContentDraft, token_data: dict) -> dict:
        content = draft.edited_content or draft.draft_content
        return {
            "external_post_id": "",
            "post_url": "",
            "not_supported": True,
            "draft_content": content,
        }


class MediumAdapter(NotSupportedAdapter):
    pass


class SubstackAdapter(NotSupportedAdapter):
    pass


class InstagramAdapter(NotSupportedAdapter):
    pass


ADAPTERS: dict[str, PlatformAdapter] = {
    "linkedin": LinkedInAdapter(),
    "x": XAdapter(),
    "medium": MediumAdapter(),
    "substack": SubstackAdapter(),
    "instagram": InstagramAdapter(),
}


class PublisherService:
    async def publish_draft(
        self,
        draft: ContentDraft,
        token_data: dict | None = None,
        *,
        case_id: str | None = None,
        skip_gateway: bool = False,
    ) -> PublishedPost:
        adapter = ADAPTERS.get(draft.platform.value)
        if not adapter:
            raise ValueError(f"No adapter for platform: {draft.platform}")

        if not skip_gateway:
            authz = await authorize_publish(
                draft.platform.value,
                case_id=case_id or f"publish-{draft.run_id}-{draft.platform.value}",
            )
            if authz.blocked:
                raise PublishBlockedError(authz.reason)
            if authz.requires_approval:
                raise PublishBlockedError(f"Gateway approval required: {authz.case_id}")

        result = await adapter.publish(draft, token_data or {})
        analytics_data = {"not_supported": True, "draft_content": result["draft_content"]} if result.get("not_supported") else None
        return PublishedPost(
            draft_id=draft.id,
            platform=draft.platform.value,
            external_post_id=result["external_post_id"] or None,
            post_url=result["post_url"] or None,
            analytics_data=analytics_data,
        )
