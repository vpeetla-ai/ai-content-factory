"""LiteLLM client — routes to proxy with agent-specific model names + observability."""

import json
import os
import re
import time
from typing import Any

from litellm import acompletion

from agents.context import get_agent_name, get_root_trace_id, get_run_id
from app.core.config import get_settings
from app.core.logging import get_logger

settings = get_settings()
logger = get_logger(__name__)

PROXY_MODELS = {
    "research": "research_agent",
    "content": "content_agent",
    "visual": "visual_agent",
    "seo": "seo_agent",
}

DIRECT_MODELS = {
    "research": "gemini/gemini-2.5-flash",
    "content": "gemini/gemini-2.5-flash",
    "visual": "groq/llama-3.3-70b-versatile",
    "seo": "groq/llama-3.3-70b-versatile",
}

# OpenAI-compatible ids for aegis-llm-gateway (stub accepts any model name)
GATEWAY_MODELS = {
    "research": "openai/stub-small",
    "content": "openai/stub-small",
    "visual": "openai/stub-small",
    "seo": "openai/stub-small",
}

_run_metrics: dict[str, object] = {}


def llm_gateway_enabled() -> bool:
    """True when LLM_GATEWAY_URL is set (federated aegis-llm-gateway plane)."""
    s = get_settings()
    return bool((s.llm_gateway_url or "").strip())


def register_run_metrics(run_id: str, metrics: object) -> None:
    _run_metrics[run_id] = metrics


def unregister_run_metrics(run_id: str) -> None:
    _run_metrics.pop(run_id, None)


def use_mock_llm() -> bool:
    env_val = os.environ.get("MOCK_LLM", "").lower()
    if env_val in ("1", "true", "yes"):
        return True
    if env_val in ("0", "false", "no"):
        return False
    if not settings.mock_llm:
        return False
    return not any(
        [
            settings.google_api_key,
            settings.groq_api_key,
            settings.cerebras_api_key,
            settings.anthropic_api_key,
        ]
    )


def _use_litellm_proxy() -> bool:
    if use_mock_llm() or not settings.litellm_proxy_url:
        return False
    if settings.use_litellm_proxy:
        return True
    return os.environ.get("USE_LITELLM_PROXY", "").lower() in ("1", "true", "yes")


def _direct_api_key(model: str) -> str | None:
    if model.startswith("gemini/"):
        return settings.google_api_key or None
    if model.startswith("groq/"):
        return settings.groq_api_key or None
    if model.startswith("anthropic/"):
        return settings.anthropic_api_key or None
    if model.startswith("cerebras/"):
        return settings.cerebras_api_key or None
    return None


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


def parse_llm_json(raw: str) -> dict[str, Any] | None:
    """Parse JSON from LLM output, stripping markdown fences."""
    text = raw.strip()
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if fence:
        text = fence.group(1).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def _record_usage(agent_name: str, model: str, input_tokens: int, output_tokens: int, latency_ms: int, *, trace_id: str | None = None) -> None:
    run_id = get_run_id()
    if not run_id:
        return
    metrics = _run_metrics.get(run_id)
    if metrics is None:
        return
    metrics.add_llm_usage(input_tokens, output_tokens, model=model)
    metrics.llm_calls.append(
        {
            "agent": agent_name or get_agent_name(),
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "latency_ms": latency_ms,
            "langfuse_trace_id": trace_id,
        }
    )


async def call_llm(
    agent_name: str,
    system_prompt: str,
    user_prompt: str,
    *,
    temperature: float = 0.7,
) -> str:
    use_gateway = llm_gateway_enabled()
    use_proxy = False if use_gateway else _use_litellm_proxy()
    if use_gateway:
        models = GATEWAY_MODELS
    elif use_proxy:
        models = PROXY_MODELS
    else:
        models = DIRECT_MODELS
    model = models.get(agent_name, models["research"])
    started = time.monotonic()

    if use_mock_llm():
        content = _mock_response(agent_name, user_prompt)
        latency_ms = int((time.monotonic() - started) * 1000)
        in_tok = max(len(user_prompt) // 4, 10)
        out_tok = max(len(content) // 4, 10)
        _record_usage(agent_name, "mock", in_tok, out_tok, latency_ms)
        return content

    langfuse_trace_id: str | None = None
    langfuse_generation = None
    langfuse = None
    if settings.langfuse_configured:
        try:
            from app.core.observability import get_langfuse

            langfuse = get_langfuse()
            if langfuse:
                root_trace_id = get_root_trace_id() or get_run_id()
                trace = langfuse.trace(
                    id=root_trace_id,
                    name=f"llm.{agent_name}",
                    session_id=get_run_id(),
                    metadata={"agent": agent_name, "model": model},
                )
                langfuse_trace_id = trace.id
                langfuse_generation = trace.generation(
                    name=agent_name,
                    model=model,
                    input={"system": system_prompt, "user": user_prompt},
                )
        except Exception as exc:
            logger.warning("langfuse_trace_start_failed", error=str(exc))

    kwargs: dict = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "timeout": 90,
    }
    if use_gateway:
        s = get_settings()
        kwargs["api_base"] = s.llm_gateway_url.rstrip("/")
        kwargs["api_key"] = s.llm_gateway_api_key or "acf-gateway"
        # ADR-029: app selects; gateway enforces+records via role headers
        _thesis = {
            "research": "retriever",
            "content": "executor",
            "visual": "executor",
            "seo": "summarizer",
            "editor": "verifier",
        }.get(agent_name, "executor")
        _tier = {
            "research": "fast",
            "content": "high_reasoning",
            "visual": "specialized",
            "seo": "fast",
            "editor": "high_reasoning",
        }.get(agent_name, "fast")
        _selected = "gemini" if _thesis == "verifier" else "stub"
        kwargs["extra_headers"] = {
            "X-Tenant-Id": s.llm_gateway_tenant_id or "ai-content-factory",
            "X-Agent-Role": agent_name,
            "X-Thesis-Role": _thesis,
            "X-Data-Class": "internal",
            "X-Selected-Provider": _selected,
            "X-Model-Tier": _tier,
        }
        if _thesis == "verifier":
            kwargs["extra_headers"]["X-Generator-Provider"] = "stub"
            kwargs["extra_headers"]["X-Cache-Bypass"] = "true"
        if getattr(s, "llm_gateway_principal_id", ""):
            kwargs["extra_headers"]["X-Principal-Id"] = s.llm_gateway_principal_id
    elif use_proxy:
        kwargs["api_base"] = settings.litellm_proxy_url
        kwargs["api_key"] = settings.litellm_master_key or os.environ.get("LITELLM_MASTER_KEY", "sk-acf-dev")
    else:
        api_key = _direct_api_key(model)
        if api_key:
            kwargs["api_key"] = api_key

    try:
        response = await acompletion(**kwargs)
        content = response.choices[0].message.content or ""
        usage = getattr(response, "usage", None)
        in_tok = getattr(usage, "prompt_tokens", 0) or 0
        out_tok = getattr(usage, "completion_tokens", 0) or 0
        latency_ms = int((time.monotonic() - started) * 1000)
        _record_usage(agent_name, model, in_tok, out_tok, latency_ms, trace_id=langfuse_trace_id)
        if langfuse_generation is not None:
            langfuse_generation.end(output=content, usage={"input": in_tok, "output": out_tok})
        return content
    except Exception as exc:
        logger.warning("llm_call_failed", agent=agent_name, model=model, error=str(exc))
        if langfuse_generation is not None:
            langfuse_generation.end(level="ERROR", status_message=str(exc))
        if not settings.is_production:
            content = _mock_response(agent_name, user_prompt)
            latency_ms = int((time.monotonic() - started) * 1000)
            _record_usage(agent_name, "mock-fallback", 50, 100, latency_ms, trace_id=langfuse_trace_id)
            return content
        raise
