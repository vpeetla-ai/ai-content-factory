# Swarm Agent Pattern

[![Part of Production Agent Patterns](https://img.shields.io/badge/series-Production%20Agent%20Patterns-purple)](https://github.com/vpeetla-ai/swarm-agent-pattern)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Part 5 of 5** in the [Production Agent Patterns](https://github.com/vpeetla-ai/react-agent-pattern) series.

Production-grade reference implementation of the **Swarm** pattern — parallel autonomous agents with coordination, aggregation, and conflict resolution.

| # | Pattern | Repository | Use when |
|---|---------|------------|----------|
| 1 | ReAct | [react-agent-pattern](https://github.com/vpeetla-ai/react-agent-pattern) | Tool use + reasoning loops |
| 2 | Reflection | [reflection-agent-pattern](https://github.com/vpeetla-ai/reflection-agent-pattern) | Self-critique and improve output |
| 3 | Plan-Execute | [plan-execute-agent-pattern](https://github.com/vpeetla-ai/plan-execute-agent-pattern) | Decompose goals into steps |
| 4 | Multi-Agent | [multi-agent-system-pattern](https://github.com/vpeetla-ai/multi-agent-system-pattern) | Specialized role delegation |
| 5 | **Swarm** | **this repo** | Parallel autonomous agents |

[📖 Full series roadmap](https://github.com/vpeetla-ai/ai-content-factory/blob/main/docs/agent-patterns/ROADMAP.md) · [🚀 See in production — AI Content Factory](https://github.com/vpeetla-ai/ai-content-factory)

---

## What you'll learn

- Spawn **parallel workers** on subtasks
- Coordinate results without central bottleneck
- Handle duplicate/conflicting outputs
- Cost and concurrency guardrails for production

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m swarm_agent_pattern
pytest
```

Runs without external API keys using deterministic stubs.

```bash
cp .env.example .env
```

See [docs/LOCAL_DEVELOPMENT.md](docs/LOCAL_DEVELOPMENT.md) and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Series complete?

You now have all five core patterns. Compose them in **[AI Content Factory](https://github.com/vpeetla-ai/ai-content-factory)** — research RAG, parallel enrich, HITL gate, multi-platform publish.

[▶ Live demo](https://ai-content-factory-iota.vercel.app)

## Related

- **Previous:** [Multi-Agent System Pattern](https://github.com/vpeetla-ai/multi-agent-system-pattern)
- **Enterprise RAG:** [enterprise_rag_platform](https://github.com/vpeetla-ai/enterprise_rag_platform)

⭐ Star the repo — and the full [series](https://github.com/vpeetla-ai) — if this helped.
