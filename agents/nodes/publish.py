"""Publisher Agent — platform API adapters."""

from agents.observability import observe_node
from agents.state import ContentFactoryState


@observe_node("publish")
async def publisher_agent(state: ContentFactoryState) -> dict:
    """Publish approved content to connected platforms.

    In dev mode, simulates publish and returns mock post IDs.
    Production: delegates to Publisher Service adapters.
    """
    approved = state.get("hitl_approved") or {}
    edits = state.get("hitl_edits") or {}
    drafts = state.get("platform_drafts") or {}
    results: dict[str, dict] = {}

    for platform, draft_data in drafts.items():
        decision = approved.get(platform, {})
        if decision.get("skip") or not decision.get("approved", True):
            continue

        content = edits.get(platform) or draft_data.get("content", "")
        # Simulated publish — replace with real adapters in publisher service
        results[platform] = {
            "post_id": f"mock_{platform}_{state.get('run_id', 'unknown')[:8]}",
            "url": f"https://{platform}.example/post/mock",
            "content_preview": content[:100],
        }

    return {"published_results": results, "error": None}
