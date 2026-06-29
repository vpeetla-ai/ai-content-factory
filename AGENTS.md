# Agent Instructions — vpeetla-ai org

Read [CONTEXT.md](CONTEXT.md) for shared vocabulary.

## Agentic engineering (Karpathy)

1. **Think before coding** — state assumptions, plan, success criteria
2. **Simplicity first** — minimum diff; no speculative features
3. **Surgical changes** — match existing style; no drive-by refactors
4. **Goal-driven execution** — tests/evals define done; iterate until pass

## Stack awareness

This org builds **governed agent systems**, not chat demos:

- Orchestration (VAP) and governance (AegisAI) are **separate layers**
- RAG uses **access-before-ranking**
- Side effects require **gateway or HITL**
- Self-improvement uses **harness + eval loops** (LoopForge)

## Repo conventions

- Python 3.11+, FastAPI, Pydantic v2, LangGraph for agent graphs
- `pip install -e ".[dev]"` + `pytest -q` before claiming done
- README: badges → problem → 60s diagram → **honest status table** → quick start
- Deploy: Vercel (UI) + Render (API); see `render.yaml`

## Skills repo

Install org skills from [vpeetla-ai-skills](https://github.com/vpeetla-ai/vpeetla-ai-skills):

```bash
./scripts/install.sh --cursor --project .
./scripts/install.sh --codex --project .
```

## When stuck

1. Check which **stack layer** the task belongs to
2. Read the target repo's `docs/ECOSYSTEM.md` or `docs/ARCHITECTURE.md`
3. Use **tdd-agent-loops** for graph changes; **aegis-gateway** for side effects
