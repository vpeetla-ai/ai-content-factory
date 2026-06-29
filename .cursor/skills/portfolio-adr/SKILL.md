---
name: portfolio-adr
description: >-
  Write ADRs, case studies, and portfolio copy for ai-architecture-portfolio and
  venkat-ai-portfolio. Use when documenting decisions, updating ecosystem pages,
  or syncing GitHub profile README with live demos.
---

# Portfolio & ADR Writing

## ADR template

```markdown
# ADR-NNN: Title

## Status
Proposed | Accepted | Superseded

## Context
What problem and constraints?

## Decision
What we chose.

## Consequences
Trade-offs, what we gave up.

## Links
Live demo, repo, related ADR
```

## Case study structure

1. Problem (1 paragraph)
2. Architecture diagram (mermaid or link)
3. Key decisions (3–5 bullets with ADR links)
4. Live demo URL (must work)
5. What we'd do differently

## Honesty rules

- **Implemented** vs **Planned** vs **Demo-only** — separate columns in README tables
- No fake metrics; cite eval gates and test counts instead

## Sync targets

| Artifact | Repo |
|----------|------|
| ADRs, case studies | ai-architecture-portfolio |
| venkat-ai.com pages | venkat-ai-portfolio |
| GitHub profile | vpeetla-ai/README.md |

## Essay anchor

`from-multi-agent-os-to-agent-governance` — link from profile + portfolio

## After writing

- Verify all demo URLs return 200
- Update stack map in `ecosystem.ts` if layer changed
