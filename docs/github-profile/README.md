<!-- Profile README for https://github.com/vpeetla-ai (Overview tab) -->

# Hi, I'm Venkata Peetla — Principal AI Architect

> I build **self-improving agent systems** — loop engineering, harness, MCP tools, RAG tuning, memory, and **repo fix → PR** — with **11 live demos** you can inspect before we talk.

[![Website](https://img.shields.io/badge/Website-venkat--ai.com-blue)](https://venkat-ai.com)
[![Architecture Portfolio](https://img.shields.io/badge/Architecture_Portfolio-Case_Studies_%26_ADRs-5eead4)](https://github.com/vpeetla-ai/ai-architecture-portfolio)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2)](https://linkedin.com/in/venkata-peetla)
[![Substack](https://img.shields.io/badge/Substack-Subscribe-orange)](https://venkatapeetla.substack.com)

---

## Architecture portfolio

**[ai-architecture-portfolio](https://github.com/vpeetla-ai/ai-architecture-portfolio)** — case studies, ADRs, trade-offs, and stack map (Nic Chin–style architecture hub).

→ [Featured case studies & decisions](https://github.com/vpeetla-ai/ai-architecture-portfolio#featured-case-studies) · [Live demos](https://venkat-ai.com/work)

---

## Agent skills (Cursor + Codex)

**[vpeetla-ai-skills](https://github.com/vpeetla-ai/vpeetla-ai-skills)** — org-wide agent skills for every repo: LangGraph, gateway/HITL, loop engineering, TDD, deploy.

```bash
git clone https://github.com/vpeetla-ai/vpeetla-ai-skills.git
./vpeetla-ai-skills/scripts/install.sh --cursor --codex --project .
```

Inspired by [mattpocock/skills](https://github.com/mattpocock/skills) + [Karpathy agentic engineering](https://www.youtube.com/watch?v=96jN2OCOfLs).

---

## Top projects

### [LoopForge — Self-Improving Agent Harness](https://github.com/vpeetla-ai/loop-engine-agent-platform) · **LIVE**

**Agent → Harness → Loops → Memory** — LangGraph coding loop (Orchestrator · Review · Quality), ODAEU RAG tuning, **real repo bug-fix → GitHub PR** (never pushes to `main`).

[▶ Live demo](https://demo-omega-taupe.vercel.app) · [API](https://loopforge-api.onrender.com/health) · LangGraph · MCP · Groq · GitHub PR workflow

### [AegisAI — Enterprise Agent Governance](https://github.com/vpeetla-ai/aegisai-enterprise-agent-platform)

**Monitor → Govern → Remediate** — AI Gateway for tool authorization: policy, HITL, signed audit, registry lifecycle, FinOps.

[▶ Live control plane](https://aegisai-enterprise-agent-platform.vercel.app) · Gateway SDK · OPA · FastAPI · Next.js

### [Venkat AI Platform (VAP)](https://github.com/vpeetla-ai/venkat-ai-platform)

**Principal-architect multi-agent OS** — 3 LangGraph orchestrators, **7 RAG strategies** (incl. Enterprise RAG adapter), loop patterns (ReAct · Reflection · Plan-Execute), gateway-wrapped notify.

Chief → parallel specialists → Critic → Slack / Telegram / WhatsApp · pairs with AegisAI

[▶ Live demo](https://venkat-ai-platform.vercel.app)

### [AI Content Factory](https://github.com/vpeetla-ai/ai-content-factory)

**Multi-agent content pipeline** — Research → 5 platform drafts → HITL → Publish.

[▶ Live demo](https://ai-content-factory-iota.vercel.app) · LangGraph · Clerk · Render + Vercel

### [Enterprise RAG Platform](https://github.com/vpeetla-ai/enterprise_rag_platform)

**Governed knowledge layer** — access-before-ranking, hybrid retrieval, AegisAI HITL bridge, Qdrant adapter, OTLP export.

[▶ Live demo](https://enterprise-rag-platform.vercel.app)

### [vLLM Architecture Lab](https://github.com/vpeetla-ai/vllm-architecture-lab) · **LIVE**

**PagedAttention · Continuous Batching · KV Cache** — interactive 5-tab architecture explorer + Python engine simulator (scheduler, block allocator, memory budget API).

[▶ Live demo](https://vllm-architecture-lab.vercel.app) · [API](https://vllm-architecture-lab-api.onrender.com/health) · FastAPI · Educational simulator

### [AegisLoop AgentOps Workbench](https://github.com/vpeetla-ai/aegisloop-agentops-workbench)

**Mission fleets + eval gates** — FinOps estimates, Langfuse spans, VAP delegation, AegisAI human-gated ship, Netlify→FastAPI proxy.

[▶ Live mission console](https://aegisloop-agentops-workbench.vercel.app)

---

## How the stack fits together

```text
What should agents do?     →  Venkat AI Platform (orchestration)
What are agents allowed?   →  AegisAI (gateway, policy, HITL, audit)
What knowledge can they use? → Enterprise RAG (access-aware retrieval)
How do we operate them?    →  AegisLoop (missions, traces, eval gates)
What do they produce?        →  AI Content Factory (governed publish pipeline)
How do agents improve?       →  LoopForge (harness · LangGraph · repo fix → PR)
How do we serve LLMs?        →  vLLM Architecture Lab (PagedAttention · batching · KV budget)
```

| Layer | Repository | Live demo |
|-------|------------|-----------|
| **Self-improvement** | [loop-engine-agent-platform](https://github.com/vpeetla-ai/loop-engine-agent-platform) | [LoopForge UI](https://demo-omega-taupe.vercel.app) · [API](https://loopforge-api.onrender.com) |
| **Agent governance** | [aegisai-enterprise-agent-platform](https://github.com/vpeetla-ai/aegisai-enterprise-agent-platform) | [Control plane](https://aegisai-enterprise-agent-platform.vercel.app) |
| **Multi-agent OS** | [venkat-ai-platform](https://github.com/vpeetla-ai/venkat-ai-platform) | [VAP console](https://venkat-ai-platform.vercel.app) |
| **Knowledge** | [enterprise_rag_platform](https://github.com/vpeetla-ai/enterprise_rag_platform) | [RAG lab](https://enterprise-rag-platform.vercel.app) |
| **AgentOps** | [aegisloop-agentops-workbench](https://github.com/vpeetla-ai/aegisloop-agentops-workbench) | [Mission console](https://aegisloop-agentops-workbench.vercel.app) |
| **Content automation** | [ai-content-factory](https://github.com/vpeetla-ai/ai-content-factory) | [Content pipeline](https://ai-content-factory-iota.vercel.app) |
| **LLM inference** | [vllm-architecture-lab](https://github.com/vpeetla-ai/vllm-architecture-lab) | [Architecture lab](https://vllm-architecture-lab.vercel.app) · [API](https://vllm-architecture-lab-api.onrender.com) |

### Production Agent Patterns (series)

| # | Pattern | Repository | Live demo |
|---|---------|------------|-----------|
| 1 | ReAct | [react-agent-pattern](https://github.com/vpeetla-ai/react-agent-pattern) | [Trace viewer](https://react-agent-pattern.vercel.app) |
| 2 | Reflection | [reflection-agent-pattern](https://github.com/vpeetla-ai/reflection-agent-pattern) | [Trace viewer](https://reflection-agent-pattern.vercel.app) |
| 3 | Plan-Execute | [plan-execute-agent-pattern](https://github.com/vpeetla-ai/plan-execute-agent-pattern) | [Trace viewer](https://plan-execute-agent-pattern.vercel.app) |
| 4 | Multi-Agent | [multi-agent-system-pattern](https://github.com/vpeetla-ai/multi-agent-system-pattern) | [Trace viewer](https://multi-agent-system-pattern.vercel.app) |
| 5 | Swarm | [swarm-agent-pattern](https://github.com/vpeetla-ai/swarm-agent-pattern) | [Trace viewer](https://swarm-agent-pattern.vercel.app) |

---

## Currently building

- [x] **LoopForge** — LangGraph repo fix loop, PR workflow, live on Render + Vercel
- [x] VAP ↔ AegisAI gateway (notify channels)
- [x] VAP — 3 orchestrators + 7 RAG strategies + Enterprise RAG adapter
- [x] Enterprise RAG ↔ AegisAI HITL bridge + Qdrant adapter
- [x] AegisLoop — FinOps, Langfuse, VAP delegation, gateway ship path
- [x] **vLLM Architecture Lab** — PagedAttention simulator live on Vercel + Render
- [x] **vpeetla-ai-skills** — org-wide agent skills (Cursor + Codex)
- [x] Live demos on Vercel for VAP, AegisLoop, Enterprise RAG, LoopForge, vLLM Lab, and all 5 agent pattern repos

---

## Writing

- **Substack** — [venkatapeetla.substack.com](https://venkatapeetla.substack.com) — architecture decisions for production AI
- **Medium** — [@vpeetla.ai](https://medium.com/@vpeetla.ai) — agent patterns & RAG governance
- **Essay** — [From Multi-Agent OS to Agent Governance](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/case-studies/from-multi-agent-os-to-agent-governance.md) (VAP + AegisAI story)

---

## Connect

- 🌐 [venkat-ai.com](https://venkat-ai.com)
- 💼 [LinkedIn](https://linkedin.com/in/venkata-peetla)
- 📰 [Substack](https://venkatapeetla.substack.com)

If any repo helps you, a ⭐ helps other builders discover it.
