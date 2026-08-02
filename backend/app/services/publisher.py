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


async def _fetch_media_bytes(url: str) -> bytes | None:
    try:
        async with httpx.AsyncClient(timeout=45.0) as client:
            resp = await client.get(url)
            if resp.status_code >= 400:
                return None
            return resp.content
    except Exception as exc:
        logger.warning("media_fetch_failed url=%s err=%s", url, exc)
        return None


async def _linkedin_register_and_upload(
    client: httpx.AsyncClient,
    *,
    access_token: str,
    person_id: str,
    image_bytes: bytes,
) -> str | None:
    """Register + upload image; return digitalmediaAsset URN or None."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }
    register = await client.post(
        "https://api.linkedin.com/v2/assets?action=registerUpload",
        headers=headers,
        json={
            "registerUploadRequest": {
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "owner": f"urn:li:person:{person_id}",
                "serviceRelationships": [
                    {
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent",
                    }
                ],
            }
        },
    )
    if register.status_code >= 400:
        logger.warning("LinkedIn registerUpload failed: %s", register.text[:300])
        return None
    value = register.json().get("value") or {}
    asset = value.get("asset")
    upload_mech = (value.get("uploadMechanism") or {}).get(
        "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"
    ) or {}
    upload_url = upload_mech.get("uploadUrl")
    if not asset or not upload_url:
        logger.warning("LinkedIn registerUpload missing asset/uploadUrl")
        return None
    put = await client.put(
        upload_url,
        content=image_bytes,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "image/png",
        },
    )
    if put.status_code >= 400:
        logger.warning("LinkedIn media PUT failed: %s", put.text[:300])
        return None
    return str(asset)


class LinkedInAdapter(PlatformAdapter):
    async def publish(self, draft: ContentDraft, token_data: dict) -> dict:
        content = draft.edited_content or draft.draft_content
        media_urls = list(token_data.get("_media_urls") or []) if isinstance(token_data, dict) else []
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

        async with httpx.AsyncClient(timeout=60.0) as client:
            media_urn: str | None = None
            if media_urls:
                image_bytes = await _fetch_media_bytes(str(media_urls[0]))
                if image_bytes:
                    media_urn = await _linkedin_register_and_upload(
                        client,
                        access_token=access_token,
                        person_id=person_id,
                        image_bytes=image_bytes,
                    )
            # Fail-soft: if native upload failed, keep URL in text.
            if media_urls and not media_urn:
                url = str(media_urls[0])
                if url and url not in content:
                    content = f"{content.rstrip()}\n\n{url}"

            share_content: dict = {
                "shareCommentary": {"text": content[:3000]},
                "shareMediaCategory": "NONE",
            }
            if media_urn:
                share_content = {
                    "shareCommentary": {"text": content[:3000]},
                    "shareMediaCategory": "IMAGE",
                    "media": [
                        {
                            "status": "READY",
                            "description": {"text": "AI Content Factory visual"},
                            "media": media_urn,
                            "title": {"text": "Visual"},
                        }
                    ],
                }

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
                    "specificContent": {"com.linkedin.ugc.ShareContent": share_content},
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
            return {
                "external_post_id": post_id,
                "post_url": f"https://linkedin.com/feed/update/{post_id}",
                "media_attached": bool(media_urn),
            }


async def _x_upload_media(client: httpx.AsyncClient, *, access_token: str, image_bytes: bytes) -> str | None:
    """Upload PNG via Twitter media v1.1 endpoint; return media_id_string or None."""
    response = await client.post(
        "https://upload.twitter.com/1.1/media/upload.json",
        headers={"Authorization": f"Bearer {access_token}"},
        files={"media": ("card.png", image_bytes, "image/png")},
    )
    if response.status_code >= 400:
        logger.warning("X media upload failed: %s", response.text[:300])
        return None
    media_id = response.json().get("media_id_string") or response.json().get("media_id")
    return str(media_id) if media_id is not None else None


class XAdapter(PlatformAdapter):
    async def publish(self, draft: ContentDraft, token_data: dict) -> dict:
        content = (draft.edited_content or draft.draft_content)[:280]
        media_urls = list(token_data.get("_media_urls") or []) if isinstance(token_data, dict) else []
        access_token = token_data.get("access_token") or ""
        if not access_token:
            return {
                "external_post_id": f"x_mock_{draft.id}",
                "post_url": "https://x.com/user/status/mock",
            }

        async with httpx.AsyncClient(timeout=60.0) as client:
            media_id: str | None = None
            if media_urls:
                image_bytes = await _fetch_media_bytes(str(media_urls[0]))
                if image_bytes:
                    media_id = await _x_upload_media(
                        client, access_token=access_token, image_bytes=image_bytes
                    )
            if media_urls and not media_id:
                url = str(media_urls[0])
                if url and url not in content:
                    room = max(0, 280 - len(url) - 1)
                    content = f"{content[:room].rstrip()}\n{url}"[:280]

            payload_json: dict = {"text": content}
            if media_id:
                payload_json["media"] = {"media_ids": [media_id]}

            response = await client.post(
                "https://api.twitter.com/2/tweets",
                headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
                json=payload_json,
            )
            if response.status_code >= 400:
                logger.warning("X publish failed: %s", response.text)
                return {
                    "external_post_id": f"x_error_{draft.id}",
                    "post_url": "https://x.com/user/status/error",
                }
            payload = response.json()
            tweet_id = payload.get("data", {}).get("id", f"x_{draft.id}")
            return {
                "external_post_id": tweet_id,
                "post_url": f"https://x.com/i/web/status/{tweet_id}",
                "media_attached": bool(media_id),
            }


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
        if result.get("media_attached"):
            analytics_data = {**(analytics_data or {}), "media_attached": True}
        return PublishedPost(
            draft_id=draft.id,
            platform=draft.platform.value,
            external_post_id=result["external_post_id"] or None,
            post_url=result["post_url"] or None,
            analytics_data=analytics_data,
        )
