"use client";

import { useState } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { api, getToken, setToken } from "@/lib/api";
import { usePipelineStore } from "@/lib/store";
import { usePipelineSocket } from "@/hooks/usePipelineSocket";
import { usePipelineSSE } from "@/hooks/usePipelineSSE";
import { PipelineForm } from "@/components/pipeline-form";
import { AgentLog } from "@/components/agent-log";
import { HITLReview } from "@/components/hitl-review";
import { RunList } from "@/components/run-list";

const PLATFORMS = ["linkedin", "substack", "medium", "x", "instagram"];

export default function DashboardPage() {
  const [topic, setTopic] = useState("");
  const [token, setAuthToken] = useState<string | null>(null);
  const { activeRunId, status, agentLogs, setActiveRun, setStatus, addLog } = usePipelineStore();
  usePipelineSocket(activeRunId);
  usePipelineSSE(activeRunId, token || getToken());

  const authMutation = useMutation({
    mutationFn: () => api.auth.token("dev@acf.local"),
    onSuccess: (data) => {
      setToken(data.access_token);
      setAuthToken(data.access_token);
      addLog("Authenticated");
    },
  });

  const runMutation = useMutation({
    mutationFn: () => api.pipelines.run(topic, PLATFORMS),
    onSuccess: (data) => {
      setActiveRun(data.run_id);
      setStatus(data.status);
      addLog(`Pipeline started: ${data.run_id}`);
    },
  });

  const { data: runs } = useQuery({
    queryKey: ["pipelines"],
    queryFn: () => api.pipelines.list(),
    enabled: !!getToken(),
  });

  const handleStart = async () => {
    if (!getToken()) await authMutation.mutateAsync();
    await runMutation.mutateAsync();
  };

  return (
    <main className="min-h-screen p-6 max-w-6xl mx-auto">
      <header className="mb-8 flex items-center gap-3">
        <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-accent to-teal flex items-center justify-center font-bold text-white">
          ⚡
        </div>
        <div>
          <h1 className="text-xl font-bold">AI Content Factory</h1>
          <p className="text-sm text-muted">Multi-Agent · HITL · Free-First Stack</p>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <PipelineForm
            topic={topic}
            onTopicChange={setTopic}
            onStart={handleStart}
            loading={runMutation.isPending}
          />
          <AgentLog logs={agentLogs} status={status} runId={activeRunId} />
          {status === "hitl_wait" && activeRunId && (
            <HITLReview runId={activeRunId} onComplete={() => setStatus("running")} />
          )}
        </div>
        <div>
          <RunList runs={runs || []} onSelect={(id) => setActiveRun(id)} />
        </div>
      </div>
    </main>
  );
}
