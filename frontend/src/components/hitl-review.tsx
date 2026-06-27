"use client";

import { useQuery, useMutation } from "@tanstack/react-query";
import { api } from "@/lib/api";

interface Props {
  runId: string;
  onComplete: () => void;
}

export function HITLReview({ runId, onComplete }: Props) {
  const { data: review, refetch } = useQuery({
    queryKey: ["hitl", runId],
    queryFn: () => api.hitl.review(runId),
  });

  const approveMutation = useMutation({
    mutationFn: () =>
      api.hitl.approve(
        runId,
        (review?.drafts || []).map((d: { platform: string; draft_content: string }) => ({
          platform: d.platform,
          approved: true,
          edited_content: d.draft_content,
        }))
      ),
    onSuccess: () => {
      onComplete();
      refetch();
    },
  });

  const rejectMutation = useMutation({
    mutationFn: () => api.hitl.reject(runId),
    onSuccess: onComplete,
  });

  return (
    <section className="bg-panel border border-green-500/30 rounded-xl p-6">
      <h2 className="text-sm font-semibold uppercase tracking-wider text-green-400 mb-4">
        ✋ Human Review (HITL Gate)
      </h2>
      <div className="space-y-4">
        {(review?.drafts || []).map((draft: {
          id: string;
          platform: string;
          draft_content: string;
          hook_variant?: string;
          char_count: number;
        }) => (
          <div key={draft.id} className="bg-surface rounded-lg p-4 border border-white/5">
            <div className="flex justify-between mb-2">
              <span className="text-xs font-bold uppercase text-accent">{draft.platform}</span>
              <span className="text-xs text-muted">{draft.char_count} chars</span>
            </div>
            {draft.hook_variant && (
              <p className="text-xs text-teal mb-2">Hook: {draft.hook_variant}</p>
            )}
            <p className="text-sm text-white/80 whitespace-pre-wrap">{draft.draft_content}</p>
          </div>
        ))}
      </div>
      <div className="flex gap-3 mt-6">
        <button
          onClick={() => approveMutation.mutate()}
          disabled={approveMutation.isPending}
          className="px-4 py-2 rounded-lg bg-green-500/20 border border-green-500/40 text-green-400 text-sm font-semibold hover:bg-green-500/30"
        >
          Approve & Publish
        </button>
        <button
          onClick={() => rejectMutation.mutate()}
          disabled={rejectMutation.isPending}
          className="px-4 py-2 rounded-lg bg-rose-500/20 border border-rose-500/40 text-rose-400 text-sm font-semibold"
        >
          Reject
        </button>
      </div>
    </section>
  );
}
