import type { AdrLink, ArchitectLayer, Tradeoff } from "@/components/ArchitectOverview";

export const ACF_API_BASE =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/api\/v1$/, "") || "http://localhost:8000";

export const ACF_LAYERS: ArchitectLayer[] = [
  { tier: "L1", name: "Experience", role: "Human-in-the-loop content ops", components: ["Next.js dashboard", "Clerk auth", "Platform drafts"] },
  { tier: "L2", name: "Orchestration", role: "Multi-agent LangGraph pipeline", components: ["Research", "Writers", "HITL interrupt"] },
  { tier: "L3", name: "Governance", role: "Side effects gated before publish", components: ["AegisAI gateway", "OAuth publish", "Invite access"] },
  { tier: "L4", name: "Knowledge + Ops", role: "Grounded generation with proof", components: ["Hybrid RAG", "Langfuse", "Golden eval CI"] },
];

export const ACF_TRADEOFFS: Tradeoff[] = [
  { decision: "HITL before every publish", gain: "Zero unauthorized side effects; audit-ready approvals", trade: "Higher latency vs fully autonomous posting" },
  { decision: "Separate orchestration from governance", gain: "Swap VAP graphs without rewriting policy engine", trade: "Two services to deploy and observe" },
  { decision: "Postgres + trace tables", gain: "Public /ops/metrics without exposing PII", trade: "Schema migrations vs serverless-only demos" },
  { decision: "Mock LLM on Render free tier", gain: "Portfolio demos stay up without GPU spend", trade: "P95 reflects mock path, not production LLM" },
];

export const ACF_ADR_LINKS: AdrLink[] = [
  {
    title: "ADR-008 — Real publish scope and invite gating",
    href: "https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/adr/ADR-008-real-publish-scope-and-invite-gating.md",
  },
  {
    title: "Case study — AI Content Factory",
    href: "https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/case-studies/ai-content-factory.md",
  },
];

export const ACF_DOCS_LINKS: AdrLink[] = [
  { title: "Architecture (repo)", href: "https://github.com/vpeetla-ai/ai-content-factory/blob/main/docs/ARCHITECTURE.md" },
  { title: "SLO targets", href: "https://github.com/vpeetla-ai/ai-content-factory/blob/main/docs/SLO.md" },
  { title: "FinOps metering", href: "https://github.com/vpeetla-ai/ai-content-factory/blob/main/docs/FINOPS.md" },
];

export const ACF_ARCHITECTURE_PROPS = {
  tagline: "Four layers separate what agents do (orchestration) from what they may do (governance) and what they know (RAG).",
  layers: ACF_LAYERS,
  tradeoffs: ACF_TRADEOFFS,
  metricsUrl: `${ACF_API_BASE}/api/v1/ops/metrics`,
  metricLabels: { runs: "Pipeline runs", entities: "Invited users", latency: "P95 node latency" },
  eagleEyeNote: "Reference application layer in the vpeetla-ai stack — pairs with VAP orchestration and AegisAI gateway.",
  adrLinks: ACF_ADR_LINKS,
  docsLinks: ACF_DOCS_LINKS,
} as const;
