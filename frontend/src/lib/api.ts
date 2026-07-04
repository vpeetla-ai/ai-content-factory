const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

let token: string | null = null;

export function setToken(t: string) {
  token = t;
  if (typeof window !== "undefined") localStorage.setItem("acf_token", t);
}

export function getToken(): string | null {
  if (token) return token;
  if (typeof window !== "undefined") token = localStorage.getItem("acf_token");
  return token;
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };
  const t = getToken();
  if (t) headers.Authorization = `Bearer ${t}`;

  const res = await fetch(`${API_URL}${path}`, { ...options, headers });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "Request failed");
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

export const api = {
  auth: {
    token: (clerkToken: string, inviteCode?: string | null) =>
      request<{ access_token: string }>("/auth/token", {
        method: "POST",
        body: JSON.stringify({ clerk_token: clerkToken, invite_code: inviteCode || undefined }),
      }),
  },
  pipelines: {
    run: (topic: string, platforms: string[]) =>
      request<{ run_id: string; status: string; topic: string }>("/pipelines/run", {
        method: "POST",
        body: JSON.stringify({ topic, platforms }),
      }),
    get: (runId: string) => request(`/pipelines/${runId}`),
    list: () => request<Array<{ run_id: string; status: string; topic: string }>>("/pipelines"),
  },
  hitl: {
    review: (runId: string) => request(`/hitl/${runId}/review`),
    approve: (runId: string, decisions: unknown[]) =>
      request(`/hitl/${runId}/approve`, {
        method: "POST",
        body: JSON.stringify({ decisions }),
      }),
    reject: (runId: string) =>
      request(`/hitl/${runId}/reject`, { method: "POST" }),
  },
  content: {
    drafts: (runId: string) => request(`/content/${runId}/drafts`),
  },
  oauth: {
    authorize: (platform: "linkedin" | "x") =>
      request<{ authorize_url: string }>(`/oauth/${platform}/authorize`),
    status: () => request<{ connected: string[] }>("/oauth/status"),
  },
};
