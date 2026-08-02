"""Publisher Agent — select approved platforms for real adapter publish.

The graph node does **not** call LinkedIn/X APIs. It emits publish *intents*
(platform + content preview). ``PipelineService._persist_published`` then runs
``PublisherService`` (AegisAI gateway + real adapters / copy-draft export).
"""

from agents.observability import observe_node
from agents.state import ContentFactoryState


@observe_node("publish")
async def publisher_agent(state: ContentFactoryState) -> dict:
    """Select approved drafts for the post-graph PublisherService path."""
    approved = state.get("hitl_approved") or {}
    edits = state.get("hitl_edits") or {}
    drafts = state.get("platform_drafts") or {}
    results: dict[str, dict] = {}

    for platform, draft_data in drafts.items():
        decision = approved.get(platform, {})
        if decision.get("skip") or not decision.get("approved", True):
            continue

        content = edits.get(platform) or (
            draft_data.get("content", "") if isinstance(draft_data, dict) else str(draft_data)
        )
        results[platform] = {
            "status": "selected",
            "pending_adapter": True,
            "content_preview": content[:100],
            # No fake post URLs — real IDs come from PublisherService adapters.
        }

    return {"published_results": results, "error": None}
