import { create } from "zustand";

export interface PublishResult {
  platform: string;
  postId: string;
  url: string;
  notSupported: boolean;
  draftContent: string;
}

export type PhaseId = "research" | "content" | "enrich" | "hitl" | "publish";
export type PhaseStatus = "idle" | "active" | "done";

export const PIPELINE_PHASES: PhaseId[] = ["research", "content", "enrich", "hitl", "publish"];

interface PipelineStore {
  activeRunId: string | null;
  status: string | null;
  agentLogs: string[];
  publishResults: PublishResult[];
  phaseStatus: Record<PhaseId, PhaseStatus>;
  phaseLatencyMs: Partial<Record<PhaseId, number>>;
  setActiveRun: (runId: string) => void;
  setStatus: (status: string) => void;
  addLog: (msg: string) => void;
  addPublishResult: (result: PublishResult) => void;
  setPhaseActive: (phase: PhaseId) => void;
  setPhaseDone: (phase: PhaseId, latencyMs?: number) => void;
  resetPhases: () => void;
  clear: () => void;
}

const idlePhases = (): Record<PhaseId, PhaseStatus> => ({
  research: "idle",
  content: "idle",
  enrich: "idle",
  hitl: "idle",
  publish: "idle",
});

function asPhase(name: string | undefined): PhaseId | null {
  if (!name) return null;
  const n = name.toLowerCase();
  if ((PIPELINE_PHASES as string[]).includes(n)) return n as PhaseId;
  return null;
}

export { asPhase };

export const usePipelineStore = create<PipelineStore>((set) => ({
  activeRunId: null,
  status: null,
  agentLogs: [],
  publishResults: [],
  phaseStatus: idlePhases(),
  phaseLatencyMs: {},
  setActiveRun: (runId) =>
    set({
      activeRunId: runId,
      phaseStatus: idlePhases(),
      phaseLatencyMs: {},
      agentLogs: [],
      publishResults: [],
    }),
  setStatus: (status) => set({ status }),
  addLog: (msg) => set((s) => ({ agentLogs: [...s.agentLogs, msg] })),
  addPublishResult: (result) =>
    set((s) => ({ publishResults: [...s.publishResults, result] })),
  setPhaseActive: (phase) =>
    set((s) => ({
      phaseStatus: { ...s.phaseStatus, [phase]: "active" },
    })),
  setPhaseDone: (phase, latencyMs) =>
    set((s) => ({
      phaseStatus: { ...s.phaseStatus, [phase]: "done" },
      phaseLatencyMs:
        latencyMs != null
          ? { ...s.phaseLatencyMs, [phase]: latencyMs }
          : s.phaseLatencyMs,
    })),
  resetPhases: () => set({ phaseStatus: idlePhases(), phaseLatencyMs: {} }),
  clear: () =>
    set({
      activeRunId: null,
      status: null,
      agentLogs: [],
      publishResults: [],
      phaseStatus: idlePhases(),
      phaseLatencyMs: {},
    }),
}));
