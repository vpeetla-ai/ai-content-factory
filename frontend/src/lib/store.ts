import { create } from "zustand";

export interface PublishResult {
  platform: string;
  postId: string;
  url: string;
  notSupported: boolean;
  draftContent: string;
}

interface PipelineStore {
  activeRunId: string | null;
  status: string | null;
  agentLogs: string[];
  publishResults: PublishResult[];
  setActiveRun: (runId: string) => void;
  setStatus: (status: string) => void;
  addLog: (msg: string) => void;
  addPublishResult: (result: PublishResult) => void;
  clear: () => void;
}

export const usePipelineStore = create<PipelineStore>((set) => ({
  activeRunId: null,
  status: null,
  agentLogs: [],
  publishResults: [],
  setActiveRun: (runId) => set({ activeRunId: runId }),
  setStatus: (status) => set({ status }),
  addLog: (msg) => set((s) => ({ agentLogs: [...s.agentLogs, msg] })),
  addPublishResult: (result) =>
    set((s) => ({ publishResults: [...s.publishResults, result] })),
  clear: () => set({ activeRunId: null, status: null, agentLogs: [], publishResults: [] }),
}));
