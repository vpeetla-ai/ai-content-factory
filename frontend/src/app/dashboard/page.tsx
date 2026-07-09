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
import { ArchitectOverview } from "@/components/ArchitectOverview";
import { ProductWorkbench } from "@/components/ProductWorkbench";
import { ACF_ARCHITECTURE_PROPS } from "@/lib/workbench-config";

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
      onHitlComplete={() => setStatus("running")}
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
      onHitlComplete={() => setStatus("running")}
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
  return (
    <ProductWorkbench
      eyebrow="Governed multi-agent content pipeline"
      productName="AI Content Factory"
      subtitle="Run the pipeline, review HITL gates, and publish through AegisAI — architecture and live metrics on the second tab."
      headerActions={headerRight}
      productPanel={
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <PipelineForm topic={topic} onTopicChange={onTopicChange} onStart={onStart} loading={loading} />
            <AgentLog logs={agentLogs} status={status} runId={activeRunId} />
            {status === "hitl_wait" && activeRunId && (
              <HITLReview runId={activeRunId} onComplete={onHitlComplete} />
            )}
            <PublishResults results={publishResults} />
          </div>
          <div className="space-y-6">
            <ConnectAccounts />
            <RunList runs={runs} onSelect={onSelectRun} />
          </div>
        </div>
      }
      architecturePanel={<ArchitectOverview {...ACF_ARCHITECTURE_PROPS} />}
    />
  );
}

export default function DashboardPage() {
  return isClerkEnabled ? <ClerkDashboard /> : <DevDashboard />;
}
