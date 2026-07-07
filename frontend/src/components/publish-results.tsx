"use client";

import { PublishResult } from "@/lib/store";

interface Props {
  results: PublishResult[];
}

export function PublishResults({ results }: Props) {
  if (results.length === 0) return null;

  return (
    <section className="bg-panel border border-border rounded-xl p-6 shadow-card">
      <h2 className="text-sm font-semibold uppercase tracking-wider text-muted mb-4">
        Publish Results
      </h2>
      <div className="space-y-2">
        {results.map((r) => (
          <div
            key={r.platform}
            className="flex items-center justify-between gap-3 bg-surface border border-border rounded-lg p-3 text-sm"
          >
            <span className="font-mono text-xs uppercase text-muted w-20 shrink-0">{r.platform}</span>
            {r.notSupported ? (
              <>
                <span className="text-xs text-amber-400 flex-1">
                  No auto-publish API available — copy and paste manually
                </span>
                <button
                  onClick={() => navigator.clipboard.writeText(r.draftContent)}
                  className="px-3 py-1 rounded bg-accent/20 hover:bg-accent/40 text-accent text-xs font-semibold"
                >
                  Copy draft
                </button>
              </>
            ) : (
              <a
                href={r.url}
                target="_blank"
                rel="noreferrer"
                className="text-teal text-xs truncate flex-1 hover:underline"
              >
                {r.url}
              </a>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}
