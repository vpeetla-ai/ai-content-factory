# ReAct Agent Pattern

[![Part of Production Agent Patterns](https://img.shields.io/badge/series-Production%20Agent%20Patterns-purple)](https://github.com/vpeetla-ai/react-agent-pattern)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Part 1 of 5** in the [Production Agent Patterns](https://github.com/vpeetla-ai/react-agent-pattern) series.

Production-grade reference implementation of the **ReAct (Reason + Act)** pattern for tool-using assistants, retrieval workflows, API copilots, and enterprise Q&A.

| # | Pattern | Repository | Use when |
|---|---------|------------|----------|
| 1 | **ReAct** | **this repo** | Tool use + reasoning loops |
| 2 | Reflection | [reflection-agent-pattern](https://github.com/vpeetla-ai/reflection-agent-pattern) | Self-critique and improve output |
| 3 | Plan-Execute | [plan-execute-agent-pattern](https://github.com/vpeetla-ai/plan-execute-agent-pattern) | Decompose goals into steps |
| 4 | Multi-Agent | [multi-agent-system-pattern](https://github.com/vpeetla-ai/multi-agent-system-pattern) | Specialized role delegation |
| 5 | Swarm | [swarm-agent-pattern](https://github.com/vpeetla-ai/swarm-agent-pattern) | Parallel autonomous agents |

[📖 Full series roadmap](https://github.com/vpeetla-ai/ai-content-factory/blob/main/docs/agent-patterns/ROADMAP.md) · [🚀 See in production — AI Content Factory](https://github.com/vpeetla-ai/ai-content-factory)

---

## What you'll learn

- Explicit **thought → action → observation** loop with bounded iterations
- Tool contracts with schema-light validation and deterministic tests
- Stop conditions that prevent hallucination loops and runaway cost
- Clean separation: model reasoning, tool execution, orchestration, audit traces

## What this repo demonstrates

- Explicit thought/action/observation loop with bounded iterations
- Tool contracts with schema-light validation and deterministic tests
- Stop conditions that prevent hallucination loops and runaway cost
- Separation between model reasoning, tool execution, orchestration, and audit traces

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m react_agent_pattern
pytest
```

The default demo uses a deterministic model stub so the architecture can be tested **without external API keys**.

```bash
cp .env.example .env
```

For LLM keys, database config, and production adapters, see [docs/LOCAL_DEVELOPMENT.md](docs/LOCAL_DEVELOPMENT.md).

## Repo layout

```text
src/react_agent_pattern/
  __main__.py       # CLI demo
  agent.py          # ReAct orchestration loop
  models.py         # Model protocol + deterministic demo model
  tools.py          # Tool interface and sample tools
  tracing.py        # Structured trace events
docs/
  ARCHITECTURE.md   # Architect-level design decision record
tests/
  test_react_agent.py
```

## Production mapping

Replace `ScriptedReasoningModel` with an LLM gateway that supports tool-call structured output. Keep boundaries intact: the agent should not know vendor SDK details, and tools should remain independently testable.

## Related

- **Next in series:** [Reflection Agent Pattern](https://github.com/vpeetla-ai/reflection-agent-pattern)
- **Full pipeline:** [AI Content Factory](https://github.com/vpeetla-ai/ai-content-factory) — multi-agent content orchestration with HITL

If this helped you, ⭐ the repo — and star the [series](https://github.com/vpeetla-ai) to follow new patterns.
