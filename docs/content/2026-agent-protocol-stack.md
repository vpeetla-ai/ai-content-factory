# The 2026 Agent Protocol Stack — Skills, MCP, Gateway, Observability

**By Venkata Peetla** · [GitHub](https://github.com/vpeetla-ai) · [venkat-ai.com](https://venkat-ai.com) · [Substack](https://venkatapeetla.substack.com)

> **ADR:** [ADR-007 Agent Protocol Stack](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/adr/ADR-007-2026-agent-protocol-stack.md)  
> **Org plan:** [ORG_IMPROVEMENT_PLAN_2026](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/docs/ORG_IMPROVEMENT_PLAN_2026.md)

---

In 2024, the conversation was "which LLM?" In 2026, the conversation is **which protocol stack?**

Production agent systems are no longer a single prompt chain. They are:

- **Skills** — how engineers and coding agents develop safely
- **MCP** — how agents access tools
- **Gateway** — what side effects are allowed
- **Observability** — what happened, with eval proof

This essay maps that stack to the [vpeetla-ai](https://github.com/vpeetla-ai) reference implementation — honestly, including what is stub vs live.

---

## Why a stack, not a framework

Frameworks optimize for demos. Enterprises optimize for:

| Question | Protocol layer |
|----------|----------------|
| How do we build consistently? | **Agent Skills** (`SKILL.md`) |
| How do agents call tools? | **MCP** (tool bridge → stdio servers) |
| What may agents do? | **Gateway + HITL** (AegisAI) |
| How do we prove behavior? | **Observability + evals** (Langfuse, OTel, pytest) |

No single vendor ships all four well. Composable protocols win.

---

## Layer 1 — Agent Skills (engineering discipline)

**Repo:** [vpeetla-ai-skills](https://github.com/vpeetla-ai/vpeetla-ai-skills)

Skills are small, versioned instructions — not megaprompts. We install them across 14 repos via `scripts/install.sh` for Cursor (`.cursor/skills/`) and Codex (`AGENTS.md` + `CONTEXT.md`).

| Skill category | Example |
|----------------|---------|
| Stack routing | `governed-ai-stack` |
| Implementation | `langgraph-orchestration`, `aegis-gateway` |
| Credibility | `honest-status-table` |
| Role | `enterprise-ai-architect` |

**2026 trend:** Skill management is the new "lint rules for agents." CI smoke-tests the installer so skills do not rot.

---

## Layer 2 — MCP (tool access)

**Repos:** LoopForge `mcp/bridge.py`, Content Factory `agents/mcp/bridge.py`, VAP [docs/MCP.md](https://github.com/vpeetla-ai/venkat-ai-platform/blob/main/docs/MCP.md)

MCP standardizes *how* tools are discovered and invoked. Our v1 pattern:

```text
Agent node  →  in-process MCPBridge  →  read-only tools (no gateway)
Side effect  →  PublisherService / git_pr_node  →  gateway first
```

| Tool class | Gateway? |
|------------|----------|
| `read_style_guide`, `search_docs` | No |
| `publish.linkedin`, `git.push_branch` | **Yes** |

**Honest gap:** Stdio MCP servers are roadmap — bridges are in-process today. The *contract* is documented; packaging is Phase 3.

---

## Layer 3 — Gateway (governance)

**Repo:** [aegisai-enterprise-agent-platform](https://github.com/vpeetla-ai/aegisai-enterprise-agent-platform)

Every irreversible action should pass `authorize_tool()`:

| System | Side effect | Integration |
|--------|-------------|-------------|
| Content Factory | Social publish | `backend/app/integrations/aegis_gateway.py` |
| LoopForge | Git push + PR | `loop_engine/integrations/aegis_gateway.py` |
| AegisLoop | Mission tools | `integrations/aegis_gateway.py` |

Decisions: `allow` · `approval_required` · `block`

**Production rule:** fail-open in dev (`AEGISAI_GATEWAY_FAIL_OPEN=true`), fail-closed in prod.

---

## Layer 4 — Observability

| Platform | Trace path |
|----------|------------|
| Content Factory | LangSmith + Langfuse + Sentry |
| VAP / AegisLoop | Langfuse optional |
| LoopForge | `trace_events` + Langfuse export on harness |
| Enterprise RAG | Pipeline `EventRecorder` → OTLP planned |

Observability without evals is expensive logging. We pair traces with **pytest** (Content Factory graph/HITL) and golden queries (Enterprise RAG).

---

## The eight application layers (where protocols attach)

```text
Orchestration (VAP)           ← MCP client
Governance (AegisAI)          ← Gateway
Knowledge (Enterprise RAG)    ← Access-before-ranking
AgentOps (AegisLoop)          ← Missions + eval gates
Application (Content Factory) ← HITL publish
Self-improvement (LoopForge)  ← ODAEU + repo-fix PR
Inference (vLLM Lab)          ← Education — pairs with VAP router
Engineering (Skills)          ← This protocol essay's meta-layer
```

---

## Scorecard — what we closed in Phase 2

| Trend | Before | After Phase 2 |
|-------|--------|---------------|
| MCP docs | LoopForge only | + Content Factory, VAP |
| Content Factory pytest | Smoke script | `tests/` graph + HITL + gateway |
| Gateway on git push | Missing | LoopForge push + PR |
| Langfuse on harness | In-process only | Optional export |
| Architecture hubs | ADRs only | Enterprise RAG + AegisLoop `ARCHITECTURE.md` |
| Skills CI | None | `smoke_test.sh` in GitHub Actions |
| Inference story | Isolated lab | VAP `INFERENCE.md` ↔ vLLM lab |

---

## What I'd tell a principal architect interview panel

1. **Separate orchestration from governance** — VAP delegates; AegisAI authorizes.
2. **Document stubs honestly** — pattern repos are teaching units, not faux "production."
3. **Protocol stack > model choice** — Skills + MCP + Gateway + OTel outlive GPT-N.
4. **Evals are product** — if pytest does not cover your graph, you do not have an agent platform.

---

## Try it live

| Demo | URL |
|------|-----|
| Content Factory (HITL publish) | [ai-content-factory-iota.vercel.app](https://ai-content-factory-iota.vercel.app) |
| LoopForge (repo-fix PR) | [demo-omega-taupe.vercel.app](https://demo-omega-taupe.vercel.app) |
| AegisAI gateway | [aegisai-enterprise-agent-platform.vercel.app](https://aegisai-enterprise-agent-platform.vercel.app) |
| vLLM inference lab | [vllm-architecture-lab.vercel.app](https://vllm-architecture-lab.vercel.app) |
| Full portfolio | [venkat-ai.com/work](https://venkat-ai.com/work) |

---

*Building in public at [github.com/vpeetla-ai](https://github.com/vpeetla-ai). Feedback welcome via issues on `ai-architecture-portfolio`.*
