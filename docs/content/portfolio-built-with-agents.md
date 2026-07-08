# Building venkat-ai.com with AI Agents — Meta Case Study

How the portfolio site was built using agentic engineering discipline.

## Approach

1. **Context files first** — `CONTEXT.md`, `AGENTS.md`, org skills (`vpeetla-ai-skills`) ground every agent session
2. **Architectural control** — human reviews ADRs and status tables; agents implement within boundaries
3. **Honest status** — every repo exposes what is production vs stub
4. **Eval gates** — golden-eval-registry prevents demo drift

## Agent workflow

```text
PROFILE / CONTEXT → Cursor or Codex with org skills
                 → Surgical diffs (agentic-engineering skill)
                 → pytest / golden eval CI
                 → Deploy Vercel + Render
```

## Context grounding

| File | Purpose |
|------|---------|
| `CONTEXT.md` | Shared vocabulary, demo URLs, integration rules |
| `AGENTS.md` | Karpathy discipline, stack awareness |
| `.cursor/skills/*` | Task routing (gateway, LangGraph, deploy) |
| `docs/PRODUCT.md` | Who we serve, trade-offs, success metrics |

## Outcomes

- **16 live demos** across the org stack
- **20+ ADRs** documenting rejected alternatives
- **Public ops metrics** — `/api/v1/ops/metrics` proves production thinking
- **5-night velocity** — portfolio reskin + diagram sync (Jul 2026)

## Lesson for Principal interviews

> AI agents are accelerators, not architects. The value is in **decision records**, **governance boundaries**, and **measurable SLOs** — not line count.

## Related

- [venkat-ai-portfolio](https://github.com/vpeetla-ai/venkat-ai-portfolio)
- [ai-architecture-portfolio](https://github.com/vpeetla-ai/ai-architecture-portfolio)
- [PORTFOLIO_GRADE_A.md](../PORTFOLIO_GRADE_A.md)
