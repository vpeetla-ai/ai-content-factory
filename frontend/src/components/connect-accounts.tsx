"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

const CONNECTABLE = ["linkedin", "x"] as const;

export function ConnectAccounts() {
  const [connected, setConnected] = useState<string[]>([]);
  const [loading, setLoading] = useState<string | null>(null);

  useEffect(() => {
    api.oauth
      .status()
      .then((data) => setConnected(data.connected))
      .catch(() => setConnected([]));
  }, []);

  const handleConnect = async (platform: "linkedin" | "x") => {
    setLoading(platform);
    try {
      const { authorize_url } = await api.oauth.authorize(platform);
      window.location.href = authorize_url;
    } catch {
      setLoading(null);
    }
  };

  return (
    <section className="bg-panel border border-white/10 rounded-xl p-6">
      <h2 className="text-sm font-semibold uppercase tracking-wider text-muted mb-4">
        Connected Accounts
      </h2>
      <div className="flex flex-wrap gap-2">
        {CONNECTABLE.map((platform) => {
          const isConnected = connected.includes(platform);
          return (
            <button
              key={platform}
              onClick={() => !isConnected && handleConnect(platform)}
              disabled={isConnected || loading === platform}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold border transition ${
                isConnected
                  ? "bg-green-400/10 border-green-400/30 text-green-400 cursor-default"
                  : "bg-surface border-white/10 text-muted hover:border-accent hover:text-accent"
              }`}
            >
              {isConnected ? `✓ ${platform} connected` : loading === platform ? "Connecting…" : `Connect ${platform}`}
            </button>
          );
        })}
      </div>
      <p className="mt-3 text-xs text-muted">
        Only LinkedIn and X support real auto-publish today. Medium, Substack and Instagram drafts are
        provided as copy-ready text after each run.
      </p>
    </section>
  );
}
