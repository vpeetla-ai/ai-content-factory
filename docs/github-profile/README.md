<!-- Profile README for https://github.com/vpeetla-ai (Overview tab) -->
<!-- Canonical: vpeetla-ai/README.md — keep ACF docs/github-profile in sync -->

# Hi, I'm Venkata Peetla — Principal AI Architect

**Principal AI Architect at [SNH AI](https://www.snh-ai.com/)** (Sep 2026–). I architect digital employees that own a regulated role — verification, public-records research, adjudication — inside the systems a screener already runs. A trace on every action. A person on the exception.

> **6-spine review path** below is inspectable reference architecture (govern · orchestrate · RAG · **models** · publish · ADRs) · **34 ADRs** — not SNH or Lucid production code.

[![Website](https://img.shields.io/badge/Website-venkat--ai.com-blue)](https://venkat-ai.com)
[![Technical review](https://img.shields.io/badge/15--Min_Technical_Review-Start_here-5eead4)](https://venkat-ai.com/technical-review)
[![Architecture portfolio](https://img.shields.io/badge/Architecture_Portfolio-ADRs_%26_Case_Studies-purple)](https://github.com/vpeetla-ai/ai-architecture-portfolio)
[![Model Plane 100%](https://img.shields.io/badge/Model_Plane-100%25_plan-9333EA)](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/docs/MODEL_PLANE_100_PLAN.md)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2)](https://linkedin.com/in/venkata-peetla)
[![Substack](https://img.shields.io/badge/Substack-Subscribe-orange)](https://venkatapeetla.substack.com)

---

## Start here

| For | Link |
|-----|------|
| **Technical review (~15 min)** | [venkat-ai.com/technical-review](https://venkat-ai.com/technical-review) |
| **Current role** | [venkat-ai.com/hire](https://venkat-ai.com/hire) |
| **Full portfolio catalog** | [venkat-ai.com/work](https://venkat-ai.com/work) |
| **Model Plane plan** | [MODEL_PLANE_100_PLAN](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/docs/MODEL_PLANE_100_PLAN.md) |
| **Flagship essay** | [From Multi-Agent OS to Agent Governance](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/case-studies/from-multi-agent-os-to-agent-governance.md) |

---

## Public spine (D1 — review these)

Narrative hub + **agent plane** + **model plane**. Labs stay labs — ModelForge is the hire hero for SLM / PEFT / CUDA vLLM / LLMOps.

| # | Layer | Repo | Live |
|---|-------|------|------|
| 1 | **Decisions** | [ai-architecture-portfolio](https://github.com/vpeetla-ai/ai-architecture-portfolio) | ADRs · [Model Plane 100%](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/docs/MODEL_PLANE_100_PLAN.md) |
| 2 | **Governance** | [aegisai-enterprise-agent-platform](https://github.com/vpeetla-ai/aegisai-enterprise-agent-platform) | [Control plane](https://aegisai-enterprise-agent-platform.vercel.app) |
| 3 | **Orchestration** | [venkat-ai-platform](https://github.com/vpeetla-ai/venkat-ai-platform) | [VAP console](https://venkat-ai-platform.vercel.app) |
| 4 | **Knowledge** | [enterprise_rag_platform](https://github.com/vpeetla-ai/enterprise_rag_platform) | [RAG lab](https://enterprise-rag-platform-eta.vercel.app) |
| 5 | **Models** | [modelforge-llmops](https://github.com/vpeetla-ai/modelforge-llmops) | [ModelForge live](https://modelforge-gamma.vercel.app) |
| 6 | **Application** | [ai-content-factory](https://github.com/vpeetla-ai/ai-content-factory) | [Content pipeline](https://ai-content-factory-iota.vercel.app) |

**Proof (linked, not hero):** [golden-eval-registry](https://github.com/vpeetla-ai/golden-eval-registry) · [agent-finops](https://github.com/vpeetla-ai/agent-finops)  
**Career layer:** [ai-architect-interview-playbook](https://github.com/vpeetla-ai/ai-architect-interview-playbook) · [ai-architect-practice-arena](https://github.com/vpeetla-ai/ai-architect-practice-arena)

---

## Two planes (how I talk to a CAIO)

```text
AGENT PLANE                         MODEL PLANE
What should agents do?     → VAP    Which weights?          → ModelForge
What are they allowed?     → Aegis  How do we adapt?        → DomainForge (PEFT)
What knowledge?            → RAG    How do we serve?        → CUDA vLLM (+ lab for math)
What do they produce?      → ACF    How do we route/meter?  → LLM gateway + FinOps
```

**30s:** I don’t only build agents. Agents decide *what to do*; ModelForge decides *which weights, where they run, and how we prove it* — SLM bake-offs, PEFT receipts, CUDA vLLM metrics, gateway enforce+record.

---

## Agent skills (Cursor + Codex)

**[vpeetla-ai-skills](https://github.com/vpeetla-ai/vpeetla-ai-skills)** — org-wide agent skills for every repo: LangGraph, gateway/HITL, loop engineering, TDD, deploy, vLLM inference.

```bash
git clone https://github.com/vpeetla-ai/vpeetla-ai-skills.git
./vpeetla-ai-skills/scripts/install.sh --cursor --codex --project .
```

---

## Top projects (spine detail)

### [AegisAI — Enterprise Agent Governance](https://github.com/vpeetla-ai/aegisai-enterprise-agent-platform)

I'd put an independent gateway in front of irreversible tools — policy, HITL on the scary ones, signed audit. The agent graph doesn't get a back door.

[▶ Live control plane](https://aegisai-enterprise-agent-platform.vercel.app)

### [Venkat AI Platform (VAP)](https://github.com/vpeetla-ai/venkat-ai-platform)

**Principal-architect multi-agent OS** — LangGraph orchestrators, RAG strategies, loop patterns, gateway-wrapped notify.

[▶ Live demo](https://venkat-ai-platform.vercel.app)

### [Enterprise RAG Platform](https://github.com/vpeetla-ai/enterprise_rag_platform)

**Governed knowledge layer** — access-before-ranking, hybrid retrieval, cross-encoder rerank, decline-to-answer.

[▶ Live demo](https://enterprise-rag-platform-eta.vercel.app)

### [ModelForge — Model Plane](https://github.com/vpeetla-ai/modelforge-llmops)

**SLM · PEFT · CUDA vLLM · LLMOps** — hire hero for the model plane. Composes DomainForge training, upstream vLLM serve receipts, SLM bake-off, and aegis-llm-gateway.

[▶ Live ModelForge](https://modelforge-gamma.vercel.app) · [ADR-034](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/adr/ADR-034-modelforge-model-plane.md) · [100% plan](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/docs/MODEL_PLANE_100_PLAN.md)

### [AI Content Factory](https://github.com/vpeetla-ai/ai-content-factory)

**Multi-agent content pipeline** — Research → drafts → HITL → Publish.

[▶ Live demo](https://ai-content-factory-iota.vercel.app)

### [Architecture portfolio — ADRs](https://github.com/vpeetla-ai/ai-architecture-portfolio)

**34 ADRs**, case studies, Model Plane 100% tracker.

---

## Model Plane depth (feeds ModelForge)

| Repo | Role |
|------|------|
| [DomainForge](https://github.com/vpeetla-ai/domainforge-rag-peft) | RAG facts + QLoRA/DPO behavior (ADR-019/020) |
| [vLLM Architecture Lab](https://github.com/vpeetla-ai/vllm-architecture-lab) | Educational paging/batching (not CUDA prod) |
| [aegis-llm-gateway](https://github.com/vpeetla-ai/aegis-llm-gateway) | Apps select · plane enforces+records |

---

## Labs & secondary platforms

| Repo | Hook |
|------|------|
| [OmniForge](https://github.com/vpeetla-ai/omniforge) | Multimodal multi-LLM ask |
| [LoopForge](https://github.com/vpeetla-ai/loop-engine-agent-platform) | Harness · repo fix → PR |
| [VoiceForge](https://github.com/vpeetla-ai/voiceforge-assistant) | ASR → LLM → TTS |
| [AegisLoop](https://github.com/vpeetla-ai/aegisloop-agentops-workbench) | Mission fleets + eval gates |
| [Sentinel Brief](https://github.com/vpeetla-ai/sentinel-brief) | Overnight AI radar |

Pattern stubs (ReAct · Reflection · Plan-Execute · Multi-Agent · Swarm) remain curriculum — compose into VAP.

---

## Writing

- **Substack** — [venkatapeetla.substack.com](https://venkatapeetla.substack.com)
- **Essay** — From Multi-Agent OS to Agent Governance

---

## Connect

- 🌐 [venkat-ai.com](https://venkat-ai.com)
- 💼 [LinkedIn](https://linkedin.com/in/venkata-peetla)
- 📰 [Substack](https://venkatapeetla.substack.com)

_Spine narrative: agent plane + model plane (ADR-034) — see MODEL_PLANE_100_PLAN.md._
