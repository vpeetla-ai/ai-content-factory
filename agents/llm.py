"""LiteLLM client — routes to proxy with agent-specific model names + mock dev mode."""

import json
import os
import time

from litellm import acompletion

from agents.context import get_agent_name, get_run_id
from app.core.config import get_settings

settings = get_settings()

AGENT_MODELS = {
    "research": "research_agent",
    "content": "content_agent",
    "visual": "visual_agent",
    "seo": "seo_agent",
}

# Populated by pipeline service during a run
_run_metrics: dict[str, object] = {}


def register_run_metrics(run_id: str, metrics: object) -> None:
    _run_metrics[run_id] = metrics


def unregister_run_metrics(run_id: str) -> None:
    _run_metrics.pop(run_id, None)


def use_mock_llm() -> bool:
    if os.environ.get("MOCK_LLM", "").lower() in ("1", "true", "yes"):
        return True
    if os.environ.get("MOCK_LLM", "").lower() in ("0", "false", "no"):
        return False
    return not any(
        [
            settings.google_api_key,
            settings.groq_api_key,
            settings.cerebras_api_key,
            settings.anthropic_api_key,
        ]
    )


def _mock_response(agent_name: str, user_prompt: str) -> str:
    topic = user_prompt.split("Topic:")[-1].strip()[:120] if "Topic:" in user_prompt else user_prompt[:120]

    if agent_name == "research":
        return json.dumps(
            {
                "brief": f"Research brief for: {topic}. Key trends include AI automation, multi-platform distribution, and human-in-the-loop quality gates.",
                "sources": ["https://example.com/ai-content", "https://example.com/trends"],
                "angles": ["practitioner guide", "thought leadership", "how-to thread"],
            }
        )
    if agent_name == "content":
        platforms = ["linkedin", "substack", "medium", "x", "instagram"]
        return json.dumps(
            {
                p: {
                    "content": f"[{p.upper()}] Draft about {topic} — tailored for {p} audience with clear CTA.",
                    "hook": f"Why {topic} matters now",
                }
                for p in platforms
            }
        )
    if agent_name == "visual":
        return json.dumps(
            {
                "prompts": [
                    f"Minimal editorial illustration about {topic}, purple/teal gradient",
                    f"Abstract data visualization for {topic}, dark mode",
                    f"Professional hero image for social post on {topic}",
                ]
            }
        )
    if agent_name == "seo":
        return json.dumps(
            {
                "keywords": ["AI content", "multi-agent", "automation", topic.split()[0] if topic else "content"],
                "hooks": [f"The future of {topic}", f"5 insights on {topic}"],
                "hashtags": ["#AI", "#ContentMarketing", "#Automation"],
            }
        )
    return json.dumps({"result": topic})


def _record_usage(agent_name: str, model: str, input_tokens: int, output_tokens: int, latency_ms: int) -> None:
    run_id = get_run_id()
    if not run_id:
        return
    metrics = _run_metrics.get(run_id)
    if metrics is None:
        return
    metrics.add_llm_usage(input_tokens, output_tokens, model=model)
    # Per-call trace data stored on metrics for node-level flush
    metrics.llm_calls.append(
        {
            "agent": agent_name or get_agent_name(),
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "latency_ms": latency_ms,
        }
    )


async def call_llm(
    agent_name: str,
    system_prompt: str,
    user_prompt: str,
    *,
    temperature: float = 0.7,
) -> str:
    model = AGENT_MODELS.get(agent_name, "research_agent")
    started = time.monotonic()

    if use_mock_llm():
        content = _mock_response(agent_name, user_prompt)
        latency_ms = int((time.monotonic() - started) * 1000)
        in_tok = max(len(user_prompt) // 4, 10)
        out_tok = max(len(content) // 4, 10)
        _record_usage(agent_name, "mock", in_tok, out_tok, latency_ms)
        return content

    api_base = settings.litellm_proxy_url or None
    kwargs: dict = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
    }
    if api_base:
        kwargs["api_base"] = api_base
        kwargs["api_key"] = os.environ.get("LITELLM_MASTER_KEY", "sk-acf-dev")

    try:
        response = await acompletion(**kwargs)
        content = response.choices[0].message.content or ""
        usage = getattr(response, "usage", None)
        in_tok = getattr(usage, "prompt_tokens", 0) or 0
        out_tok = getattr(usage, "completion_tokens", 0) or 0
        latency_ms = int((time.monotonic() - started) * 1000)
        _record_usage(agent_name, model, in_tok, out_tok, latency_ms)
        return content
    except Exception:
        # Fallback to mock when providers unavailable (local dev without keys)
        content = _mock_response(agent_name, user_prompt)
        latency_ms = int((time.monotonic() - started) * 1000)
        _record_usage(agent_name, "mock-fallback", 50, 100, latency_ms)
        return content
