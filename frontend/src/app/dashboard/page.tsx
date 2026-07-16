"use client";

import { useState } from "react";
import { useAuth, UserButton } from "@clerk/nextjs";
import { useMutation, useQuery } from "@tanstack/react-query";
import { api, getToken, setToken } from "@/lib/api";
import { getInviteCode, clearInviteCode } from "@/lib/invite";
import { usePipelineStore, PublishResult } from "@/lib/store";
import { usePipelineSocket } from "@/hooks/usePipelineSocket";
import { usePipelineSSE } from "@/hooks/usePipelineSSE";
import { PipelineForm } from "@/components/pipeline-form";
import { AgentLog } from "@/components/agent-log";
import { HITLReview } from "@/components/hitl-review";
import { RunList } from "@/components/run-list";
import { PublishResults } from "@/components/publish-results";
import { ConnectAccounts } from "@/components/connect-accounts";
import { isClerkEnabled } from "@/components/providers";
import Link from "next/link";
import { GlassboxWorkbench } from "@/components/GlassboxWorkbench";
import {
  ACF_ARCHITECTURE_PROPS,
  ACF_LAYERS,
  ACF_TRADEOFFS,
  ACF_ADR_LINKS,
  ACF_DOCS_LINKS,
} from "@/lib/workbench-config";

const PLATFORMS = ["linkedin", "substack", "medium", "x", "instagram"];

function ClerkDashboard() {
  const { getToken: getClerkToken, isLoaded, isSignedIn } = useAuth();
  const [topic, setTopic] = useState("");
  const [token, setAuthToken] = useState<string | null>(null);
  const { activeRunId, status, agentLogs, publishResults, setActiveRun, setStatus, addLog } = usePipelineStore();
  const effectiveToken = token || getToken();
  usePipelineSocket(activeRunId, effectiveToken);
  usePipelineSSE(activeRunId, effectiveToken);

  const authMutation = useMutation({
    mutationFn: async () => {
      const clerkToken = await getClerkToken({ skipCache: true });
      if (!clerkToken) throw new Error("Not signed in");
      return api.auth.token(clerkToken, getInviteCode());
    },
    onSuccess: (data) => {
      setToken(data.access_token);
      setAuthToken(data.access_token);
      clearInviteCode();
      addLog("Authenticated via Clerk");
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

  if (!isLoaded) {
    return <LoadingScreen />;
  }

  if (!isSignedIn) {
    return (
      <main className="min-h-screen p-6 flex flex-col items-center justify-center gap-4">
        <h1 className="text-xl font-bold">AI Content Factory</h1>
        <p className="text-muted">Sign in to start the content pipeline.</p>
        <div className="flex flex-wrap items-center justify-center gap-3">
          <a href="/sign-in?redirect_url=/dashboard" className="px-4 py-2 rounded-lg bg-accent text-white">
            Sign in
          </a>
          <Link href="/" className="text-sm font-medium text-slate-600 hover:text-slate-900">
            ← Back to overview
          </Link>
        </div>
      </main>
    );
  }

  return (
    <DashboardShell
      topic={topic}
      onTopicChange={setTopic}
      onStart={handleStart}
      loading={runMutation.isPending || authMutation.isPending}
      agentLogs={agentLogs}
      publishResults={publishResults}
      status={status}
      activeRunId={activeRunId}
      runs={runs || []}
      onSelectRun={setActiveRun}
      onHitlComplete={() => {
        usePipelineStore.getState().setPhaseDone("hitl");
        usePipelineStore.getState().setPhaseActive("publish");
        setStatus("running");
      }}
      headerRight={
        <div className="flex items-center gap-3">
          <Link href="/" className="text-sm font-medium text-slate-600 hover:text-slate-900">
            ← Overview
          </Link>
          <UserButton afterSignOutUrl="/" />
        </div>
      }
    />
  );
}

function DevDashboard() {
  const [topic, setTopic] = useState("");
  const [token, setAuthToken] = useState<string | null>(null);
  const { activeRunId, status, agentLogs, publishResults, setActiveRun, setStatus, addLog } = usePipelineStore();
  const effectiveToken = token || getToken();
  usePipelineSocket(activeRunId, effectiveToken);
  usePipelineSSE(activeRunId, effectiveToken);

  const authMutation = useMutation({
    mutationFn: () => api.auth.token("dev@acf.local"),
    onSuccess: (data) => {
      setToken(data.access_token);
      setAuthToken(data.access_token);
      addLog("Authenticated (local dev mode)");
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
    <DashboardShell
      topic={topic}
      onTopicChange={setTopic}
      onStart={handleStart}
      loading={runMutation.isPending || authMutation.isPending}
      agentLogs={agentLogs}
      publishResults={publishResults}
      status={status}
      activeRunId={activeRunId}
      runs={runs || []}
      onSelectRun={setActiveRun}
      onHitlComplete={() => {
        usePipelineStore.getState().setPhaseDone("hitl");
        usePipelineStore.getState().setPhaseActive("publish");
        setStatus("running");
      }}
      headerRight={
        <div className="flex items-center gap-3">
          <Link href="/" className="text-sm font-medium text-slate-600 hover:text-slate-900">
            ← Overview
          </Link>
          <span className="text-xs text-muted px-2 py-1 rounded bg-surface border border-border">
            {typeof window !== "undefined" && window.location.hostname.includes("vercel.app")
              ? "Demo — add Clerk keys in Vercel for sign-in"
              : "Local dev"}
          </span>
        </div>
      }
    />
  );
}

function LoadingScreen() {
  return (
    <main className="min-h-screen p-6 flex items-center justify-center">
      <p className="text-muted">Loading...</p>
    </main>
  );
}

function DashboardShell({
  topic,
  onTopicChange,
  onStart,
  loading,
  agentLogs,
  publishResults,
  status,
  activeRunId,
  runs,
  onSelectRun,
  onHitlComplete,
  headerRight,
}: {
  topic: string;
  onTopicChange: (v: string) => void;
  onStart: () => void;
  loading: boolean;
  agentLogs: string[];
  publishResults: PublishResult[];
  status: string | null;
  activeRunId: string | null;
  runs: Array<{ run_id: string; status: string; topic: string }>;
  onSelectRun: (id: string) => void;
  onHitlComplete: () => void;
  headerRight: React.ReactNode;
}) {
  const { phaseStatus, phaseLatencyMs } = usePipelineStore();

  return (
    <GlassboxWorkbench
      eyebrow="Governed multi-agent content pipeline"
      title="AI Content Factory — glass-box"
      subtitle="Run the pipeline, review HITL gates, and publish through AegisAI. Live agent:start / agent:done phases stream in the center — including real latency_ms when the API sends them."
      headerActions={headerRight}
      homeHref="/"
      traceSource={activeRunId ? "live" : "idle"}
      phaseStatus={phaseStatus}
      phaseLatencyMs={phaseLatencyMs}
      status={status}
      runId={activeRunId}
      eventLog={agentLogs}
      architect={{
        layers: [...ACF_LAYERS],
        tradeoffs: [...ACF_TRADEOFFS],
        metricsUrl: ACF_ARCHITECTURE_PROPS.metricsUrl,
        metricLabels: ACF_ARCHITECTURE_PROPS.metricLabels,
        adrLinks: [...ACF_ADR_LINKS],
        docsLinks: [...ACF_DOCS_LINKS],
      }}
      productPanel={
        <>
          <p className="gb-guided">
            <strong>1.</strong> Enter a topic → <strong>2.</strong> Start Pipeline →{" "}
            <strong>3.</strong> approve each platform at HITL, then publish.
          </p>
          <PipelineForm topic={topic} onTopicChange={onTopicChange} onStart={onStart} loading={loading} />
          <AgentLog logs={agentLogs} status={status} runId={activeRunId} />
          {status === "hitl_wait" && activeRunId && (
            <HITLReview runId={activeRunId} onComplete={onHitlComplete} />
          )}
          <PublishResults results={publishResults} />
          <div className="gb-side-stack">
            <ConnectAccounts />
            <RunList runs={runs} onSelect={onSelectRun} />
          </div>
        </>
      }
    />
  );
}

export default function DashboardPage() {
  return isClerkEnabled ? <ClerkDashboard /> : <DevDashboard />;
}
