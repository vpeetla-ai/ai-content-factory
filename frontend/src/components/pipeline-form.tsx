interface Props {
  topic: string;
  onTopicChange: (v: string) => void;
  onStart: () => void;
  loading: boolean;
}

export function PipelineForm({ topic, onTopicChange, onStart, loading }: Props) {
  return (
    <section className="bg-panel border border-white/10 rounded-xl p-6">
      <h2 className="text-sm font-semibold uppercase tracking-wider text-muted mb-4">
        New Pipeline Run
      </h2>
      <textarea
        className="w-full bg-surface border border-white/10 rounded-lg p-3 text-sm min-h-[100px] focus:outline-none focus:border-accent"
        placeholder="Enter content topic (e.g. 'AI agents in enterprise content workflows')"
        value={topic}
        onChange={(e) => onTopicChange(e.target.value)}
      />
      <div className="mt-4 flex flex-wrap gap-2">
        {["linkedin", "substack", "medium", "x", "instagram"].map((p) => (
          <span key={p} className="text-xs px-2 py-1 rounded bg-surface border border-white/10 text-muted">
            {p}
          </span>
        ))}
      </div>
      <button
        onClick={onStart}
        disabled={!topic.trim() || loading}
        className="mt-4 px-6 py-2 rounded-lg bg-accent hover:bg-accent/80 disabled:opacity-50 text-white font-semibold text-sm transition"
      >
        {loading ? "Running agents…" : "Start Pipeline"}
      </button>
    </section>
  );
}
