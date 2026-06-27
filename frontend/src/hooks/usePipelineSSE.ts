"use client";

import { useEffect } from "react";
import { usePipelineStore } from "@/lib/store";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export function usePipelineSSE(runId: string | null, token: string | null) {
  const { addLog, setStatus } = usePipelineStore();

  useEffect(() => {
    if (!runId || !token) return;

    const url = `${API_URL}/pipelines/${runId}/stream`;
    const source = new EventSource(url, { withCredentials: false });

    // EventSource cannot set Authorization header — use fetch-based SSE fallback via polling
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
            if (event === "agent:start") addLog(`▶ ${parsed.agent_name} started`);
            if (event === "agent:chunk") addLog(`${parsed.agent_name}: ${parsed.token}`);
            if (event === "agent:done") addLog(`✓ ${parsed.agent_name} → ${parsed.output_key}`);
            if (event === "hitl:ready") {
              setStatus("hitl_wait");
              addLog("✋ HITL review required");
            }
            if (event === "publish:result") {
              addLog(`🚀 Published to ${parsed.platform}: ${parsed.url}`);
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
  }, [runId, token, addLog, setStatus]);
}
