<!-- Profile README for https://github.com/vpeetla-ai (Overview tab) -->
<!-- Sync from: ai-content-factory/docs/github-profile/README.md -->

# Hi, I'm Venkata Peetla — Principal AI Architect

> **16 live products** (11 production platforms + 5 pattern products) · **22 open-source repos** · **20 ADRs** — inspect before we talk.

[![Website](https://img.shields.io/badge/Website-venkat--ai.com-blue)](https://venkat-ai.com)
[![Technical review](https://img.shields.io/badge/5--Min_Technical_Review-Start_here-5eead4)](https://venkat-ai.com/technical-review)
[![Architecture portfolio](https://img.shields.io/badge/Architecture_Portfolio-ADRs_%26_Case_Studies-purple)](https://github.com/vpeetla-ai/ai-architecture-portfolio)
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

**[ai-architecture-portfolio](https://github.com/vpeetla-ai/ai-architecture-portfolio)** — 20 ADRs, case studies, trade-offs, and stack map.

→ [Featured case studies](https://github.com/vpeetla-ai/ai-architecture-portfolio#featured-case-studies) · [golden-eval-registry](https://github.com/vpeetla-ai/golden-eval-registry) (CI regression gates)

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

### Pattern products (5 trace viewers)

ReAct · Reflection · Plan-Execute · Multi-Agent · Swarm — [venkat-ai.com/work#patterns](https://venkat-ai.com/work#patterns)

---

## How the stack fits together

```text
What should agents do?       →  Venkat AI Platform
What are agents allowed?     →  AegisAI (gateway, policy, HITL, audit)
What knowledge can they use? →  Enterprise RAG (access-before-ranking)
How do we adapt domain format? → DomainForge (RAG facts + PEFT behavior)
How do we run voice triage?     → VoiceForge (ASR → LLM → TTS + latency budgets)
How do we operate fleets?    →  AegisLoop (missions, traces, eval gates)
What do they produce?        →  AI Content Factory (governed publish)
How do agents improve?       →  LoopForge (harness · repo fix → PR)
How do we serve LLMs?        →  vLLM Architecture Lab
Overnight signal?            →  Sentinel Brief
```

---

## Agent skills (Cursor + Codex)

```bash
git clone https://github.com/vpeetla-ai/vpeetla-ai-skills.git
./vpeetla-ai-skills/scripts/install.sh --cursor --codex --project .
```

---

## Writing

- **Substack** — [venkatapeetla.substack.com](https://venkatapeetla.substack.com)
- **Portfolio blog** — [venkat-ai.com/blog](https://venkat-ai.com/blog)
- **YouTube** — [@venkat-ai](https://www.youtube.com/@venkat-ai) (architecture walkthroughs launching)

---

## Connect

- 🌐 [venkat-ai.com](https://venkat-ai.com)
- 💼 [LinkedIn](https://linkedin.com/in/venkata-peetla)
- 📰 [Substack](https://venkatapeetla.substack.com)

If any repo helps you, a ⭐ helps other builders discover it.

*Metrics synced Jul 2026 — update `venkat-ai-portfolio/data/metrics.ts` as source of truth.*
