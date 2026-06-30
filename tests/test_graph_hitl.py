"""Tests for LangGraph pipeline structure and HITL behavior."""

from __future__ import annotations

import pytest

from agents.graph import build_graph
from agents.mcp.bridge import default_content_factory_bridge
from agents.nodes.hitl import human_review_node
from agents.nodes.publish import publisher_agent
from agents.state import ContentFactoryState


def test_graph_compiles_with_hitl_interrupt():
    graph = build_graph()
    assert graph is not None
    # LangGraph stores interrupt config on compiled graph
    assert "hitl" in str(graph.get_graph().nodes)


@pytest.mark.asyncio
async def test_hitl_node_passes_through_approval(sample_state):
    result = await human_review_node(sample_state)  # type: ignore[arg-type]
    assert result["hitl_approved"] == sample_state["hitl_approved"]
    assert result["hitl_edits"] == {}


@pytest.mark.asyncio
async def test_hitl_node_merges_edits():
    state: ContentFactoryState = {
        "topic": "test",
        "platforms": ["linkedin"],
        "run_id": "r1",
        "hitl_approved": {"linkedin": {"approved": True}},
        "hitl_edits": {"linkedin": "Edited content"},
        "messages": [],
    }
    result = await human_review_node(state)
    assert result["hitl_edits"]["linkedin"] == "Edited content"


@pytest.mark.asyncio
async def test_publish_skips_unapproved_platforms(sample_state):
    sample_state["hitl_approved"] = {
        "linkedin": {"approved": True},
        "x": {"approved": False, "skip": True},
    }
    result = await publisher_agent(sample_state)  # type: ignore[arg-type]
    published = result["published_results"]
    assert "linkedin" in published
    assert "x" not in published


@pytest.mark.asyncio
async def test_publish_uses_hitl_edits_over_draft(sample_state):
    sample_state["hitl_edits"] = {"linkedin": "Human-edited final copy"}
    result = await publisher_agent(sample_state)  # type: ignore[arg-type]
    assert "Human-edited" in result["published_results"]["linkedin"]["content_preview"]


def test_graph_node_order():
    graph = build_graph()
    nodes = list(graph.get_graph().nodes.keys())
    for expected in ("research", "content", "enrich", "hitl", "publish"):
        assert expected in nodes


@pytest.mark.asyncio
async def test_mcp_bridge_lists_read_only_tools():
    bridge = default_content_factory_bridge()
    tools = bridge.list_tools()
    names = {t["name"] for t in tools}
    assert "read_style_guide" in names
    assert "search_research_cache" in names
    guide = await bridge.invoke("read_style_guide", platform="x")
    assert "280" in guide["guide"]
