"""HITL node — passthrough; interrupt_before pauses graph before this node."""

from agents.state import ContentFactoryState


async def human_review_node(state: ContentFactoryState) -> dict:
    """Merge HITL decisions from external approval into state."""
    return {
        "hitl_approved": state.get("hitl_approved"),
        "hitl_edits": state.get("hitl_edits"),
    }
