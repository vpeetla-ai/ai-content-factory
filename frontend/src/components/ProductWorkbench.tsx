"use client";

import Link from "next/link";
import { useState, type ReactNode } from "react";

export type WorkbenchTab = "product" | "architecture";

type Props = {
  eyebrow: string;
  productName: string;
  subtitle: string;
  headerActions?: ReactNode;
  productPanel: ReactNode;
  architecturePanel: ReactNode;
  defaultTab?: WorkbenchTab;
  homeHref?: string;
};

/** Enterprise workbench: product/demo first, architecture & metrics on a separate tab. */
export function ProductWorkbench({
  eyebrow,
  productName,
  subtitle,
  headerActions,
  productPanel,
  architecturePanel,
  defaultTab = "product",
  homeHref = "/",
}: Props) {
  const [tab, setTab] = useState<WorkbenchTab>(defaultTab);

  return (
    <div className="workbench-shell min-h-screen text-slate-900">
      <header className="border-b border-slate-200/80 bg-white/80 backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-6 py-4">
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
                {productName}
              </h1>
            </div>
          </Link>
          {headerActions ? <div className="flex shrink-0 items-center gap-3">{headerActions}</div> : null}
        </div>
        <div className="mx-auto max-w-6xl px-6 pb-0">
          <p className="max-w-3xl pb-4 text-sm leading-relaxed text-slate-600">{subtitle}</p>
          <nav
            className="flex gap-1 border-b border-slate-200"
            role="tablist"
            aria-label="Product workbench"
          >
            <WorkbenchTabButton
              active={tab === "product"}
              onClick={() => setTab("product")}
              label="Live product"
              description="Run the demo"
            />
            <WorkbenchTabButton
              active={tab === "architecture"}
              onClick={() => setTab("architecture")}
              label="Architecture & metrics"
              description="Stack, tradeoffs, SLOs"
            />
          </nav>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 py-8">
        {tab === "product" ? (
          <div role="tabpanel" aria-label="Live product">
            {productPanel}
          </div>
        ) : (
          <div role="tabpanel" aria-label="Architecture and metrics">
            {architecturePanel}
          </div>
        )}
      </main>
    </div>
  );
}

function WorkbenchTabButton({
  active,
  onClick,
  label,
  description,
}: {
  active: boolean;
  onClick: () => void;
  label: string;
  description: string;
}) {
  return (
    <button
      type="button"
      role="tab"
      aria-selected={active}
      onClick={onClick}
      className={[
        "relative -mb-px rounded-t-lg px-4 py-3 text-left transition-colors",
        active
          ? "border border-b-white border-slate-200 bg-white text-slate-900"
          : "border border-transparent text-slate-500 hover:bg-white/60 hover:text-slate-800",
      ].join(" ")}
    >
      <span className="block text-sm font-semibold">{label}</span>
      <span className="block text-[0.65rem] text-slate-500">{description}</span>
      {active ? (
        <span className="absolute inset-x-0 bottom-0 h-0.5 bg-teal-600" aria-hidden />
      ) : null}
    </button>
  );
}
