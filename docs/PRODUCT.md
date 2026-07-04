# Product framing — AI Content Factory

## Who we serve

| Persona | Pain today | What they get |
|---------|------------|---------------|
| **Content lead / editor** | Drafting for 5 platforms is slow and inconsistent | One topic → platform-tailored drafts in one run |
| **Marketing ops** | Fear of rogue AI posting | HITL gate + AegisAI gateway before any publish |
| **Engineering team** | Demo pipelines lack observability | LangGraph + Langfuse + pytest + honest status table |

## Job-to-be-done

> "Turn a approved topic into platform-ready drafts, let humans edit and approve, then publish only what policy allows."

## What we are NOT

- A single ChatGPT prompt wrapper
- Autonomous social posting without human review
- A replacement for brand/legal review on regulated industries
- An auto-publisher for every platform: Substack has no public posting API, Medium deprecated
  its public integration API for new apps, and Instagram publish requires Meta Business app
  review. LinkedIn and X are real auto-publish (OAuth + PKCE); the other three produce a
  copy-ready draft instead of a fake "published" link.

## Architecture (customer view)

```text
Topic in → Research (RAG) → Drafts (5 platforms) → Human review → Gateway → Publish
```

## Trade-offs

| Choice | Why | Cost |
|--------|-----|------|
| HITL before publish | Trust + compliance | Slower than fully autonomous |
| Real OAuth for LinkedIn + X only | Only two platforms have a viable public posting API | Medium/Substack/Instagram are copy-draft export, not auto-publish |
| In-process MCP bridge | Fast to test; Cursor-ready | Stdio MCP server = Phase 4 |
| Gateway fail-open in dev | Local velocity | Must fail-closed in prod |

## Success metrics

- Pipeline completes research → drafts → HITL without error
- Gateway blocks unauthorized publish in tests
- Editor can edit per-platform copy before approve

## Related

- [Case study](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/case-studies/ai-content-factory.md)
- [MCP.md](MCP.md) · [2026 protocol stack essay](docs/content/2026-agent-protocol-stack.md)
