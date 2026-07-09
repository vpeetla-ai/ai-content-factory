# vpeetla-ai Domain Model

Shared vocabulary for all org repos. Agents should use these terms consistently.

**Org:** [github.com/vpeetla-ai](https://github.com/vpeetla-ai) · **Portfolio hub:** [venkat-ai.com/work](https://venkat-ai.com/work) · **Case studies / ADRs:** [ai-architecture-portfolio](https://github.com/vpeetla-ai/ai-architecture-portfolio)

---

## Stack layers

| Layer | Question | Repo | Live demo | API (Render) |
|-------|----------|------|-----------|--------------|
| Orchestration | What should agents do? | venkat-ai-platform | [venkat-ai-platform.vercel.app](https://venkat-ai-platform.vercel.app) | `vap-api.onrender.com` |
| Governance | What are agents allowed? | aegisai-enterprise-agent-platform | [aegisai-enterprise-agent-platform.vercel.app](https://aegisai-enterprise-agent-platform.vercel.app) | `aegisai-api.onrender.com` |
| Knowledge | What knowledge can they use? | enterprise_rag_platform | [enterprise-rag-platform-eta.vercel.app](https://enterprise-rag-platform-eta.vercel.app) | `enterprise-rag-api-4el1.onrender.com` |
| Knowledge + MLOps | How do we adapt models to domain format? | domainforge-rag-peft | [domainforge-rag-peft.vercel.app](https://domainforge-rag-peft.vercel.app) | `domainforge-api.onrender.com` |
| Voice / Multimodal | How do we run real-time voice triage? | voiceforge-assistant | [voiceforge-assistant.vercel.app](https://voiceforge-assistant.vercel.app) | `voiceforge-api-eysb.onrender.com` |
| AgentOps | How do we operate fleets? | aegisloop-agentops-workbench | [aegisloop-agentops-workbench.vercel.app](https://aegisloop-agentops-workbench.vercel.app) | `aegisloop-api.onrender.com` |
| FinOps | What did agents cost? | agent-finops | [agent-finops.vercel.app](https://agent-finops.vercel.app) | `agent-finops-api.onrender.com` |
| Application | What do they produce? | ai-content-factory | [ai-content-factory-iota.vercel.app](https://ai-content-factory-iota.vercel.app) | `acf-api-eub4.onrender.com` *(active)* |
| Self-improvement | How do agents improve? | loop-engine-agent-platform | [demo-omega-taupe.vercel.app](https://demo-omega-taupe.vercel.app) | `loopforge-api.onrender.com` |
| Inference education | How do we serve LLMs? | vllm-architecture-lab | [vllm-architecture-lab.vercel.app](https://vllm-architecture-lab.vercel.app) | `vllm-architecture-lab-api.onrender.com` |
| Overnight intel | What changed overnight? | sentinel-brief | [sentinel-brief-ruddy.vercel.app](https://sentinel-brief-ruddy.vercel.app) | `sentinel-brief-api.onrender.com` |
| Eval contracts | How do we prove quality? | golden-eval-registry | — (fixtures + CI) | — |
| Interview prep | How do we practice architecture? | ai-architect-interview-playbook | — (markdown) | — |
| Mock interviews | BYOK judge practice | ai-architect-practice-arena | [ai-architect-practice-arena.vercel.app](https://ai-architect-practice-arena.vercel.app) | `practice-arena-api.onrender.com` |
| Skills / MCP | How do agents follow org rules? | vpeetla-ai-skills | — | — |
| Public site | How is the stack presented? | venkat-ai-portfolio | [venkat-ai.com](https://venkat-ai.com) | — |

**Stale Vercel aliases (do not use):** `enterprise-rag-platform.vercel.app` (old static demo), `sentinel-brief.vercel.app` (wrong project), `acf-api.onrender.com` (suspended — use `acf-api-eub4`).

**Demo access status (Phase 4 verify — Jul 7 2026):**

| Demo | HTTP | Public? | Action needed |
|------|------|---------|---------------|
| enterprise-rag-platform-eta | 200 | ✅ | — |
| vllm-architecture-lab | 200 | ✅ | — |
| venkat-ai-platform | 200 | ✅ | — |
| aegisloop-agentops-workbench | 200 | ✅ | — |
| demo-omega-taupe (LoopForge) | 200 | ✅ | — |
| sentinel-brief-ruddy | 200 | ✅ | — |
| aegisai-enterprise-agent-platform | 200 | ✅ | — |
| domainforge-rag-peft | 200 | ✅ | Canonical `domainforge-rag-peft.vercel.app` live (Jul 8 2026); `/bench` 200 |
| voiceforge-assistant | 200 | ✅ | Canonical `voiceforge-assistant.vercel.app` live (Jul 8 2026) |
| agent-finops | 200 | ✅ | UI + API live at `agent-finops-api.onrender.com` (Jul 8 2026) |
| demo-omega-taupe (LoopForge) | 200 | ✅ | Architect workbench redeployed (Jul 8 2026) |
| ai-content-factory-iota | 200 at `/` (public landing), `/dashboard` app | ✅ | Public landing + Clerk dashboard |

> All core demos public (DomainForge, VoiceForge, LoopForge, Agent FinOps). Canonical FinOps API host is `agent-finops-api.onrender.com` (not `agent-finops.onrender.com`).

---

## Jul 2026 org-wide changes (summary)

1. **API-key gates** on production write paths: VAP (`VAP_API_KEY`), Enterprise RAG ingest/answer, LoopForge repo-fix/HITL, Sentinel `POST /runs`, AegisLoop mission run/stream.
2. **Trace-linked LLMOps** — Langfuse spans documented across VAP, ACF, Sentinel, LoopForge, Enterprise RAG; spec in `ai-architecture-portfolio/docs/TRACE_LINKED_OBSERVABILITY.md`.
3. **Golden eval CI** — `golden-eval-registry` scorer runner; **6/6** suites wired as real CI gates (all suite kinds).
4. **Real FinOps** — new `agent-finops` service; AegisLoop meters via agent-finops (not character-count heuristics).
5. **Real IaC paths** — AegisAI AWS ECS+Fargate+RDS Terraform; agent-finops GCP Cloud Run+Cloud SQL Terraform (ADR PaaS vs IaC trade-offs).
6. **ACF publish** — real LinkedIn/X OAuth publish; invite-only signup; Medium/Substack/Instagram honestly gated.
7. **Enterprise RAG** — upload demo, retrieval ranking fixes, ingestion lineage ADR; cross-encoder rerank + decline-to-answer ([ADR-023](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/adr/ADR-023-enterprise-rag-rerank-decline.md)); Langfuse-only (no OTLP collector).
8. **Sentinel Brief** — real LLM executive summary; logging fix for `POST /runs`.
9. **AegisLoop** — real VAP A2A delegation before mission invoke.
10. **Interview layer** — playbook 35/35 coverage; Practice Arena live with BYOK judges.
11. **Portfolio** — venkat-ai-portfolio light-theme reskin, diagram recolor, navbar fix (Jul 6).
12. **LinkedIn launch prep (Phase 3)** — canonical diagrams for VAP, ACF, AegisLoop, LoopForge; case study + ADR alignment (Enterprise RAG cross-encoder/decline ADR-023, DomainForge S0→S4, vLLM multi-LoRA ADR-022); ecosystem.ts sync.

---

## RAG + inference track (LinkedIn Weeks 1–4)

| Week | Repo | Architectural hook |
|------|------|-------------------|
| 1 | Enterprise RAG | Access-before-ranking · cross-encoder rerank · decline-to-answer ([ADR-023](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/adr/ADR-023-enterprise-rag-rerank-decline.md)) |
| 2 | DomainForge | RAG for facts · PEFT for behavior · S0→S4 eval ladder ([ADR-019](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/adr/ADR-019-rag-facts-peft-behavior.md)) |
| 3 | vLLM Lab | PagedAttention · multi-LoRA economics ([ADR-022](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/adr/ADR-022-domainforge-vllm-multi-lora-serving.md)) |
| 4 | VoiceForge | ASR → LLM → TTS latency budgets ([ADR-021](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/adr/ADR-021-voiceforge-multimodal-pipeline.md)) |

Tracker: [ai-architecture-portfolio/docs/LINKEDIN_LAUNCH_PLAN.md](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/docs/LINKEDIN_LAUNCH_PLAN.md)

## Core terms

| Term | Meaning |
|------|---------|
| **Harness** | Outer scheduler: budgets, tracing, eval gates, loop termination (LoopForge, ODAEU) |
| **Gateway** | AegisAI runtime control plane — policy + HITL + audit before tool side effects |
| **ODAEU** | Observe → Decide → Act → Evaluate → Update (outer self-improve loop) |
| **Access-before-ranking** | Filter chunks by principal clearance before hybrid retrieval scores |
| **HITL** | Human-in-the-loop gate before irreversible actions (publish, push, deploy) |
| **Mission** | Bounded AgentOps unit in AegisLoop (research, content, incident, etc.) |
| **Orchestrator** | LangGraph node that plans and routes between specialist agents |
| **loopforge/fix-{id}** | Branch name for automated repo fixes — never push directly to `main` |
| **Stub mode** | `AGENT_RUNTIME_MODE=local_stub` or MockLLM — no API keys required |
| **Golden eval** | Versioned fixture + scorer in `golden-eval-registry`; wired as CI gate where noted |
| **Agent-finops** | Shared metering/budget service consumed by AegisLoop (and org-wide FinOps story) |
| **Trace-linked observability** | Langfuse export from graph nodes; eval scores on spans — not generic OTEL-only |

---

## Agent patterns (VAP series)

| Pattern | Repo | Demo |
|---------|------|------|
| ReAct | react-agent-pattern | [react-agent-pattern.vercel.app](https://react-agent-pattern.vercel.app) |
| Reflection | reflection-agent-pattern | [reflection-agent-pattern.vercel.app](https://reflection-agent-pattern.vercel.app) |
| Plan-Execute | plan-execute-agent-pattern | [plan-execute-agent-pattern.vercel.app](https://plan-execute-agent-pattern.vercel.app) |
| Multi-Agent | multi-agent-system-pattern | [multi-agent-system-pattern.vercel.app](https://multi-agent-system-pattern.vercel.app) |
| Swarm | swarm-agent-pattern | [swarm-agent-pattern.vercel.app](https://swarm-agent-pattern.vercel.app) |

---

## Deploy boundaries (ADR-005)

- **UI** → Vercel (static or Next.js)
- **API** → Render (Docker or native Python); optional real IaC (AWS/GCP) for governance/FinOps demos
- **Vectors** → Qdrant Cloud (optional)
- **LLM** → Groq / OpenRouter / LiteLLM routing
- **Free tier** → `plan: free` in render.yaml; expect cold starts
- **Vercel aliases** — after `vercel deploy --prod`, re-assign short aliases (`-iota`, `-eta`, `-ruddy`) if 404

---

## Integration rules

- VAP **delegates** side effects; AegisAI **authorizes** them
- Enterprise RAG **feeds** VAP strategies; does not replace gateway
- LoopForge **improves** configs/prompts; does not replace orchestration
- AegisLoop **meters** via agent-finops; **delegates** to VAP via A2A when configured
- Side effects (notify, publish, deploy, git push to protected branch) → **gateway or HITL** unless explicitly in local stub mode

---

## Skills install

```bash
./vpeetla-ai-skills/scripts/install.sh --cursor --project .
```

Routing table: `vpeetla-ai-skills/skills/governed-ai-stack/SKILL.md`
