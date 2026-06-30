# MCP — Content Factory Tool Layer

## Architecture decision

Content Factory agents use an **in-process MCP bridge** (`agents/mcp/bridge.py`) as the tool-access layer per [ADR-007](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/adr/ADR-007-2026-agent-protocol-stack.md).

| Tool class | Examples | Governance |
|------------|----------|------------|
| Read-only | `search_research_cache`, `read_style_guide` | No gateway |
| Side effects | `publish.*` | **AegisAI gateway** via `PublisherService` |

## Why not raw API calls in graph nodes?

- **Auditability** — tool registry lists what agents can invoke
- **Testability** — mock bridge in pytest without network
- **Editor portability** — same tool names for Cursor MCP servers later

## Roadmap

1. ✅ In-process bridge (this repo)
2. 🟡 Stdio MCP server exposing research tools
3. ❌ Gateway-wrapped MCP publish tool registration in AegisAI

## Usage

```python
from agents.mcp.bridge import default_content_factory_bridge

bridge = default_content_factory_bridge()
guide = await bridge.invoke("read_style_guide", platform="linkedin")
```

Publish remains in `backend/app/services/publisher.py` with `authorize_publish()`.
