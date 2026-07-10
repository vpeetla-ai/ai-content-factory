<!-- Profile README for https://github.com/vpeetla-ai (Overview tab) -->
<!-- Canonical: vpeetla-ai/README.md — keep ACF docs/github-profile in sync -->

# Hi, I'm Venkata Peetla — Principal AI Architect

> **16 live products** (11 production platforms + 5 curriculum pattern products) · **22 open-source repos** · **26 ADRs** — inspect before we talk.

[![Website](https://img.shields.io/badge/Website-venkat--ai.com-blue)](https://venkat-ai.com)
[![Technical review](https://img.shields.io/badge/5--Min_Technical_Review-Start_here-5eead4)](https://venkat-ai.com/technical-review)
[![Architecture portfolio](https://img.shields.io/badge/Architecture_Portfolio-ADRs_%26_Case_Studies-purple)](https://github.com/vpeetla-ai/ai-architecture-portfolio)
[![LinkedIn launch plan](https://img.shields.io/badge/LinkedIn_Launch_Plan-Phase_tracker-0A66C2)](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/docs/LINKEDIN_LAUNCH_PLAN.md)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2)](https://linkedin.com/in/venkata-peetla)
[![Substack](https://img.shields.io/badge/Substack-Subscribe-orange)](https://venkatapeetla.substack.com)

---

## Start here

| For | Link |
|-----|------|
| **Engineering panels (5 min)** | [venkat-ai.com/technical-review](https://venkat-ai.com/technical-review) |
| **Full portfolio** | [venkat-ai.com/work](https://venkat-ai.com/work) |
| **Hire overview** | [venkat-ai.com/hire](https://venkat-ai.com/hire) |
| **Flagship essay** | [From Multi-Agent OS to Agent Governance](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/case-studies/from-multi-agent-os-to-agent-governance.md) |

---

## Architecture portfolio

**[ai-architecture-portfolio](https://github.com/vpeetla-ai/ai-architecture-portfolio)** — **26 ADRs**, case studies, trade-offs, and stack map (incl. `PRODUCTION_STRICT`, NIST AI RMF, multi-tenant isolation).

→ [Featured case studies](https://github.com/vpeetla-ai/ai-architecture-portfolio#featured-case-studies) · [LinkedIn launch plan](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/docs/LINKEDIN_LAUNCH_PLAN.md) · [golden-eval-registry](https://github.com/vpeetla-ai/golden-eval-registry) (CI regression gates) · [Top-1% 90-day backlog](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/docs/TOP1PCT_90DAY_BACKLOG.md)

### RAG + inference track (flagship quartet)

| Repo | Hook |
|------|------|
| [Enterprise RAG](https://github.com/vpeetla-ai/enterprise_rag_platform) | Access-before-ranking · cross-encoder rerank · decline-to-answer · JWT Principal under `PRODUCTION_STRICT` |
| [DomainForge](https://github.com/vpeetla-ai/domainforge-rag-peft) | RAG facts + PEFT behavior · S0→S4 eval · educational vLLM Path B (ADR-022) |
| [vLLM Lab](https://github.com/vpeetla-ai/vllm-architecture-lab) | PagedAttention · continuous batching · educational multi-LoRA chat `/v1/adapters` |
| [VoiceForge](https://github.com/vpeetla-ai/voiceforge-assistant) | ASR → LLM → TTS · P50/P95 latency budgets |

---

## Agent skills (Cursor + Codex)

**[vpeetla-ai-skills](https://github.com/vpeetla-ai/vpeetla-ai-skills)** — org-wide agent skills for every repo: LangGraph, gateway/HITL, loop engineering, TDD, deploy.

```bash
git clone https://github.com/vpeetla-ai/vpeetla-ai-skills.git
./vpeetla-ai-skills/scripts/install.sh --cursor --codex --project .
```

Inspired by [mattpocock/skills](https://github.com/mattpocock/skills) + [Karpathy agentic engineering](https://www.youtube.com/watch?v=96jN2OCOfLs) + [autoresearch](https://github.com/karpathy/autoresearch).

---

## Top projects

### [VoiceForge — Real-Time Voice Triage](https://github.com/vpeetla-ai/voiceforge-assistant) · **LIVE**

**ASR → LLM → TTS** — browser speech + edge-tts + pluggable triage (mock / Ollama / DomainForge), latency waterfall UI, WebSocket phases, graceful degradation.

[▶ Live demo](https://voiceforge-assistant.vercel.app) · [API](https://voiceforge-api-eysb.onrender.com/health) · [ADR-021](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/adr/ADR-021-voiceforge-multimodal-pipeline.md) · FastAPI · edge-tts · Next.js

### [DomainForge — Enterprise RAG + PEFT Pipeline](https://github.com/vpeetla-ai/domainforge-rag-peft) · **LIVE**

**Fine-tune behavior, retrieve facts** — QLoRA for strict JSON triage + hybrid RAG over capstone SOP corpus, with S0→S4 eval harness (incl. DPO) and adapter promotion gates.

[▶ Live demo](https://domainforge-rag-peft.vercel.app) · [API](https://domainforge-api.onrender.com/health) · [ADR-019](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/adr/ADR-019-rag-facts-peft-behavior.md) · Chroma · TRL · PEFT · Bitext SFT

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

### [Enterprise RAG Platform](https://github.com/vpeetla-ai/enterprise_rag_platform)

**Governed knowledge layer** — access-before-ranking, hybrid retrieval, cross-encoder rerank, decline-to-answer, AegisAI HITL bridge, Qdrant adapter.

[▶ Live demo](https://enterprise-rag-platform-eta.vercel.app)

### [AI Content Factory](https://github.com/vpeetla-ai/ai-content-factory)

**Multi-agent content pipeline** — Research → 5 platform drafts → HITL → Publish.

[▶ Live demo](https://ai-content-factory-iota.vercel.app) · LangGraph · Clerk · Render + Vercel

### [Golden Eval Registry](https://github.com/vpeetla-ai/golden-eval-registry)

**Cross-repo regression contracts** — versioned golden fixtures for RAG answers, LoopForge benchmarks, repo-fix, mission gates, and Content Factory HITL.

Validator · JSONL suites · CI · Evals-as-product proof

### [vLLM Architecture Lab](https://github.com/vpeetla-ai/vllm-architecture-lab) · **LIVE**

**PagedAttention · Continuous Batching · KV Cache** — interactive 5-tab architecture explorer + Python engine simulator (scheduler, block allocator, memory budget API).

[▶ Live demo](https://vllm-architecture-lab.vercel.app) · [API](https://vllm-architecture-lab-api.onrender.com/health) · FastAPI · Educational simulator

### [AegisLoop AgentOps Workbench](https://github.com/vpeetla-ai/aegisloop-agentops-workbench)

**Mission fleets + eval gates** — FinOps estimates, Langfuse spans, VAP delegation, AegisAI human-gated ship, Netlify→FastAPI proxy.

[▶ Live mission console](https://aegisloop-agentops-workbench.vercel.app)

### [Sentinel Brief](https://github.com/vpeetla-ai/sentinel-brief) · **LIVE**

**Overnight AI radar** — HN, arXiv, VentureBeat, MIT Tech Review, The Batch, Paper Digest, Towards Data Science, and more → snapshot diff → eval gate → governed email.

[▶ Live demo](https://sentinel-brief-ruddy.vercel.app) · [API](https://sentinel-brief-api.onrender.com/health) · LangGraph · Resend · eval gate · cron

---

## How the stack fits together

```text
What should agents do?       →  Venkat AI Platform (orchestration)
What are agents allowed?     →  AegisAI (gateway, policy, HITL, audit)
What knowledge can they use? →  Enterprise RAG (access-before-ranking)
How do we adapt domain format? → DomainForge (RAG facts + PEFT behavior)
How do we run voice triage?     → VoiceForge (ASR → LLM → TTS + latency budgets)
How do we operate fleets?    →  AegisLoop (missions, traces, eval gates)
What did agents cost?        →  Agent FinOps (metering + budgets)
What do they produce?        →  AI Content Factory (governed publish)
How do agents improve?       →  LoopForge (harness · repo fix → PR)
How do we serve LLMs?        →  vLLM Architecture Lab (educational multi-LoRA Path B)
How do we prove quality?     →  Golden Eval Registry (versioned eval contracts)
Overnight signal?            →  Sentinel Brief
```

| Layer | Repository | Live demo |
|-------|------------|-----------|
| **Knowledge + MLOps** | [domainforge-rag-peft](https://github.com/vpeetla-ai/domainforge-rag-peft) | [DomainForge UI](https://domainforge-rag-peft.vercel.app) · [API](https://domainforge-api.onrender.com) |
| **Voice / Multimodal** | [voiceforge-assistant](https://github.com/vpeetla-ai/voiceforge-assistant) | [VoiceForge UI](https://voiceforge-assistant.vercel.app) · [API](https://voiceforge-api-eysb.onrender.com) |
| **Self-improvement** | [loop-engine-agent-platform](https://github.com/vpeetla-ai/loop-engine-agent-platform) | [LoopForge UI](https://demo-omega-taupe.vercel.app) · [API](https://loopforge-api.onrender.com) |
| **Agent governance** | [aegisai-enterprise-agent-platform](https://github.com/vpeetla-ai/aegisai-enterprise-agent-platform) | [Control plane](https://aegisai-enterprise-agent-platform.vercel.app) |
| **Multi-agent OS** | [venkat-ai-platform](https://github.com/vpeetla-ai/venkat-ai-platform) | [VAP console](https://venkat-ai-platform.vercel.app) |
| **Knowledge** | [enterprise_rag_platform](https://github.com/vpeetla-ai/enterprise_rag_platform) | [RAG lab](https://enterprise-rag-platform-eta.vercel.app) |
| **AgentOps** | [aegisloop-agentops-workbench](https://github.com/vpeetla-ai/aegisloop-agentops-workbench) | [Mission console](https://aegisloop-agentops-workbench.vercel.app) |
| **FinOps** | [agent-finops](https://github.com/vpeetla-ai/agent-finops) | [FinOps UI](https://agent-finops.vercel.app) · [API](https://agent-finops-api.onrender.com) |
| **Content automation** | [ai-content-factory](https://github.com/vpeetla-ai/ai-content-factory) | [Content pipeline](https://ai-content-factory-iota.vercel.app) |
| **LLM inference** | [vllm-architecture-lab](https://github.com/vpeetla-ai/vllm-architecture-lab) | [Architecture lab](https://vllm-architecture-lab.vercel.app) · [API](https://vllm-architecture-lab-api.onrender.com) |
| **Eval contracts** | [golden-eval-registry](https://github.com/vpeetla-ai/golden-eval-registry) | Versioned golden eval fixtures |
| **Overnight intelligence** | [sentinel-brief](https://github.com/vpeetla-ai/sentinel-brief) | [Brief UI](https://sentinel-brief-ruddy.vercel.app) · [API](https://sentinel-brief-api.onrender.com) |

### Curriculum Agent Patterns (series — teaching stubs)

Deterministic stub loops + live trace viewers for interviews and skill-building. **Not** production fleets — compose into VAP / Content Factory for governed graphs. Status tables mark LangGraph production graph 🟡, gateway ❌.

| # | Pattern | Repository | Live demo |
|---|---------|------------|-----------|
| 1 | ReAct | [react-agent-pattern](https://github.com/vpeetla-ai/react-agent-pattern) | [Trace viewer](https://react-agent-pattern.vercel.app) |
| 2 | Reflection | [reflection-agent-pattern](https://github.com/vpeetla-ai/reflection-agent-pattern) | [Trace viewer](https://reflection-agent-pattern.vercel.app) |
| 3 | Plan-Execute | [plan-execute-agent-pattern](https://github.com/vpeetla-ai/plan-execute-agent-pattern) | [Trace viewer](https://plan-execute-agent-pattern.vercel.app) |
| 4 | Multi-Agent | [multi-agent-system-pattern](https://github.com/vpeetla-ai/multi-agent-system-pattern) | [Trace viewer](https://multi-agent-system-pattern.vercel.app) |
| 5 | Swarm | [swarm-agent-pattern](https://github.com/vpeetla-ai/swarm-agent-pattern) | [Trace viewer](https://swarm-agent-pattern.vercel.app) |

---

## Production platforms (11)

| Platform | Live URL |
|----------|----------|
| **VoiceForge** — real-time voice triage | [voiceforge-assistant.vercel.app](https://voiceforge-assistant.vercel.app) |
| **DomainForge** — RAG + PEFT triage | [domainforge-rag-peft.vercel.app](https://domainforge-rag-peft.vercel.app) |
| **AegisAI** — agent governance | [aegisai-enterprise-agent-platform.vercel.app](https://aegisai-enterprise-agent-platform.vercel.app) |
| **Venkat AI Platform** — multi-agent OS | [venkat-ai-platform.vercel.app](https://venkat-ai-platform.vercel.app) |
| **Enterprise RAG** — access-aware retrieval | [enterprise-rag-platform-eta.vercel.app](https://enterprise-rag-platform-eta.vercel.app) |
| **AegisLoop** — AgentOps missions | [aegisloop-agentops-workbench.vercel.app](https://aegisloop-agentops-workbench.vercel.app) |
| **AI Content Factory** — governed publish | [ai-content-factory-iota.vercel.app](https://ai-content-factory-iota.vercel.app) |
| **LoopForge** — repo fix → PR | [demo-omega-taupe.vercel.app](https://demo-omega-taupe.vercel.app) |
| **vLLM Architecture Lab** | [vllm-architecture-lab.vercel.app](https://vllm-architecture-lab.vercel.app) |
| **Sentinel Brief** — overnight intelligence | [sentinel-brief-ruddy.vercel.app](https://sentinel-brief-ruddy.vercel.app) |
| **Practice Arena** — system design mock interviews | [ai-architect-practice-arena.vercel.app](https://ai-architect-practice-arena.vercel.app) |

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

*Metrics synced Jul 2026 — update `venkat-ai-portfolio/data/metrics.ts` as source of truth.*
