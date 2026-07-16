"use client";

import { useEffect, useRef, useState } from "react";
import type { PhaseId, PhaseStatus } from "@/lib/store";
import { PIPELINE_PHASES } from "@/lib/store";

const PHASE_META: { id: PhaseId; label: string; detail: string }[] = [
  { id: "research", label: "Research", detail: "RAG-grounded brief" },
  { id: "content", label: "Content", detail: "Platform drafts" },
  { id: "enrich", label: "Enrich", detail: "SEO + image prompts" },
  { id: "hitl", label: "HITL", detail: "Human approve" },
  { id: "publish", label: "Publish", detail: "AegisAI gateway" },
];

export type TraceSource = "idle" | "live" | "preview";

type Props = {
  /** Live phase status from SSE/WS store (dashboard). */
  phaseStatus?: Record<PhaseId, PhaseStatus>;
  phaseLatencyMs?: Partial<Record<PhaseId, number>>;
  /** When set, animate a preview replay (public landing). */
  preview?: boolean;
  traceSource?: TraceSource;
  status?: string | null;
  runId?: string | null;
  eventLog?: string[];
  onReplayDone?: () => void;
};

export function ContentPipelineGlassbox({
  phaseStatus,
  phaseLatencyMs = {},
  preview = false,
  traceSource = "idle",
  status = null,
  runId = null,
  eventLog = [],
  onReplayDone,
}: Props) {
  const [previewActive, setPreviewActive] = useState<PhaseId | null>(null);
  const [previewDone, setPreviewDone] = useState<Set<PhaseId>>(new Set());
  const [gate, setGate] = useState(
    "Research → content → enrich → HITL → governed publish — interrupt_before on every platform."
  );
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Public landing: one-shot preview animation (no invented ms)
  useEffect(() => {
    if (!preview) return;
    if (timerRef.current) clearTimeout(timerRef.current);
    setPreviewActive(null);
    setPreviewDone(new Set());
    let i = 0;
    let prev: PhaseId | null = null;
    const step = () => {
      if (i >= PIPELINE_PHASES.length) {
        if (prev) setPreviewDone((d) => new Set(d).add(prev!));
        setPreviewActive(null);
        setGate("Phase map complete — sign in to run a live pipeline with real node latency_ms.");
        onReplayDone?.();
        return;
      }
      const id = PIPELINE_PHASES[i];
      if (prev) setPreviewDone((d) => new Set(d).add(prev!));
      setPreviewActive(id);
      prev = id;
      const meta = PHASE_META.find((p) => p.id === id)!;
      setGate(`${meta.label} — ${meta.detail}`);
      i += 1;
      timerRef.current = setTimeout(step, 420);
    };
    step();
    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, [preview, onReplayDone]);

  // Live dashboard: update gate from phaseStatus
  useEffect(() => {
    if (preview || !phaseStatus) return;
    const active = PIPELINE_PHASES.find((p) => phaseStatus[p] === "active");
    if (active) {
      const meta = PHASE_META.find((p) => p.id === active)!;
      const ms = phaseLatencyMs[active];
      setGate(
        `${meta.label} — ${meta.detail}${ms != null ? ` · last ${ms}ms` : " · running"}`
      );
      return;
    }
    const allDone = PIPELINE_PHASES.every((p) => phaseStatus[p] === "done");
    if (allDone) {
      setGate("Pipeline complete — drafts approved and publish path finished.");
      return;
    }
    if (status === "hitl_wait") {
      setGate("HITL gate — approve each platform before AegisAI allows publish.");
      return;
    }
    if (status === "error") {
      setGate("Pipeline error — inspect the event log and retry.");
      return;
    }
    setGate(
      runId
        ? `Run ${runId.slice(0, 8)}… — waiting for agent events.`
        : "Start a pipeline to stream real research → content → enrich → HITL → publish events."
    );
  }, [preview, phaseStatus, phaseLatencyMs, status, runId]);

  const isActive = (id: PhaseId) =>
    preview ? previewActive === id : phaseStatus?.[id] === "active";
  const isDone = (id: PhaseId) =>
    preview ? previewDone.has(id) : phaseStatus?.[id] === "done";

  const totalMs = PIPELINE_PHASES.reduce((sum, id) => sum + (phaseLatencyMs[id] ?? 0), 0);
  const doneCount = PIPELINE_PHASES.filter((id) => isDone(id)).length;

  const badge =
    traceSource === "live"
      ? "live stream"
      : traceSource === "preview"
        ? "phase preview"
        : "awaiting run";

  return (
    <>
      <div className="gb-center-head">
        <h2>Content pipeline · phase glass-box</h2>
        <span
          className={`gb-source-badge${
            traceSource === "live" ? " live" : traceSource === "preview" ? " fallback" : ""
          }`}
        >
          {badge}
        </span>
      </div>

      <div className="gb-pipeline">
        {PHASE_META.map((p, i) => (
          <span key={p.id} className="gb-pipeline-item">
            {i > 0 ? <span className="gb-agent-arrow" aria-hidden="true">→</span> : null}
            <div
              className={`gb-agent-node${isActive(p.id) ? " gb-active" : ""}${
                isDone(p.id) ? " gb-done" : ""
              }`}
            >
              <span className="gb-agent-idx">{String(i + 1).padStart(2, "0")}</span>
              <div>
                <strong>{p.label}</strong>
                <small>{p.detail}</small>
              </div>
              <em>
                {phaseLatencyMs[p.id] != null ? `${phaseLatencyMs[p.id]}ms` : isDone(p.id) ? "✓" : "—"}
              </em>
            </div>
          </span>
        ))}
      </div>

      <div className="gb-gate">{gate}</div>

      <div className="gb-event-log" aria-live="polite">
        {eventLog.length === 0 ? (
          <div className="gb-muted" style={{ fontStyle: "italic" }}>
            {preview
              ? "Previewing honest phase order — no invented latency_ms."
              : "No events yet — start a pipeline to stream agent:start / agent:done."}
          </div>
        ) : (
          eventLog.slice(-12).map((line, idx) => (
            <div key={`${line}-${idx}`} className="ev-live">
              {line}
            </div>
          ))
        )}
      </div>

      <div className="gb-ops-strip">
        <span>
          <strong>phases</strong> {doneCount}/{PIPELINE_PHASES.length}
        </span>
        <span>
          <strong>node latency</strong>{" "}
          {totalMs > 0 ? `${totalMs} ms` : traceSource === "live" ? "streaming" : "n/a"}
        </span>
        <span>
          <strong>status</strong> {status || (preview ? "preview" : "idle")}
        </span>
        <span>
          <strong>run</strong> {runId ? runId.slice(0, 8) + "…" : "—"}
        </span>
      </div>
    </>
  );
}
