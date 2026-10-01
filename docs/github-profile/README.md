<!-- Profile README for https://github.com/vpeetla-ai (Overview tab) -->
<!-- Canonical: vpeetla-ai/README.md -->

# Hi, I'm Venkata Peetla — Principal AI Architect

**Principal AI Architect at [SNH AI](https://www.snh-ai.com/)** (Sep 2026–). I architect digital employees that own a regulated role — verification, public-records research, adjudication — inside the systems a screener already runs. A trace on every action. A person on the exception.

> **6-spine review path** below is inspectable reference architecture (govern · orchestrate · RAG · **models** · publish · ADRs) · **37 ADRs** — personal work, not SNH or Lucid production code.

[![Website](https://img.shields.io/badge/Website-venkat--ai.com-blue)](https://venkat-ai.com)
[![Technical review](https://img.shields.io/badge/15--Min_Technical_Review-Start_here-5eead4)](https://venkat-ai.com/technical-review)
[![Current role](https://img.shields.io/badge/Principal_AI_Architect-SNH_AI-111827)](https://venkat-ai.com/hire)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2)](https://linkedin.com/in/venkata-peetla)
[![Substack](https://img.shields.io/badge/Substack-Subscribe-orange)](https://venkatapeetla.substack.com)

---

## Start here

| For | Link |
|-----|------|
| **Technical review (~15 min)** | [venkat-ai.com/technical-review](https://venkat-ai.com/technical-review) |
| **Current role** | [venkat-ai.com/hire](https://venkat-ai.com/hire) |
| **Leadership** | [venkat-ai.com/leadership](https://venkat-ai.com/leadership) |
| **FDE field method** | [venkat-ai.com/fde](https://venkat-ai.com/fde) |
| **Full portfolio catalog** | [venkat-ai.com/work](https://venkat-ai.com/work) |
| **Model Plane plan** | [MODEL_PLANE_100_PLAN](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/docs/MODEL_PLANE_100_PLAN.md) |
| **Flagship essay** | [From Multi-Agent OS to Agent Governance](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/case-studies/from-multi-agent-os-to-agent-governance.md) |

---

## Public spine (review these)

Narrative hub + **agent plane** + **model plane**. Labs stay labs.

| # | Layer | Repo | Live |
|---|-------|------|------|
| 1 | **Decisions** | [ai-architecture-portfolio](https://github.com/vpeetla-ai/ai-architecture-portfolio) | ADRs · [honest scorecard](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/docs/ORG_HONEST_SCORECARD.md) |
| 2 | **Governance** | [aegisai-enterprise-agent-platform](https://github.com/vpeetla-ai/aegisai-enterprise-agent-platform) | [Control plane](https://aegisai-enterprise-agent-platform.vercel.app) |
| 3 | **Orchestration** | [venkat-ai-platform](https://github.com/vpeetla-ai/venkat-ai-platform) | [VAP console](https://venkat-ai-platform.vercel.app) |
| 4 | **Knowledge** | [enterprise_rag_platform](https://github.com/vpeetla-ai/enterprise_rag_platform) | [RAG lab](https://enterprise-rag-platform-eta.vercel.app) |
| 5 | **Models** | [modelforge-llmops](https://github.com/vpeetla-ai/modelforge-llmops) | [ModelForge](https://modelforge-gamma.vercel.app) — receipts, not win-rates |
| 6 | **Application** | [ai-content-factory](https://github.com/vpeetla-ai/ai-content-factory) | [Content pipeline](https://ai-content-factory-iota.vercel.app) |

**Proof (linked, not hero):** [golden-eval-registry](https://github.com/vpeetla-ai/golden-eval-registry) · [agent-finops](https://github.com/vpeetla-ai/agent-finops)

---

## Two planes (how I talk to a CAIO)

```text
AGENT PLANE                         MODEL PLANE
What should agents do?     → VAP    Which weights?          → ModelForge
What are they allowed?     → Aegis  How do we adapt?        → DomainForge (PEFT)
What knowledge?            → RAG    How do we serve?        → CUDA vLLM (+ lab for math)
What do they produce?      → ACF    How do we route/meter?  → LLM gateway + FinOps
```

**30s:** I don't only build agents. Agents decide *what to do*. The model plane decides *which weights, where they run, and how we prove it* — without pretending a training receipt is a quality score.

---

## Agent skills (Cursor + Codex)

**[vpeetla-ai-skills](https://github.com/vpeetla-ai/vpeetla-ai-skills)** — org-wide agent skills: LangGraph, gateway/HITL, loop engineering, TDD, deploy, vLLM inference.

```bash
git clone https://github.com/vpeetla-ai/vpeetla-ai-skills.git
./vpeetla-ai-skills/scripts/install.sh --cursor --codex --project .
```

---

## Top projects (spine detail)

### [AegisAI — Enterprise Agent Governance](https://github.com/vpeetla-ai/aegisai-enterprise-agent-platform)

I'd put an independent gateway in front of irreversible tools — policy, HITL on the scary ones, signed audit. The agent graph doesn't get a back door. This repo is personal work — a public reference you can inspect.

[▶ Live control plane](https://aegisai-enterprise-agent-platform.vercel.app)

### [Venkat AI Platform (VAP)](https://github.com/vpeetla-ai/venkat-ai-platform)

What agents should do — specialists, RAG strategies, gateway-wrapped notify. Orchestration stays separate from governance on purpose.

[▶ Live demo](https://venkat-ai-platform.vercel.app)

### [Enterprise RAG Platform](https://github.com/vpeetla-ai/enterprise_rag_platform)

Filter by who the caller is *before* you rank. Optimizing recall with unauthorized neighbors is how demos look smart and prod leaks.

[▶ Live demo](https://enterprise-rag-platform-eta.vercel.app)

### [ModelForge — Model Plane](https://github.com/vpeetla-ai/modelforge-llmops)

SLM · PEFT · CUDA vLLM · LLMOps. Hire hero for the model plane. PEFT and vLLM receipts are real L4 runs. They are not adapter win-rates.

[▶ Live ModelForge](https://modelforge-gamma.vercel.app)

### [AI Content Factory](https://github.com/vpeetla-ai/ai-content-factory)

Research → drafts → HITL → publish. Side effects stay behind gates. Publish fails closed when Strict.

[▶ Live demo](https://ai-content-factory-iota.vercel.app)

### [Architecture portfolio — ADRs](https://github.com/vpeetla-ai/ai-architecture-portfolio)

What I decided, what I refused, and live links. Start with the [honest scorecard](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/docs/ORG_HONEST_SCORECARD.md), not a Grade A sticker.

---

## Labs & secondary platforms

Not on the 15-minute path. Open these after the spine holds.

| Repo | Hook |
|------|------|
| [OmniForge](https://github.com/vpeetla-ai/omniforge) | Multimodal multi-LLM ask |
| [LoopForge](https://github.com/vpeetla-ai/loop-engine-agent-platform) | Harness · repo fix → PR |
| [DomainForge](https://github.com/vpeetla-ai/domainforge-rag-peft) | RAG facts + PEFT behavior |
| [VoiceForge](https://github.com/vpeetla-ai/voiceforge-assistant) | ASR → LLM → TTS |
| [AegisLoop](https://github.com/vpeetla-ai/aegisloop-agentops-workbench) | Mission fleets + eval gates |
| [Sentinel Brief](https://github.com/vpeetla-ai/sentinel-brief) | Overnight AI radar |

Pattern stubs (ReAct · Reflection · Plan-Execute · Multi-Agent · Swarm) stay curriculum — compose into VAP.

---

## Writing

- **Substack** — [venkatapeetla.substack.com](https://venkatapeetla.substack.com)
- **Essay** — [From Multi-Agent OS to Agent Governance](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/case-studies/from-multi-agent-os-to-agent-governance.md)

---

## Connect

- [venkat-ai.com](https://venkat-ai.com)
- [LinkedIn](https://linkedin.com/in/venkata-peetla)
- [Substack](https://venkatapeetla.substack.com)
