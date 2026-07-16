"use client";

import { useEffect, useRef } from "react";
import { io, Socket } from "socket.io-client";
import { asPhase, usePipelineStore } from "@/lib/store";

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "http://localhost:8000";

export function usePipelineSocket(runId: string | null, authToken: string | null) {
  const socketRef = useRef<Socket | null>(null);
  const { addLog, setStatus, addPublishResult, setPhaseActive, setPhaseDone } = usePipelineStore();

  useEffect(() => {
    if (!runId) return;

    const socket = io(WS_URL, {
      transports: ["websocket", "polling"],
      auth: authToken ? { token: authToken } : undefined,
      query: authToken ? { token: authToken } : undefined,
    });
    socketRef.current = socket;

    socket.on("connect", () => {
      socket.emit("join_run", { run_id: runId });
      addLog("Connected to pipeline stream");
    });

    socket.on("agent:start", (data) => {
      const phase = asPhase(data.agent_name);
      if (phase) setPhaseActive(phase);
      addLog(`▶ ${data.agent_name} started`);
    });
    socket.on("agent:chunk", (data) => addLog(`${data.agent_name}: ${data.token}`));
    socket.on("agent:done", (data) => {
      const phase = asPhase(data.agent_name);
      if (phase) {
        setPhaseDone(phase, typeof data.latency_ms === "number" ? data.latency_ms : undefined);
      }
      const ms = typeof data.latency_ms === "number" ? ` (${data.latency_ms}ms)` : "";
      addLog(`✓ ${data.agent_name} → ${data.output_key}${ms}`);
    });
    socket.on("hitl:ready", () => {
      setStatus("hitl_wait");
      setPhaseActive("hitl");
      addLog("✋ HITL review required");
    });
    socket.on("publish:result", (data) => {
      setPhaseDone("publish");
      addLog(
        data.not_supported
          ? `📋 ${data.platform}: not auto-published — draft ready to copy`
          : `🚀 Published to ${data.platform}: ${data.url}`
      );
      addPublishResult({
        platform: data.platform,
        postId: data.post_id,
        url: data.url,
        notSupported: !!data.not_supported,
        draftContent: data.draft_content || "",
      });
    });
    socket.on("pipeline:error", (data) => {
      setStatus("error");
      addLog(`✗ Error: ${data.error_msg}`);
    });

    return () => {
      socket.disconnect();
    };
  }, [runId, authToken, addLog, setStatus, addPublishResult, setPhaseActive, setPhaseDone]);

  return socketRef;
}
