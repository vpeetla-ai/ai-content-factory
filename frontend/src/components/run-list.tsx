interface Run {
  run_id: string;
  status: string;
  topic: string;
}

interface Props {
  runs: Run[];
  onSelect: (id: string) => void;
}

export function RunList({ runs, onSelect }: Props) {
  return (
    <section className="bg-panel border border-white/10 rounded-xl p-6">
      <h2 className="text-sm font-semibold uppercase tracking-wider text-muted mb-4">
        Recent Runs
      </h2>
      {runs.length === 0 ? (
        <p className="text-sm text-muted">No runs yet</p>
      ) : (
        <ul className="space-y-2">
          {runs.map((run) => (
            <li key={run.run_id}>
              <button
                onClick={() => onSelect(run.run_id)}
                className="w-full text-left p-3 rounded-lg bg-surface border border-white/5 hover:border-accent/50 transition"
              >
                <p className="text-sm font-medium truncate">{run.topic}</p>
                <p className="text-xs text-muted mt-1 font-mono">{run.status}</p>
              </button>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
