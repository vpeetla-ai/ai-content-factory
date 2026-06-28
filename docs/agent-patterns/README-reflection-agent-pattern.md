# Reflection Agent Pattern

[![Part of Production Agent Patterns](https://img.shields.io/badge/series-Production%20Agent%20Patterns-purple)](https://github.com/vpeetla-ai/reflection-agent-pattern)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Part 2 of 5** in the [Production Agent Patterns](https://github.com/vpeetla-ai/react-agent-pattern) series.

Production-grade reference implementation of the **Reflection** pattern for accuracy-critical generation, code review, content validation, and complex reasoning workflows.

| # | Pattern | Repository | Use when |
|---|---------|------------|----------|
| 1 | ReAct | [react-agent-pattern](https://github.com/vpeetla-ai/react-agent-pattern) | Tool use + reasoning loops |
| 2 | **Reflection** | **this repo** | Self-critique and improve output |
| 3 | Plan-Execute | [plan-execute-agent-pattern](https://github.com/vpeetla-ai/plan-execute-agent-pattern) | Decompose goals into steps |
| 4 | Multi-Agent | [multi-agent-system-pattern](https://github.com/vpeetla-ai/multi-agent-system-pattern) | Specialized role delegation |
| 5 | Swarm | [swarm-agent-pattern](https://github.com/vpeetla-ai/swarm-agent-pattern) | Parallel autonomous agents |

[📖 Full series roadmap](https://github.com/vpeetla-ai/ai-content-factory/blob/main/docs/agent-patterns/ROADMAP.md) · [🚀 See in production — AI Content Factory](https://github.com/vpeetla-ai/ai-content-factory)

---

## What you'll learn

- **Draft → critique → improve → finalize** loop
- Quality gates with score thresholds and retry limits
- Independent generator and critic interfaces
- Structured review findings for logging, UI, and evaluation

## What this repo demonstrates

- Draft, critique, improve, and finalize loop
- Quality gates with score thresholds and retry limits
- Independent generator and critic interfaces
- Structured review findings that can be logged, displayed, or used for evaluation

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m reflection_agent_pattern
pytest
```

Runs without API keys using deterministic generator and critic stubs.

```bash
cp .env.example .env
```

See [docs/LOCAL_DEVELOPMENT.md](docs/LOCAL_DEVELOPMENT.md) for production setup.

## Repo layout

```text
src/reflection_agent_pattern/
  __main__.py
  reflection.py
  models.py
  policy.py
docs/ARCHITECTURE.md
tests/test_reflection.py
```

## Related

- **Previous:** [ReAct Agent Pattern](https://github.com/vpeetla-ai/react-agent-pattern)
- **Next:** [Plan-Execute Agent Pattern](https://github.com/vpeetla-ai/plan-execute-agent-pattern)
- **Full pipeline:** [AI Content Factory](https://github.com/vpeetla-ai/ai-content-factory)

⭐ Star the repo if this pattern helps your work.
