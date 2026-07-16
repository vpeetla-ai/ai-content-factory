"use client";

import { useEffect } from "react";
import { asPhase, usePipelineStore } from "@/lib/store";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export function usePipelineSSE(runId: string | null, token: string | null) {
  const { addLog, setStatus, addPublishResult, setPhaseActive, setPhaseDone } = usePipelineStore();

  useEffect(() => {
    if (!runId || !token) return;

    const url = `${API_URL}/pipelines/${runId}/stream`;
    const source = new EventSource(url, { withCredentials: false });
    source.close();

    let cancelled = false;

    async function streamWithAuth() {
      const res = await fetch(url, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok || !res.body) return;

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (!cancelled) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const parts = buffer.split("\n\n");
        buffer = parts.pop() || "";

        for (const part of parts) {
          let event = "message";
          let data = "";
          for (const line of part.split("\n")) {
            if (line.startsWith("event:")) event = line.slice(6).trim();
            if (line.startsWith("data:")) data = line.slice(5).trim();
          }
          if (!data) continue;
          try {
            const parsed = JSON.parse(data);
            if (event === "agent:start") {
              const phase = asPhase(parsed.agent_name);
              if (phase) setPhaseActive(phase);
              addLog(`▶ ${parsed.agent_name} started`);
            }
            if (event === "agent:chunk") addLog(`${parsed.agent_name}: ${parsed.token}`);
            if (event === "agent:done") {
              const phase = asPhase(parsed.agent_name);
              if (phase) {
                setPhaseDone(
                  phase,
                  typeof parsed.latency_ms === "number" ? parsed.latency_ms : undefined
                );
              }
              const ms =
                typeof parsed.latency_ms === "number" ? ` (${parsed.latency_ms}ms)` : "";
              addLog(`✓ ${parsed.agent_name} → ${parsed.output_key}${ms}`);
            }
            if (event === "hitl:ready") {
              setStatus("hitl_wait");
              setPhaseActive("hitl");
              addLog("✋ HITL review required");
            }
            if (event === "publish:result") {
              setPhaseDone("publish");
              addLog(
                parsed.not_supported
                  ? `📋 ${parsed.platform}: not auto-published — draft ready to copy`
                  : `🚀 Published to ${parsed.platform}: ${parsed.url}`
              );
              addPublishResult({
                platform: parsed.platform,
                postId: parsed.post_id,
                url: parsed.url,
                notSupported: !!parsed.not_supported,
                draftContent: parsed.draft_content || "",
              });
            }
            if (event === "pipeline:status") setStatus(parsed.status);
            if (event === "pipeline:error") {
              setStatus("error");
              addLog(`✗ ${parsed.error_msg}`);
            }
          } catch {
            /* ignore parse errors */
          }
        }
      }
    }

    streamWithAuth();
    return () => {
      cancelled = true;
    };
  }, [runId, token, addLog, setStatus, addPublishResult, setPhaseActive, setPhaseDone]);
}
