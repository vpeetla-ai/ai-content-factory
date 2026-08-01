---
name: portfolio-adr
description: >-
  Write ADRs, case studies, and portfolio copy for ai-architecture-portfolio and
  venkat-ai-portfolio. Use when documenting decisions, updating ecosystem pages,
  or syncing GitHub profile README with live demos.
---

# Portfolio & ADR Writing

## Voice (required)

Same bar as the interview playbook: **Principal peer who shipped this**, not brochure/template bot.
Canonical guide: `ai-architecture-portfolio/docs/HUMAN_VOICE_PASS.md` (also mirrored in this skills pack when present).

- Decision first · scar second · proof third
- Add `## In one breath (panel)` — one spoken sentence
- Refuse demo theater; label Demo vs Strict / P vs O
- Ban: leverage, comprehensive, seamless, cutting-edge, utilize, holistic, synergies

## ADR template

```markdown
# ADR-NNN: Title

## Status
Proposed | Accepted | Superseded

## In one breath (panel)
I'd … (one spoken sentence)

## Context
What failed / scared us into deciding — human, not “this document outlines”.

## Decision
What we chose (plain English, then bullets if needed).

## Consequences
Trade-offs, what we gave up, what we'd reverse on.

## Links
Live demo, repo, related ADR
```

## Case study structure

1. Problem (1 paragraph with a scar)
2. Architecture diagram (mermaid or link)
3. Key decisions (3–5 bullets with ADR links)
4. Live demo URL (must work)
5. What we'd do differently / limitations

## Honesty rules

- **Implemented** vs **Planned** vs **Demo-only** — separate columns in README tables
- No fake metrics; cite eval gates and test counts instead
- Never imply Lucid production ran public repo binaries

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
