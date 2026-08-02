"use client";

import { useQuery, useMutation } from "@tanstack/react-query";
import { useState } from "react";
import { api } from "@/lib/api";

interface HitlDraft {
  id: string;
  platform: string;
  draft_content: string;
  hook_variant?: string;
  char_count: number;
}

interface MediaAsset {
  url: string;
  prompt?: string;
  index?: number;
  content_type?: string;
}

interface QualityScore {
  pass?: boolean;
  score?: number;
  issues?: string[];
  char_count?: number;
}

interface HitlReviewResponse {
  drafts: HitlDraft[];
  media_assets?: MediaAsset[];
  image_prompts?: string[];
  quality_scores?: Record<string, QualityScore>;
}

interface Props {
  runId: string;
  onComplete: () => void;
}

export function HITLReview({ runId, onComplete }: Props) {
  const [copiedUrl, setCopiedUrl] = useState<string | null>(null);
  const { data: review, refetch } = useQuery({
    queryKey: ["hitl", runId],
    queryFn: () => api.hitl.review(runId) as Promise<HitlReviewResponse>,
  });

  const approveMutation = useMutation({
    mutationFn: () =>
      api.hitl.approve(
        runId,
        (review?.drafts || []).map((d) => ({
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

  const assets = review?.media_assets || [];
  const prompts = review?.image_prompts || [];
  const scores = review?.quality_scores || {};

  const copyUrl = async (url: string) => {
    try {
      await navigator.clipboard.writeText(url);
      setCopiedUrl(url);
      setTimeout(() => setCopiedUrl(null), 1500);
    } catch {
      /* clipboard may be blocked */
    }
  };

  return (
    <section className="bg-panel border border-green-200 rounded-xl p-6 shadow-card">
      <h2 className="text-sm font-semibold uppercase tracking-wider text-green-400 mb-4">
        Human Review (HITL Gate)
      </h2>

      {(assets.length > 0 || prompts.length > 0) && (
        <div className="mb-5 rounded-lg border border-border bg-surface p-4">
          <p className="mb-3 text-xs font-semibold uppercase tracking-wider text-slate-500">
            Visual media
          </p>
          {assets.length > 0 ? (
            <div className="grid gap-3 sm:grid-cols-2">
              {assets.map((asset) => (
                <figure
                  key={asset.url}
                  className="overflow-hidden rounded-lg border border-slate-200 bg-white"
                >
                  {/* SVG cards from R2 — public URL when configured */}
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={asset.url}
                    alt={asset.prompt || "Visual card"}
                    className="h-36 w-full object-cover object-left bg-slate-900"
                  />
                  <figcaption className="space-y-2 p-3">
                    <p className="line-clamp-2 text-xs text-slate-600">
                      {asset.prompt || "Generated visual card"}
                    </p>
                    <div className="flex flex-wrap gap-2">
                      <a
                        href={asset.url}
                        target="_blank"
                        rel="noreferrer"
                        className="text-xs font-medium text-teal-700 underline underline-offset-2"
                      >
                        Open
                      </a>
                      <button
                        type="button"
                        onClick={() => copyUrl(asset.url)}
                        className="text-xs font-medium text-slate-600 hover:text-slate-900"
                      >
                        {copiedUrl === asset.url ? "Copied" : "Copy URL"}
                      </button>
                    </div>
                  </figcaption>
                </figure>
              ))}
            </div>
          ) : (
            <ul className="space-y-1 text-xs text-slate-600">
              {prompts.map((p, i) => (
                <li key={`${i}-${p.slice(0, 24)}`}>
                  <span className="font-medium text-slate-500">Prompt {i + 1}:</span> {p}
                </li>
              ))}
              <li className="pt-1 text-slate-400">
                R2 not configured — prompts only (set R2_* + R2_PUBLIC_URL to host cards).
              </li>
            </ul>
          )}
        </div>
      )}

      <div className="space-y-4">
        {(review?.drafts || []).map((draft) => {
          const q = scores[draft.platform];
          return (
            <div key={draft.id} className="bg-surface rounded-lg p-4 border border-border">
              <div className="flex justify-between mb-2 gap-2">
                <span className="text-xs font-bold uppercase text-accent">{draft.platform}</span>
                <span className="text-xs text-muted">{draft.char_count} chars</span>
              </div>
              {q && (
                <p
                  className={`mb-2 text-xs ${
                    q.pass ? "text-emerald-600" : "text-amber-700"
                  }`}
                >
                  Rubric {q.pass ? "pass" : "needs edit"}
                  {typeof q.score === "number" ? ` · score ${q.score}` : ""}
                  {q.issues?.length ? ` · ${q.issues.join(", ")}` : ""}
                </p>
              )}
              {draft.hook_variant && (
                <p className="text-xs text-teal mb-2">Hook: {draft.hook_variant}</p>
              )}
              <p className="text-sm text-slate-700 whitespace-pre-wrap">{draft.draft_content}</p>
            </div>
          );
        })}
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
