"use client";

import Link from "next/link";
import { GlassboxWorkbench } from "@/components/GlassboxWorkbench";
import {
  ACF_ARCHITECTURE_PROPS,
  ACF_LAYERS,
  ACF_TRADEOFFS,
  ACF_ADR_LINKS,
  ACF_DOCS_LINKS,
} from "@/lib/workbench-config";

export default function LandingPage() {
  return (
    <GlassboxWorkbench
      eyebrow="Governed multi-agent content pipeline"
      title="AI Content Factory — glass-box"
      subtitle="One topic → five platform drafts → human approval → governed publish. Architecture and live SLOs on the left · honest phase map in the center · sign in on the right to run."
      headerActions={
        <a
          href="https://github.com/vpeetla-ai/ai-content-factory"
          className="text-sm font-medium text-slate-600 hover:text-slate-900"
          target="_blank"
          rel="noopener noreferrer"
        >
          GitHub
        </a>
      }
      preview
      traceSource="preview"
      architect={{
        layers: [...ACF_LAYERS],
        tradeoffs: [...ACF_TRADEOFFS],
        metricsUrl: ACF_ARCHITECTURE_PROPS.metricsUrl,
        metricLabels: ACF_ARCHITECTURE_PROPS.metricLabels,
        adrLinks: [...ACF_ADR_LINKS],
        docsLinks: [...ACF_DOCS_LINKS],
      }}
      productPanel={
        <>
          <p className="gb-guided">
            <strong>1.</strong> Sign in (invite-only) → <strong>2.</strong> enter a topic and start the
            pipeline → <strong>3.</strong> approve each platform at the HITL gate.
          </p>

          <div className="gb-product-card">
            <h2>Run the content pipeline</h2>
            <p>
              Research with RAG, generate drafts for LinkedIn, X, Substack, Medium, and blog — then
              approve each platform before AegisAI allows publish.
            </p>
            <div className="gb-run-row">
              <Link href="/sign-in?redirect_url=/dashboard" className="gb-primary-cta">
                Sign in to run pipeline
              </Link>
            </div>
            <p className="gb-hint">
              After sign-in you land on the dashboard glass-box with live SSE phase replay. Click the
              CF brand anytime to return here.
            </p>
          </div>

          <div className="gb-feature-list">
            {[
              { title: "Research + RAG", body: "Hybrid retrieval grounds drafts before generation." },
              { title: "HITL before publish", body: "interrupt_before — humans approve every platform." },
              { title: "Trace-linked LLMOps", body: "Langfuse spans; live agent:done includes latency_ms." },
            ].map((item) => (
              <div key={item.title} className="gb-feature">
                <strong>{item.title}</strong>
                <span>{item.body}</span>
              </div>
            ))}
          </div>

          <a
            href={ACF_ADR_LINKS[0].href}
            className="gb-adr-inline"
            target="_blank"
            rel="noopener noreferrer"
          >
            Read ADR-008 →
          </a>
        </>
      }
    />
  );
}
