"use client";

import Link from "next/link";
import type { ReactNode } from "react";
import { ArchitectRail, type ArchitectRailProps } from "./ArchitectRail";
import { ContentPipelineGlassbox, type TraceSource } from "./ContentPipelineGlassbox";
import { ReviewModeBanner } from "./ReviewModeBanner";
import type { PhaseId, PhaseStatus } from "@/lib/store";

type Props = {
  eyebrow: string;
  title: string;
  subtitle: string;
  headerActions?: ReactNode;
  homeHref?: string;
  architect: ArchitectRailProps;
  productPanel: ReactNode;
  secondaryPanel?: ReactNode;
  metricsRefreshToken?: number;
  /** Public landing: animate phase preview once */
  preview?: boolean;
  traceSource?: TraceSource;
  phaseStatus?: Record<PhaseId, PhaseStatus>;
  phaseLatencyMs?: Partial<Record<PhaseId, number>>;
  status?: string | null;
  runId?: string | null;
  eventLog?: string[];
};

export function GlassboxWorkbench({
  eyebrow,
  title,
  subtitle,
  headerActions,
  homeHref = "/",
  architect,
  productPanel,
  secondaryPanel,
  metricsRefreshToken = 0,
  preview = false,
  traceSource = "idle",
  phaseStatus,
  phaseLatencyMs,
  status,
  runId,
  eventLog,
}: Props) {
  return (
    <div className="gb-page workbench-shell min-h-screen text-slate-900">
      <header className="sticky top-0 z-50 border-b border-slate-200/80 bg-white/80 backdrop-blur-md">
        <div className="mx-auto flex max-w-[1440px] items-center justify-between gap-4 px-6 py-4">
          <Link href={homeHref} className="flex min-w-0 items-center gap-3 no-underline text-inherit">
            <div
              className="grid h-9 w-9 shrink-0 place-items-center rounded-[10px] bg-gradient-to-br from-teal-600 to-teal-800 text-[0.7rem] font-bold text-white shadow-sm"
              aria-hidden
            >
              CF
            </div>
            <div className="min-w-0">
              <p className="text-[0.68rem] font-semibold uppercase tracking-[0.14em] text-slate-500">
                {eyebrow}
              </p>
              <h1 className="truncate text-lg font-semibold tracking-tight text-slate-900 md:text-xl">
                {title}
              </h1>
            </div>
          </Link>
          {headerActions ? <div className="flex shrink-0 items-center gap-3">{headerActions}</div> : null}
        </div>
        <ReviewModeBanner />
      </header>

      <main className="gb-shell">
        <div className="gb-hero">
          <p className="eyebrow">{eyebrow}</p>
          <h1>{title}</h1>
          <p className="lede">{subtitle}</p>
        </div>

        <div className="gb-workbench">
          <aside className="gb-rail" aria-label="Architecture and metrics">
            <ArchitectRail {...architect} refreshToken={metricsRefreshToken} />
          </aside>

          <section className="gb-center" aria-label="Content pipeline glass-box">
            <ContentPipelineGlassbox
              preview={preview}
              traceSource={traceSource}
              phaseStatus={phaseStatus}
              phaseLatencyMs={phaseLatencyMs}
              status={status}
              runId={runId}
              eventLog={eventLog}
            />
          </section>

          <aside className="gb-product" aria-label="Content product">
            {productPanel}
          </aside>
        </div>

        {secondaryPanel ? <div className="gb-secondary">{secondaryPanel}</div> : null}
      </main>
    </div>
  );
}
