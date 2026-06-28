# Flagship article draft — Substack / LinkedIn / Medium

Use this as your first distribution piece. Cross-post with canonical link to Substack.

---

## Title options (pick one)

1. **Why I Built a 5-Agent Content Pipeline (Instead of One ChatGPT Prompt)**
2. **Production AI Content: Multi-Agent, Human-in-the-Loop, $0 Cloud Stack**
3. **From Topic to LinkedIn + Substack + Medium — With a Human Gate Before Publish**

---

## Hook (opening paragraph)

Most "AI content tools" are a text box and a prayer. You paste a topic, get one generic draft, and hope it’s good enough for LinkedIn, Substack, and Medium.

That’s not how production teams work.

I built **[AI Content Factory](https://github.com/vpeetla-ai/ai-content-factory)** — an open-source multi-agent system that runs a real pipeline: research with RAG, platform-specific drafts, parallel SEO and visual enrichment, **human approval before anything publishes**, and full observability (LangSmith, Langfuse, Sentry).

It deploys on a free-first stack: Render, Vercel, Neon, Upstash, Qdrant. Push to `main` and you’re live.

[▶ Try the demo](https://ai-content-factory-iota.vercel.app) · [⭐ Star on GitHub](https://github.com/vpeetla-ai/ai-content-factory)

---

## The problem with single-prompt content AI

| Single prompt | Multi-agent pipeline |
|---------------|----------------------|
| One model does everything | Specialized agents per task |
| No source grounding | Research agent + vector RAG |
| Same tone everywhere | Per-platform content agent |
| Ship and pray | HITL gate before publish |
| Black box failures | Traces in LangSmith / Langfuse |

When an agent silently hallucinates a stat, you need traces — not a shrug emoji in Slack.

---

## Architecture (60 seconds)

```text
Topic
  → Research Agent (Gemini + Qdrant RAG)
  → Content Agent (5 platform drafts)
  → SEO Agent ∥ Visual Agent
  → HITL Review (approve / edit / reject)
  → Publisher Agent → LinkedIn, Substack, Medium, Instagram, X
```

Built on **LangGraph** with Redis checkpointing, **FastAPI** backend, **Next.js 14** frontend, **Clerk** auth.

![Architecture diagram](https://github.com/vpeetla-ai/ai-content-factory/raw/main/docs/assets/demo-placeholder.svg)

*(Replace with your demo GIF once recorded — see docs/DEMO_GIF.md)*

---

## Why human-in-the-loop matters

Autonomous publish sounds cool until legal, brand, or factual errors hit a live audience.

The HITL gate uses LangGraph `interrupt_before` — the graph pauses, you review drafts in the UI, edit if needed, then resume. Reject stops the run cleanly.

This is the pattern I wish more agent frameworks documented by default.

---

## Free-first production stack

You don’t need a $2k/month GPU cluster to learn production agents:

- **Frontend:** Vercel
- **API + agents:** Render (Docker)
- **DB:** Neon Postgres
- **Cache / state:** Upstash Redis
- **Vectors:** Qdrant Cloud
- **Auth:** Clerk

Full setup: [DEPLOYMENT.md](https://github.com/vpeetla-ai/ai-content-factory/blob/main/docs/DEPLOYMENT.md)

---

## Part of a larger body of work

This repo connects to my open-source AI architecture work:

- **[Production Agent Patterns](https://github.com/vpeetla-ai/react-agent-pattern)** — ReAct, Reflection, Plan-Execute, Multi-Agent, Swarm
- **[Enterprise RAG Platform](https://github.com/vpeetla-ai/enterprise_rag_platform)** — governed retrieval, not a vector DB wrapper
- **[AegisLoop AgentOps](https://github.com/vpeetla-ai/aegisloop-agentops-workbench)** — tracing and evals for agents

---

## Call to action

1. **[Star the repo](https://github.com/vpeetla-ai/ai-content-factory)** if you’re building similar systems
2. **[Try the live demo](https://ai-content-factory-iota.vercel.app)**
3. **Open an issue** if you want OAuth adapters for a specific platform — good first contributions welcome

I’m Venkata Peetla — AI Architect. More at [venkat-ai.com](https://venkat-ai.com) and [Substack](https://venkatapeetla.substack.com).

---

## LinkedIn post (short version)

Shipped: **AI Content Factory** — open-source multi-agent content pipeline.

Not one prompt. Five agents + RAG + human approval before publish.

LangGraph · FastAPI · Next.js · deploys on free cloud.

Demo: https://ai-content-factory-iota.vercel.app
Code: https://github.com/vpeetla-ai/ai-content-factory

If you’re building production agents, a ⭐ helps others find it.

#AI #LangGraph #MultiAgent #OpenSource

---

## Publishing checklist

- [ ] Publish on Substack (canonical URL)
- [ ] Cross-post to Medium with `canonical` link
- [ ] LinkedIn post with architecture image or GIF
- [ ] Link from profile README after publishing
- [ ] Add article link to ai-content-factory README if desired
