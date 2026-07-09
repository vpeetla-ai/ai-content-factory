"use client";

import { useCallback, useEffect, useState } from "react";

export type OpsMetrics = {
  service: string;
  collected_at?: string;
  total_runs: number;
  success_rate_pct: number;
  p95_latency_ms: number | null;
  active_entities: number;
  slo: { target_uptime_pct: number; success_target_pct: number };
  extra?: Record<string, unknown>;
};

export type ArchitectLayer = {
  tier: string;
  name: string;
  role: string;
  components: string[];
};

export type Tradeoff = {
  decision: string;
  gain: string;
  trade: string;
};

export type AdrLink = {
  title: string;
  href: string;
};

type MetricLabels = {
  runs?: string;
  entities?: string;
  latency?: string;
};

type Props = {
  tagline: string;
  layers: ArchitectLayer[];
  tradeoffs: Tradeoff[];
  metricsUrl: string;
  metricLabels?: MetricLabels;
  eagleEyeNote?: string;
  adrLinks?: AdrLink[];
  docsLinks?: AdrLink[];
};

type MetricsState = "loading" | "live" | "failed";

export function ArchitectOverview({
  tagline,
  layers,
  tradeoffs,
  metricsUrl,
  metricLabels,
  eagleEyeNote,
  adrLinks,
  docsLinks,
}: Props) {
  const [metrics, setMetrics] = useState<OpsMetrics | null>(null);
  const [metricsState, setMetricsState] = useState<MetricsState>("loading");

  const loadMetrics = useCallback(() => {
    setMetricsState("loading");
    fetch(metricsUrl, { cache: "no-store" })
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(String(r.status)))))
      .then((data) => {
        setMetrics(normalizeMetrics(data));
        setMetricsState("live");
      })
      .catch(() => {
        setMetrics(null);
        setMetricsState("failed");
      });
  }, [metricsUrl]);

  useEffect(() => {
    loadMetrics();
  }, [loadMetrics]);

  const labels = {
    runs: metricLabels?.runs ?? "Total runs",
    entities: metricLabels?.entities ?? "Active entities",
    latency: metricLabels?.latency ?? "P95 latency",
  };

  const hasDocs = Boolean(adrLinks?.length || docsLinks?.length);

  return (
    <div className="space-y-8">
      <nav
        className="sticky top-0 z-10 -mx-1 flex flex-wrap gap-2 rounded-lg border border-slate-200 bg-white/95 px-3 py-2 shadow-sm backdrop-blur"
        aria-label="Architecture sections"
      >
        {[
          { href: "#ao-stack", label: "Stack" },
          { href: "#ao-tradeoffs", label: "Tradeoffs" },
          ...(hasDocs ? [{ href: "#ao-adrs", label: "ADRs" }] : []),
          { href: "#ao-metrics", label: "Metrics" },
        ].map((item) => (
          <a
            key={item.href}
            href={item.href}
            className="rounded-md px-2.5 py-1 text-xs font-semibold text-slate-600 hover:bg-slate-50 hover:text-slate-900"
          >
            {item.label}
          </a>
        ))}
      </nav>

      <section id="ao-stack" className="scroll-mt-16 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <SectionLabel>Eagle-eye architecture</SectionLabel>
        <h2 className="text-lg font-semibold text-slate-900">How the system is wired</h2>
        <p className="mt-2 max-w-3xl text-sm leading-relaxed text-slate-600">{tagline}</p>
        {eagleEyeNote ? <p className="mt-3 text-sm font-medium text-teal-700">{eagleEyeNote}</p> : null}
        <div className="mt-6 grid gap-3">
          {layers.map((layer) => (
            <div
              key={layer.name}
              className="grid items-start gap-3 rounded-lg border border-slate-100 bg-slate-50/80 p-4 md:grid-cols-[72px_160px_1fr]"
            >
              <span className="text-[0.65rem] font-bold uppercase tracking-wider text-teal-700">{layer.tier}</span>
              <div>
                <p className="font-semibold text-slate-900">{layer.name}</p>
                <p className="mt-0.5 text-xs text-slate-500">{layer.role}</p>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {layer.components.map((c) => (
                  <span
                    key={c}
                    className="rounded-md border border-slate-200 bg-white px-2 py-0.5 text-xs text-slate-600"
                  >
                    {c}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      <section id="ao-tradeoffs" className="scroll-mt-16 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <SectionLabel>Principal tradeoffs</SectionLabel>
        <h2 className="text-lg font-semibold text-slate-900">Decisions with explicit costs</h2>
        <div className="mt-5 grid gap-4 md:grid-cols-2">
          {tradeoffs.map((t) => (
            <div key={t.decision} className="rounded-lg border border-slate-100 bg-slate-50/50 p-4">
              <p className="font-semibold text-slate-900">{t.decision}</p>
              <p className="mt-2 text-sm text-slate-600">
                <span className="font-semibold text-emerald-700">Gain</span> — {t.gain}
              </p>
              <p className="mt-1 text-sm text-slate-600">
                <span className="font-semibold text-amber-700">Trade</span> — {t.trade}
              </p>
            </div>
          ))}
        </div>
      </section>

      {hasDocs ? (
        <section id="ao-adrs" className="scroll-mt-16 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <SectionLabel>Architecture record</SectionLabel>
          <h2 className="text-lg font-semibold text-slate-900">ADRs, case studies, and SLOs</h2>
          <ul className="mt-4 space-y-2">
            {adrLinks?.map((link) => (
              <li key={link.href}>
                <a
                  href={link.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm font-medium text-teal-700 hover:text-teal-800"
                >
                  {link.title} →
                </a>
              </li>
            ))}
            {docsLinks?.map((link) => (
              <li key={link.href}>
                <a
                  href={link.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm text-slate-600 hover:text-slate-900"
                >
                  {link.title} →
                </a>
              </li>
            ))}
          </ul>
        </section>
      ) : null}

      <section id="ao-metrics" className="scroll-mt-16 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <SectionLabel>Production metrics</SectionLabel>
        <h2 className="text-lg font-semibold text-slate-900">Live operational proof</h2>
        {metricsState === "live" && metrics ? (
          <>
            <div className="mt-5 grid grid-cols-2 gap-4 md:grid-cols-4">
              <MetricCard label={labels.runs} value={String(metrics.total_runs)} />
              <MetricCard label="Success rate" value={`${metrics.success_rate_pct}%`} />
              <MetricCard
                label={labels.latency}
                value={metrics.p95_latency_ms != null ? `${metrics.p95_latency_ms}ms` : "—"}
              />
              <MetricCard label={labels.entities} value={String(metrics.active_entities)} />
            </div>
            <p className="mt-4 font-mono text-xs text-slate-500">
              {metricsUrl.replace(/^https?:\/\/[^/]+/, "")} · SLO {metrics.slo.success_target_pct}% success ·{" "}
              {metrics.slo.target_uptime_pct}% uptime target
            </p>
          </>
        ) : metricsState === "loading" ? (
          <p className="mt-4 text-sm text-slate-500">Loading live metrics…</p>
        ) : (
          <div className="mt-4 flex flex-wrap items-center gap-3">
            <p className="text-sm text-slate-600">
              Metrics unavailable — API may be waking from idle (~30s on free tier).
            </p>
            <button
              type="button"
              onClick={loadMetrics}
              className="rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-sm font-semibold text-slate-700 hover:bg-slate-50"
            >
              Retry
            </button>
          </div>
        )}
      </section>
    </div>
  );
}

function SectionLabel({ children }: { children: React.ReactNode }) {
  return (
    <p className="mb-2 text-[0.68rem] font-semibold uppercase tracking-[0.14em] text-slate-500">{children}</p>
  );
}

function MetricCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-slate-100 bg-slate-50 p-4">
      <p className="text-xs font-medium text-slate-500">{label}</p>
      <p className="mt-1 text-2xl font-semibold tabular-nums text-slate-900">{value}</p>
    </div>
  );
}

function normalizeMetrics(data: Record<string, unknown>): OpsMetrics {
  const sloRaw = (data.slo as Record<string, unknown>) || {};
  const successTarget =
    (sloRaw.success_target_pct as number) ??
    (sloRaw.pipeline_success_target_pct as number) ??
    95.0;

  return {
    service: String(data.service ?? "unknown"),
    collected_at: data.collected_at as string | undefined,
    total_runs: Number(data.total_runs ?? data.sample_size ?? data.total ?? 0),
    success_rate_pct: Number(data.success_rate_pct ?? 100 - Number(data.failure_rate_pct ?? 0)),
    p95_latency_ms:
      (data.p95_latency_ms as number | null) ??
      (data.p95_node_latency_ms as number | null) ??
      (data.p95_ms as number | null) ??
      null,
    active_entities: Number(data.active_entities ?? data.invited_users ?? data.active_users ?? 0),
    slo: {
      target_uptime_pct: Number(sloRaw.target_uptime_pct ?? 99.5),
      success_target_pct: successTarget,
    },
    extra: (data.extra as Record<string, unknown>) ?? undefined,
  };
}
