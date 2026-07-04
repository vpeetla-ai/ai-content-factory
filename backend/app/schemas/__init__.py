"""Pydantic request/response schemas."""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class PlatformEnum(str, Enum):
    linkedin = "linkedin"
    substack = "substack"
    medium = "medium"
    instagram = "instagram"
    x = "x"


class PipelineStatusEnum(str, Enum):
    running = "running"
    hitl_wait = "hitl_wait"
    done = "done"
    error = "error"


# ── Pipeline ───────────────────────────────────────────

class PipelineRunRequest(BaseModel):
    topic: str = Field(..., min_length=3, max_length=500)
    platforms: list[PlatformEnum] = Field(
        default_factory=lambda: list(PlatformEnum)
    )
    config: dict | None = None


class PipelineRunResponse(BaseModel):
    run_id: UUID
    status: PipelineStatusEnum
    topic: str
    started_at: datetime

    model_config = {"from_attributes": True}


class PipelineStateResponse(BaseModel):
    run_id: UUID
    status: PipelineStatusEnum
    topic: str
    research_brief: str | None = None
    platform_drafts: dict | None = None
    seo_data: dict | None = None
    image_prompts: list[str] | None = None
    hitl_approved: dict | None = None
    published_results: dict | None = None
    error: str | None = None


# ── HITL ───────────────────────────────────────────────

class PlatformDecision(BaseModel):
    platform: PlatformEnum
    approved: bool = True
    edited_content: str | None = None
    skip: bool = False


class HITLApproveRequest(BaseModel):
    decisions: list[PlatformDecision]


class HITLReviewResponse(BaseModel):
    run_id: UUID
    status: PipelineStatusEnum
    drafts: list[dict]


# ── Content ────────────────────────────────────────────

class DraftResponse(BaseModel):
    id: UUID
    platform: PlatformEnum
    draft_content: str
    edited_content: str | None
    seo_keywords: list[str] | None
    hashtags: list[str] | None
    hook_variant: str | None
    char_count: int

    model_config = {"from_attributes": True}


class DraftUpdateRequest(BaseModel):
    edited_content: str


class PublishedResponse(BaseModel):
    platform: str
    external_post_id: str | None
    post_url: str | None
    published_at: datetime


# ── Auth ───────────────────────────────────────────────

class TokenRequest(BaseModel):
    clerk_token: str
    invite_code: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserProfileResponse(BaseModel):
    id: UUID
    email: str
    name: str | None
    role: str
    quotas: dict

    model_config = {"from_attributes": True}


