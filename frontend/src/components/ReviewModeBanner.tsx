"use client";

import { useEffect, useState } from "react";
import { ACF_API_BASE } from "@/lib/workbench-config";

type ReviewMode = "pending" | "demo" | "strict";

/**
 * Sticky Demo vs Strict strip — S2 honesty (Top-1% plan).
 * Reads production_strict from API /health; defaults to Demo when unreachable.
 */
export function ReviewModeBanner() {
  const [mode, setMode] = useState<ReviewMode>("pending");
  const [mockLlm, setMockLlm] = useState<boolean | null>(null);

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      try {
        const res = await fetch(`${ACF_API_BASE}/health`, { cache: "no-store" });
        if (!res.ok) throw new Error(`health ${res.status}`);
        const body = (await res.json()) as {
          production_strict?: boolean;
          review_mode?: string;
          mock_llm?: boolean;
        };
        if (cancelled) return;
        const strict = Boolean(body.production_strict) || body.review_mode === "strict";
        setMode(strict ? "strict" : "demo");
        setMockLlm(typeof body.mock_llm === "boolean" ? body.mock_llm : null);
      } catch {
        if (!cancelled) setMode("demo");
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  if (mode === "pending") {
    return (
      <div className="border-t border-sky-200 bg-sky-50 px-6 py-2 text-xs leading-5 text-sky-900">
        <strong className="uppercase tracking-wide">Checking review mode…</strong>
      </div>
    );
  }

  if (mode === "strict") {
    return (
      <div className="border-t border-emerald-200 bg-emerald-50 px-6 py-2 text-xs leading-5 text-emerald-900">
        <strong className="uppercase tracking-wide">Strict review mode</strong>
        {" — "}
        <code className="rounded bg-emerald-100 px-1">PRODUCTION_STRICT</code> is on; publish fails closed
        without AegisAI gateway.
      </div>
    );
  }

  return (
    <div className="border-t border-amber-200 bg-amber-50 px-6 py-2 text-xs leading-5 text-amber-900">
      <strong className="uppercase tracking-wide">Demo review mode</strong>
      {" — "}
      live default{mockLlm ? " uses mock LLM and" : ""} allows fail-open gateway paths. Prefer{" "}
      <code className="rounded bg-amber-100 px-1">PRODUCTION_STRICT=1</code> for Principal panels.
    </div>
  );
}
