"use client";

import Link from "next/link";
import { ArchitectOverview } from "@/components/ArchitectOverview";
import { ProductWorkbench } from "@/components/ProductWorkbench";
import { ACF_ARCHITECTURE_PROPS } from "@/lib/workbench-config";

export default function LandingPage() {
  return (
    <ProductWorkbench
      eyebrow="Governed multi-agent content pipeline"
      productName="AI Content Factory"
      subtitle="One topic → five platform drafts → human approval → governed publish. Sign in to run the full pipeline."
      headerActions={
        <>
          <a
            href="https://github.com/vpeetla-ai/ai-content-factory"
            className="text-sm font-medium text-slate-600 hover:text-slate-900"
            target="_blank"
            rel="noopener noreferrer"
          >
            GitHub
          </a>
          <Link href="/sign-in" className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700">
            Sign in
          </Link>
        </>
      }
      productPanel={
        <div className="rounded-xl border border-slate-200 bg-white p-8 shadow-sm">
          <h2 className="text-xl font-semibold text-slate-900">Run the content pipeline</h2>
          <p className="mt-2 max-w-2xl text-sm leading-relaxed text-slate-600">
            Research with RAG, generate drafts for LinkedIn, X, Substack, Medium, and blog — then approve each
            platform before AegisAI allows publish.
          </p>
          <div className="mt-8 grid gap-4 sm:grid-cols-3">
            {[
              { title: "Research + RAG", body: "Hybrid retrieval grounds drafts before generation." },
              { title: "HITL before publish", body: "interrupt_before — humans approve every platform." },
              { title: "Trace-linked LLMOps", body: "Langfuse spans at system, trace, and node levels." },
            ].map((card) => (
              <div key={card.title} className="rounded-lg border border-slate-100 bg-slate-50 p-4">
                <h3 className="font-semibold text-slate-900">{card.title}</h3>
                <p className="mt-1 text-sm text-slate-600">{card.body}</p>
              </div>
            ))}
          </div>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link href="/sign-in" className="rounded-lg bg-blue-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-blue-700">
              Try the demo
            </Link>
            <Link href="/dashboard" className="rounded-lg border border-slate-200 px-5 py-2.5 text-sm font-semibold text-slate-700 hover:bg-slate-50">
              Open dashboard
            </Link>
            <a
              href={ACF_ARCHITECTURE_PROPS.adrLinks![0].href}
              className="rounded-lg border border-slate-200 px-5 py-2.5 text-sm font-semibold text-slate-700 hover:bg-slate-50"
              target="_blank"
              rel="noopener noreferrer"
            >
              ADR-008
            </a>
          </div>
        </div>
      }
      architecturePanel={<ArchitectOverview {...ACF_ARCHITECTURE_PROPS} />}
    />
  );
}
