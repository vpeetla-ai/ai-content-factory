"""Cloudflare R2 (S3-compatible) media store.

Configured when R2_ACCOUNT_ID + access keys + R2_PUBLIC_URL are set.
Fail-soft: callers get None / empty when unset so demos stay key-free.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass

from app.core.config import get_settings

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class MediaObject:
    key: str
    public_url: str
    content_type: str


def r2_configured() -> bool:
    settings = get_settings()
    return bool(
        settings.r2_account_id
        and settings.r2_access_key_id
        and settings.r2_secret_access_key
        and settings.r2_public_url
    )


def _s3_client():
    import boto3
    from botocore.config import Config

    settings = get_settings()
    endpoint = f"https://{settings.r2_account_id}.r2.cloudflarestorage.com"
    return boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=settings.r2_access_key_id,
        aws_secret_access_key=settings.r2_secret_access_key,
        region_name="auto",
        config=Config(signature_version="s3v4"),
    )


def _upload_sync(key: str, body: bytes, content_type: str) -> MediaObject | None:
    if not r2_configured():
        return None
    settings = get_settings()
    try:
        client = _s3_client()
        client.put_object(
            Bucket=settings.r2_bucket_name,
            Key=key,
            Body=body,
            ContentType=content_type,
        )
    except Exception as exc:
        logger.warning("r2_upload_failed key=%s err=%s", key, exc)
        return None
    base = settings.r2_public_url.rstrip("/")
    return MediaObject(key=key, public_url=f"{base}/{key}", content_type=content_type)


async def upload_bytes(key: str, body: bytes, content_type: str = "image/svg+xml") -> MediaObject | None:
    """Upload object to R2; returns None when not configured or on failure."""
    return await asyncio.to_thread(_upload_sync, key, body, content_type)
