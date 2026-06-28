# Production Agent Patterns — Learning Path

A 5-part reference series for building production AI agents. Each repo runs locally without API keys (deterministic stubs) and maps to real production boundaries.

| # | Pattern | Repository | Use when |
|---|---------|------------|----------|
| 1 | **ReAct** | [react-agent-pattern](https://github.com/vpeetla-ai/react-agent-pattern) | Tool use + reasoning loops |
| 2 | **Reflection** | [reflection-agent-pattern](https://github.com/vpeetla-ai/reflection-agent-pattern) | Self-critique before shipping output |
| 3 | **Plan-Execute** | [plan-execute-agent-pattern](https://github.com/vpeetla-ai/plan-execute-agent-pattern) | Multi-step research and reporting |
| 4 | **Multi-Agent** | [multi-agent-system-pattern](https://github.com/vpeetla-ai/multi-agent-system-pattern) | Specialized role delegation |
| 5 | **Swarm** | [swarm-agent-pattern](https://github.com/vpeetla-ai/swarm-agent-pattern) | Parallel autonomous workers |

## See it in production

These patterns compose in **[AI Content Factory](https://github.com/vpeetla-ai/ai-content-factory)** — a full multi-agent content pipeline with RAG, HITL, and deploy to Render + Vercel.

[▶ Live demo](https://ai-content-factory-iota.vercel.app)

## Suggested reading order

1. Start with **ReAct** — understand thought/action/observation loops
2. Add **Reflection** when output quality matters more than speed
3. Use **Plan-Execute** for long-horizon tasks
4. Graduate to **Multi-Agent** and **Swarm** for team-style orchestration

## Updating READMEs in each repo

Enhanced READMEs are in this folder. Copy to each repository root:

```bash
# From ai-content-factory root, after cloning pattern repos as siblings:
./scripts/apply-agent-pattern-readmes.sh
```

Or copy manually from `docs/agent-patterns/README-<repo-name>.md` → `<repo>/README.md`.
