<!-- Profile README for https://github.com/vpeetla-ai (Overview tab) -->

# Hi, I'm Venkata Peetla — AI Architect

> I build **production-grade multi-agent systems**, **enterprise agent governance**, and **governed RAG** — not demos.

[![Website](https://img.shields.io/badge/Website-venkat--ai.com-blue)](https://venkat-ai.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2)](https://linkedin.com/in/venkata-peetla)
[![Substack](https://img.shields.io/badge/Substack-Subscribe-orange)](https://venkatapeetla.substack.com)
[![Medium](https://img.shields.io/badge/Medium-Articles-black)](https://medium.com/@vpeetla.ai)

---

## Top projects

### [AegisAI — Enterprise Agent Governance](https://github.com/vpeetla-ai/aegisai-enterprise-agent-platform)

**Monitor → Govern → Remediate** — AI Gateway for tool authorization: policy, HITL, signed audit, registry lifecycle, FinOps.

[▶ Live control plane](https://aegisai-enterprise-agent-platform.vercel.app) · Gateway SDK · OPA · FastAPI · Next.js

### [Venkat AI Platform (VAP)](https://github.com/vpeetla-ai/venkat-ai-platform)

**Principal-architect multi-agent OS** — 3 LangGraph orchestrators, **7 RAG strategies** (incl. Enterprise RAG adapter), loop patterns (ReAct · Reflection · Plan-Execute), gateway-wrapped notify.

Chief → parallel specialists → Critic → Slack / Telegram / WhatsApp · pairs with AegisAI

### [AI Content Factory](https://github.com/vpeetla-ai/ai-content-factory)

**Multi-agent content pipeline** — Research → 5 platform drafts → HITL → Publish.

[▶ Live demo](https://ai-content-factory-iota.vercel.app) · LangGraph · Clerk · Render + Vercel

### [Enterprise RAG Platform](https://github.com/vpeetla-ai/enterprise_rag_platform)

**Governed knowledge layer** — access-before-ranking, hybrid retrieval, AegisAI HITL bridge, Qdrant adapter, OTLP export.

### [AegisLoop AgentOps Workbench](https://github.com/vpeetla-ai/aegisloop-agentops-workbench)

**Mission fleets + eval gates** — FinOps estimates, Langfuse spans, VAP delegation, AegisAI human-gated ship, Netlify→FastAPI proxy.

---

## How the stack fits together

```text
What should agents do?     →  Venkat AI Platform (orchestration)
What are agents allowed?   →  AegisAI (gateway, policy, HITL, audit)
What knowledge can they use? → Enterprise RAG (access-aware retrieval)
How do we operate them?    →  AegisLoop (missions, traces, eval gates)
What do they produce?        →  AI Content Factory (governed publish pipeline)
```

| Layer | Repository | What it proves |
|-------|------------|----------------|
| **Agent governance** | [aegisai-enterprise-agent-platform](https://github.com/vpeetla-ai/aegisai-enterprise-agent-platform) | Gateway, registry, RAG HITL, mission ship HITL, deploy HITL |
| **Multi-agent OS** | [venkat-ai-platform](https://github.com/vpeetla-ai/venkat-ai-platform) | 3 orchestrators · 16 intents · RAG lab + Enterprise RAG adapter |
| **Knowledge** | [enterprise_rag_platform](https://github.com/vpeetla-ai/enterprise_rag_platform) | Hybrid retrieval, guardrails, AegisAI bridge, Qdrant + OTLP |
| **AgentOps** | [aegisloop-agentops-workbench](https://github.com/vpeetla-ai/aegisloop-agentops-workbench) | Mission fleets, FinOps, Langfuse, VAP delegation |
| **Content automation** | [ai-content-factory](https://github.com/vpeetla-ai/ai-content-factory) | End-to-end pipeline with human approval before publish |

### Production Agent Patterns (series)

| # | Pattern | Repository | Live in VAP |
|---|---------|------------|-------------|
| 1 | ReAct | [react-agent-pattern](https://github.com/vpeetla-ai/react-agent-pattern) | Deep Research orchestrator |
| 2 | Reflection | [reflection-agent-pattern](https://github.com/vpeetla-ai/reflection-agent-pattern) | Research + Architecture pipelines |
| 3 | Plan-Execute | [plan-execute-agent-pattern](https://github.com/vpeetla-ai/plan-execute-agent-pattern) | Architecture Review orchestrator |
| 4 | Multi-Agent | [multi-agent-system-pattern](https://github.com/vpeetla-ai/multi-agent-system-pattern) | Platform + specialist workers |
| 5 | Swarm | [swarm-agent-pattern](https://github.com/vpeetla-ai/swarm-agent-pattern) | Parallel asyncio bundles |

---

## Currently building

- [x] VAP ↔ AegisAI gateway (notify channels)
- [x] VAP — 3 orchestrators + 7 RAG strategies + Enterprise RAG adapter
- [x] Enterprise RAG ↔ AegisAI HITL bridge + Qdrant adapter
- [x] AegisLoop — FinOps, Langfuse, VAP delegation, gateway ship path
- [ ] AegisAI agent registry → Postgres migration
- [ ] Content Factory + cron pipelines through gateway
- [ ] OAuth publish adapters for AI Content Factory

---

## Writing

- **Substack** — [venkatapeetla.substack.com](https://venkatapeetla.substack.com) — architecture decisions for production AI
- **Medium** — [@vpeetla.ai](https://medium.com/@vpeetla.ai) — agent patterns & RAG governance
- **Essay** — [From Multi-Agent OS to Agent Governance](https://github.com/vpeetla-ai/ai-content-factory/blob/main/docs/content/from-multi-agent-os-to-agent-governance.md) (VAP + AegisAI story)

---

## Connect

- 🌐 [venkat-ai.com](https://venkat-ai.com)
- 💼 [LinkedIn](https://linkedin.com/in/venkata-peetla)
- 📰 [Substack](https://venkatapeetla.substack.com)

If any repo helps you, a ⭐ helps other builders discover it.
