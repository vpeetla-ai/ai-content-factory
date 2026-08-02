"use client";

import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

export function SchedulePanel() {
  const { data, isLoading, isError, refetch, isFetching } = useQuery({
    queryKey: ["ops-schedule"],
    queryFn: () => api.ops.schedule(),
    retry: 1,
    staleTime: 30_000,
  });

  return (
    <section className="bg-panel border border-border rounded-xl p-6 shadow-card">
      <div className="mb-3 flex items-center justify-between gap-2">
        <h2 className="text-sm font-semibold uppercase tracking-wider text-muted">
          Pipeline schedule
        </h2>
        <button
          type="button"
          onClick={() => refetch()}
          className="text-xs font-medium text-teal-700 hover:underline"
          disabled={isFetching}
        >
          {isFetching ? "Refreshing…" : "Refresh"}
        </button>
      </div>

      {isLoading ? (
        <p className="text-xs text-muted">Loading schedule…</p>
      ) : isError || !data ? (
        <div className="space-y-2">
          <p className="text-xs text-muted">
            Schedule unavailable — API may be waking (~30s on free tier).
          </p>
          <button
            type="button"
            onClick={() => refetch()}
            className="rounded-lg border border-border bg-surface px-3 py-1.5 text-xs font-semibold text-slate-700"
          >
            Retry
          </button>
        </div>
      ) : (
        <dl className="grid gap-2 text-sm">
          <div className="flex justify-between gap-3">
            <dt className="text-muted">Status</dt>
            <dd className="font-semibold text-slate-800">
              {data.enabled ? "Enabled" : "Disabled"}
            </dd>
          </div>
          <div className="flex justify-between gap-3">
            <dt className="text-muted">Cron (UTC)</dt>
            <dd className="font-mono text-xs text-slate-800">{data.cron || "—"}</dd>
          </div>
          <div className="flex justify-between gap-3">
            <dt className="text-muted">Topic</dt>
            <dd className="truncate text-right text-slate-800" title={data.topic}>
              {data.topic || "—"}
            </dd>
          </div>
          <div className="flex justify-between gap-3">
            <dt className="text-muted">Platforms</dt>
            <dd className="text-right text-slate-800">
              {(data.platforms || []).length ? data.platforms.join(", ") : "—"}
            </dd>
          </div>
        </dl>
      )}

      <p className="mt-3 text-xs text-muted">
        Read-only product surface. Mutations stay env-only (
        <code className="text-[0.7rem]">CRON_PIPELINE_ENABLED</code>
        ); gateway authorizes <code className="text-[0.7rem]">schedule_pipeline</code>.
      </p>
    </section>
  );
}
