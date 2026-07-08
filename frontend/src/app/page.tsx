"use client";

import Link from "next/link";
import { ArchitectOverview } from "@/components/ArchitectOverview";

const API_BASE = process.env.NEXT_PUBLIC_API_URL?.replace(/\/api\/v1$/, "") || "http://localhost:8000";

const LAYERS = [
  {
    tier: "L1",
    name: "Experience",
    role: "Human-in-the-loop content ops",
    components: ["Next.js dashboard", "Clerk auth", "Platform drafts UI"],
  },
  {
    tier: "L2",
    name: "Orchestration",
    role: "Multi-agent LangGraph pipeline",
    components: ["Research agent", "Writer agents", "HITL interrupt_before"],
  },
  {
    tier: "L3",
    name: "Governance",
    role: "Side effects gated before publish",
    components: ["AegisAI gateway", "OAuth publish", "Invite-only access"],
  },
  {
    tier: "L4",
    name: "Knowledge + Ops",
    role: "Grounded generation with proof",
    components: ["Hybrid RAG", "Langfuse traces", "Golden eval CI"],
  },
];

const TRADEOFFS = [
  {
    decision: "HITL before every publish",
    gain: "Zero unauthorized side effects; audit-ready approvals",
    trade: "Higher latency vs fully autonomous posting",
  },
  {
    decision: "Separate orchestration from governance",
    gain: "Swap VAP graphs without rewriting policy engine",
    trade: "Two services to deploy and observe",
  },
  {
    decision: "Postgres + trace tables over log-only ops",
    gain: "Public /ops/metrics without exposing PII",
    trade: "Schema migrations vs serverless-only demos",
  },
  {
    decision: "Mock LLM default on Render free tier",
    gain: "Portfolio demos stay up without GPU spend",
    trade: "P95 latency numbers reflect mock path, not prod LLM",
  },
];

export default function LandingPage() {
  return (
    <main className="min-h-screen bg-bg text-fg">
      <header className="border-b border-border">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-accent to-teal flex items-center justify-center font-bold text-white text-sm">
              ⚡
            </div>
            <span className="font-semibold">AI Content Factory</span>
          </div>
          <nav className="flex items-center gap-4 text-sm">
            <a
              href="https://github.com/vpeetla-ai/ai-content-factory"
              className="text-muted hover:text-fg"
              target="_blank"
              rel="noopener noreferrer"
            >
              GitHub
            </a>
            <Link href="/sign-in" className="px-3 py-1.5 rounded-lg bg-accent text-white font-medium">
              Sign in
            </Link>
          </nav>
        </div>
      </header>

      <section className="max-w-5xl mx-auto px-6 py-16">
        <p className="text-accent text-sm font-medium mb-3">Governed multi-agent content pipeline</p>
        <h1 className="text-4xl md:text-5xl font-bold tracking-tight mb-6 max-w-3xl">
          One topic → five platform drafts → human approval → governed publish
        </h1>
        <p className="text-lg text-muted max-w-2xl mb-8">
          Principal-architect lens: orchestration (LangGraph), governance (AegisAI), RAG research,
          and trace-linked LLMOps — not a single-prompt wrapper.
        </p>
        <div className="flex flex-wrap gap-3">
          <Link href="/sign-in" className="px-5 py-2.5 rounded-lg bg-accent text-white font-medium">
            Try the demo
          </Link>
          <Link href="/dashboard" className="px-5 py-2.5 rounded-lg border border-border hover:bg-surface">
            Open dashboard
          </Link>
          <a
            href="https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/case-studies/ai-content-factory.md"
            className="px-5 py-2.5 rounded-lg border border-border hover:bg-surface"
            target="_blank"
            rel="noopener noreferrer"
          >
            Case study
          </a>
        </div>
      </section>

      <section className="max-w-5xl mx-auto px-6 pb-16">
        <ArchitectOverview
          tagline="Four layers separate what agents do (orchestration) from what they may do (governance) and what they know (RAG). Metrics prove the pipeline runs in production."
          layers={LAYERS}
          tradeoffs={TRADEOFFS}
          metricsUrl={`${API_BASE}/api/v1/ops/metrics`}
          metricLabels={{ runs: "Pipeline runs", entities: "Invited users", latency: "P95 node latency" }}
          eagleEyeNote="Reference pattern for the vpeetla-ai content application layer — pairs with VAP orchestration and AegisAI gateway."
        />
      </section>

      <footer className="border-t border-border py-8">
        <div className="max-w-5xl mx-auto px-6 flex flex-wrap gap-4 text-sm text-muted">
          <Link href="/privacy">Privacy</Link>
          <Link href="/terms">Terms</Link>
          <a href="https://venkat-ai.com/work" target="_blank" rel="noopener noreferrer">
            Portfolio
          </a>
        </div>
      </footer>
    </main>
  );
}
