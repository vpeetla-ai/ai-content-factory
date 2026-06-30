"""MCP-style tool bridge — allowlisted tools for research and publish agents.

Enterprise pattern: agents call tools through a registry, not raw HTTP/shell.
Pairs with AegisAI gateway for side-effecting tools (publish.*).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Awaitable


ToolHandler = Callable[..., Awaitable[Any]]


@dataclass
class MCPTool:
    name: str
    description: str
    side_effect: bool = False
    handler: ToolHandler | None = None


@dataclass
class MCPBridge:
    """In-process MCP bridge (v1). Upgrade to stdio MCP server for multi-editor use."""

    tools: dict[str, MCPTool] = field(default_factory=dict)

    def register(self, tool: MCPTool) -> None:
        self.tools[tool.name] = tool

    def list_tools(self) -> list[dict[str, str]]:
        return [
            {"name": t.name, "description": t.description, "side_effect": str(t.side_effect)}
            for t in self.tools.values()
        ]

    async def invoke(self, name: str, **kwargs: Any) -> Any:
        tool = self.tools.get(name)
        if not tool or not tool.handler:
            raise KeyError(f"Unknown MCP tool: {name}")
        return await tool.handler(**kwargs)


def default_content_factory_bridge() -> MCPBridge:
    """Read-only research tools — publish goes through PublisherService + gateway."""

    bridge = MCPBridge()

    async def search_research_cache(topic: str) -> dict:
        return {"topic": topic, "hits": [], "source": "vector_store_stub"}

    async def read_style_guide(platform: str) -> dict:
        guides = {
            "linkedin": "Professional tone, 1-3 short paragraphs, CTA at end.",
            "x": "Under 280 chars, hook first line, one hashtag max.",
        }
        return {"platform": platform, "guide": guides.get(platform, "Clear, concise.")}

    bridge.register(MCPTool("search_research_cache", "Search prior research briefs", side_effect=False, handler=search_research_cache))
    bridge.register(MCPTool("read_style_guide", "Platform style guide for drafts", side_effect=False, handler=read_style_guide))
    return bridge
