interface Props {
  logs: string[];
  status: string | null;
  runId: string | null;
}

const STATUS_COLORS: Record<string, string> = {
  running: "text-teal",
  hitl_wait: "text-amber-400",
  done: "text-green-400",
  error: "text-rose-400",
};

export function AgentLog({ logs, status, runId }: Props) {
  return (
    <section className="bg-panel border border-border rounded-xl p-6 shadow-card">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-sm font-semibold uppercase tracking-wider text-muted">
          Agent Orchestration
        </h2>
        {status && (
          <span className={`text-xs font-mono uppercase ${STATUS_COLORS[status] || "text-muted"}`}>
            {status}
          </span>
        )}
      </div>
      {runId && (
        <p className="text-xs font-mono text-muted mb-3 truncate">run: {runId}</p>
      )}
      <div className="bg-surface rounded-lg p-3 font-mono text-xs space-y-1 max-h-64 overflow-y-auto">
        {logs.length === 0 ? (
          <p className="text-muted">Waiting for pipeline…</p>
        ) : (
          logs.map((log, i) => (
            <div key={i} className="text-slate-700">
              {log}
            </div>
          ))
        )}
      </div>
    </section>
  );
}
