"use client";

import Link from "next/link";
import { useQuery } from "@tanstack/react-query";

type OpsMetrics = {
  service: string;
  total_runs: number;
  completed_runs: number;
  success_rate_pct: number;
  invited_users: number;
  avg_pipeline_latency_ms: number | null;
  p95_node_latency_ms: number | null;
  total_cost_usd: number;
  slo: { target_uptime_pct: number; pipeline_success_target_pct: number };
};

async function fetchOpsMetrics(): Promise<OpsMetrics | null> {
  const base = process.env.NEXT_PUBLIC_API_URL?.replace(/\/api\/v1$/, "") || "http://localhost:8000";
  try {
    const res = await fetch(`${base}/api/v1/ops/metrics`);
    if (!res.ok) return null;
    return res.json();
  } catch {
    return null;
  }
}

export default function LandingPage() {
  const { data: metrics } = useQuery({
    queryKey: ["ops-metrics"],
    queryFn: fetchOpsMetrics,
    staleTime: 60_000,
  });

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
          LangGraph orchestration, RAG research, HITL gates, AegisAI gateway, and trace-linked
          observability — not a single-prompt wrapper.
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

      <section className="max-w-5xl mx-auto px-6 pb-12">
        <div className="grid md:grid-cols-3 gap-4">
          {[
            { title: "Research + RAG", body: "Hybrid retrieval grounds drafts before generation." },
            { title: "HITL before publish", body: "interrupt_before gate — humans approve every platform." },
            { title: "Trace-linked LLMOps", body: "Langfuse spans at system, trace, and node levels." },
          ].map((card) => (
            <div key={card.title} className="p-5 rounded-xl border border-border bg-surface">
              <h3 className="font-semibold mb-2">{card.title}</h3>
              <p className="text-sm text-muted">{card.body}</p>
            </div>
          ))}
        </div>
      </section>

      {metrics && (
        <section className="max-w-5xl mx-auto px-6 pb-16">
          <h2 className="text-sm font-medium text-muted uppercase tracking-wide mb-4">Production metrics</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <MetricCard label="Pipeline runs" value={String(metrics.total_runs)} />
            <MetricCard label="Success rate" value={`${metrics.success_rate_pct}%`} />
            <MetricCard
              label="P95 node latency"
              value={metrics.p95_node_latency_ms != null ? `${metrics.p95_node_latency_ms}ms` : "—"}
            />
            <MetricCard label="Invited users" value={String(metrics.invited_users)} />
          </div>
          <p className="text-xs text-muted mt-3">
            Live from <code className="text-accent">/api/v1/ops/metrics</code> · SLO target{" "}
            {metrics.slo.pipeline_success_target_pct}% pipeline success
          </p>
        </section>
      )}

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

function MetricCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="p-4 rounded-xl border border-border bg-surface">
      <p className="text-xs text-muted mb-1">{label}</p>
      <p className="text-2xl font-bold">{value}</p>
    </div>
  );
}
