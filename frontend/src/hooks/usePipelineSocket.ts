"use client";

import { useEffect, useRef } from "react";
import { io, Socket } from "socket.io-client";
import { usePipelineStore } from "@/lib/store";

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "http://localhost:8000";

export function usePipelineSocket(runId: string | null) {
  const socketRef = useRef<Socket | null>(null);
  const { addLog, setStatus } = usePipelineStore();

  useEffect(() => {
    if (!runId) return;

    const socket = io(WS_URL, { transports: ["websocket", "polling"] });
    socketRef.current = socket;

    socket.on("connect", () => {
      socket.emit("join_run", { run_id: runId });
      addLog("Connected to pipeline stream");
    });

    socket.on("agent:start", (data) => addLog(`▶ ${data.agent_name} started`));
    socket.on("agent:chunk", (data) => addLog(`${data.agent_name}: ${data.token}`));
    socket.on("agent:done", (data) => addLog(`✓ ${data.agent_name} → ${data.output_key}`));
    socket.on("hitl:ready", () => {
      setStatus("hitl_wait");
      addLog("✋ HITL review required");
    });
    socket.on("publish:result", (data) =>
      addLog(`🚀 Published to ${data.platform}: ${data.url}`)
    );
    socket.on("pipeline:error", (data) => {
      setStatus("error");
      addLog(`✗ Error: ${data.error_msg}`);
    });

    return () => {
      socket.disconnect();
    };
  }, [runId, addLog, setStatus]);

  return socketRef;
}
