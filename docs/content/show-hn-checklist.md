# Show HN checklist — AI Content Factory

Use when README, demo, and metadata are polished. Best timing: **Tuesday–Thursday, 8–10 AM US Eastern**.

## Pre-flight (complete all before posting)

### Product
- [ ] [Live demo](https://ai-content-factory-iota.vercel.app) loads and completes a pipeline
- [ ] HITL review flow works end-to-end
- [ ] No obvious console errors on demo path
- [ ] `MOCK_LLM` behavior documented if demo uses stubs

### README
- [ ] Hook + badges at top of README
- [ ] Demo GIF in README (`docs/assets/demo.gif`) — **strongly recommended**
- [ ] Quick start works on fresh clone (`make install && make up && make test`)
- [ ] Link to [DEPLOYMENT.md](../DEPLOYMENT.md)

### GitHub metadata
- [ ] Repo description set
- [ ] Topics: `langgraph`, `multi-agent`, `fastapi`, `nextjs`, `rag`, `human-in-the-loop`
- [ ] Profile README live at [github.com/vpeetla-ai](https://github.com/vpeetla-ai)
- [ ] 3 repos pinned on profile

### Profile
- [ ] GitHub bio links to venkat-ai.com or flagship repo
- [ ] Ready to respond to HN comments within 1–2 hours of posting

## HN submission template

**Title:**
```
Show HN: AI Content Factory – multi-agent content pipeline with human-in-the-loop
```

**URL:** `https://github.com/vpeetla-ai/ai-content-factory`

**First comment (post immediately after submit):**

```
Author here. AI Content Factory is an open-source reference for production multi-agent content workflows.

What it does:
- Research agent with RAG (Qdrant)
- Content agent drafts for LinkedIn, Substack, Medium, Instagram, X
- Parallel SEO + visual enrichment
- Human-in-the-loop gate before publish (LangGraph interrupt)
- Deploys on free-tier cloud (Render + Vercel + Neon + Upstash)

Live demo: https://ai-content-factory-iota.vercel.app
Deploy guide: https://github.com/vpeetla-ai/ai-content-factory/blob/main/docs/DEPLOYMENT.md

Part of a larger open-source series (agent patterns, enterprise RAG, AgentOps): https://github.com/vpeetla-ai

Happy to answer questions on architecture, HITL design, or the free-first stack choices.
```

## During the launch

- Respond to every comment within 2 hours if possible
- Be technical, humble, specific — avoid marketing tone
- Link to relevant docs, not generic homepage
- If someone reports a bug, acknowledge and open a GitHub issue publicly

## After Show HN

- [ ] Thank commenters on HN
- [ ] Capture FAQ → add to README or Discussions
- [ ] Tweet/LinkedIn thread: "We hit HN — here's what we learned"
- [ ] Submit PR to `awesome-langchain` / `awesome-ai-agents` if traction is good

## Do not

- Ask for stars directly on HN (community backlash)
- Post duplicate submissions within 6 months
- Submit with broken demo or missing README quick start
