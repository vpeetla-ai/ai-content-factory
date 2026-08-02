"""Upload PNG cards for visual prompts when R2 is configured."""

from __future__ import annotations

import logging
from typing import Any

from app.services.media_cards import card_object_key, render_prompt_card_png
from app.services.media_store import r2_configured, upload_bytes

logger = logging.getLogger(__name__)


async def materialize_media_assets(
    *,
    run_id: str,
    topic: str,
    prompts: list[str],
    limit: int = 3,
) -> list[dict[str, Any]]:
    """Return media asset dicts; empty when R2 unset or upload fails."""
    if not r2_configured():
        return []
    assets: list[dict[str, Any]] = []
    for i, prompt in enumerate(list(prompts or [])[:limit]):
        if not str(prompt).strip():
            continue
        key = card_object_key(run_id or "local", str(prompt), i, ext="png")
        body = render_prompt_card_png(topic=topic, prompt=str(prompt), index=i)
        obj = await upload_bytes(key, body, content_type="image/png")
        if obj is None:
            logger.info("media_card_skipped index=%s (upload failed or unset)", i)
            continue
        assets.append(
            {
                "key": obj.key,
                "url": obj.public_url,
                "content_type": obj.content_type,
                "prompt": str(prompt)[:300],
                "index": i,
            }
        )
    return assets
