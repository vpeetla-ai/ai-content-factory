"""LangGraph ContentFactoryState — per architecture LLD tab."""

from typing import Annotated, TypedDict

from langgraph.graph.message import add_messages


class ContentFactoryState(TypedDict, total=False):
    # Input
    topic: str
    platforms: list[str]
    config: dict

    # Agent outputs
    research_brief: str | None
    platform_drafts: dict | None  # {linkedin, substack, medium, x, instagram}
    image_prompts: list[str] | None
    seo_data: dict | None  # {keywords, hooks, hashtags}

    # HITL
    hitl_approved: dict | None
    hitl_edits: dict | None

    # Publish
    published_results: dict | None  # {platform: post_id}

    # Meta
    error: str | None
    run_id: str
    trace_id: str | None
    messages: Annotated[list, add_messages]
