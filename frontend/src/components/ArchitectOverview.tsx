"use client";

import { useEffect, useState } from "react";

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
};

export function ArchitectOverview({
  tagline,
  layers,
  tradeoffs,
  metricsUrl,
  metricLabels,
  eagleEyeNote,
}: Props) {
  const [metrics, setMetrics] = useState<OpsMetrics | null>(null);

  useEffect(() => {
    fetch(metricsUrl, { cache: "no-store" })
      .then((r) => (r.ok ? r.json() : null))
      .then((data) => data && setMetrics(normalizeMetrics(data)))
      .catch(() => null);
  }, [metricsUrl]);

  const labels = {
    runs: metricLabels?.runs ?? "Total runs",
    entities: metricLabels?.entities ?? "Active entities",
    latency: metricLabels?.latency ?? "P95 latency",
  };

  return (
    <div className="space-y-12">
      <section>
        <p className="text-xs font-medium uppercase tracking-widest text-muted mb-2">Eagle-eye view</p>
        <h2 className="text-2xl font-bold mb-2">Architecture at a glance</h2>
        <p className="text-muted max-w-3xl mb-6">{tagline}</p>
        {eagleEyeNote && <p className="text-sm text-accent mb-6">{eagleEyeNote}</p>}
        <div className="grid gap-3">
          {layers.map((layer) => (
            <div
              key={layer.name}
              className="grid md:grid-cols-[88px_140px_1fr] gap-3 p-4 rounded-xl border border-border bg-surface items-start"
            >
              <span className="text-xs font-semibold uppercase tracking-wide text-accent">{layer.tier}</span>
              <div>
                <p className="font-semibold">{layer.name}</p>
                <p className="text-xs text-muted mt-0.5">{layer.role}</p>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {layer.components.map((c) => (
                  <span key={c} className="text-xs px-2 py-0.5 rounded-md bg-bg border border-border text-muted">
                    {c}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      <section>
        <p className="text-xs font-medium uppercase tracking-widest text-muted mb-2">Principal tradeoffs</p>
        <h2 className="text-2xl font-bold mb-4">Decisions, not defaults</h2>
        <div className="grid md:grid-cols-2 gap-4">
          {tradeoffs.map((t) => (
            <div key={t.decision} className="p-5 rounded-xl border border-border bg-surface">
              <p className="font-semibold mb-2">{t.decision}</p>
              <p className="text-sm text-muted">
                <span className="text-teal font-medium">Gain:</span> {t.gain}
              </p>
              <p className="text-sm text-muted mt-1">
                <span className="text-amber-400/90 font-medium">Trade:</span> {t.trade}
              </p>
            </div>
          ))}
        </div>
      </section>

      {metrics && (
        <section>
          <p className="text-xs font-medium uppercase tracking-widest text-muted mb-2">Production metrics</p>
          <h2 className="text-2xl font-bold mb-4">Live from the API — not slide-deck numbers</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <MetricCard label={labels.runs} value={String(metrics.total_runs)} />
            <MetricCard label="Success rate" value={`${metrics.success_rate_pct}%`} />
            <MetricCard
              label={labels.latency}
              value={metrics.p95_latency_ms != null ? `${metrics.p95_latency_ms}ms` : "—"}
            />
            <MetricCard label={labels.entities} value={String(metrics.active_entities)} />
          </div>
          <p className="text-xs text-muted mt-3">
            Live from <code className="text-accent">{metricsUrl.replace(/^https?:\/\/[^/]+/, "")}</code> · SLO target{" "}
            {metrics.slo.success_target_pct}% success · {metrics.slo.target_uptime_pct}% uptime
          </p>
        </section>
      )}
    </div>
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
    success_rate_pct: Number(
      data.success_rate_pct ?? (100 - Number(data.failure_rate_pct ?? 0))
    ),
    p95_latency_ms:
      (data.p95_latency_ms as number | null) ??
      (data.p95_node_latency_ms as number | null) ??
      (data.p95_ms as number | null) ??
      null,
    active_entities: Number(
      data.active_entities ?? data.invited_users ?? data.active_users ?? 0
    ),
    slo: {
      target_uptime_pct: Number(sloRaw.target_uptime_pct ?? 99.5),
      success_target_pct: successTarget,
    },
    extra: (data.extra as Record<string, unknown>) ?? undefined,
  };
}
