import { create } from "zustand";

interface PipelineStore {
  activeRunId: string | null;
  status: string | null;
  agentLogs: string[];
  setActiveRun: (runId: string) => void;
  setStatus: (status: string) => void;
  addLog: (msg: string) => void;
  clear: () => void;
}

export const usePipelineStore = create<PipelineStore>((set) => ({
  activeRunId: null,
  status: null,
  agentLogs: [],
  setActiveRun: (runId) => set({ activeRunId: runId }),
  setStatus: (status) => set({ status }),
  addLog: (msg) => set((s) => ({ agentLogs: [...s.agentLogs, msg] })),
  clear: () => set({ activeRunId: null, status: null, agentLogs: [] }),
}));
