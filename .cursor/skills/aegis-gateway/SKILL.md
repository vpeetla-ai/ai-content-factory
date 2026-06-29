---
name: aegis-gateway
description: >-
  Integrate AegisAI gateway before tool side effects (notify, publish, deploy).
  Use when adding Slack/Telegram/WhatsApp notify, content publish, or any
  irreversible external action in VAP, AegisLoop, or ai-content-factory.
---

# AegisAI Gateway Integration

## When required

Any **side effect** leaving the system:

- Publish to LinkedIn/X/Substack
- Send Slack/Telegram/WhatsApp messages
- Deploy or git push to protected branches (prefer PR workflow)

## Pattern

```python
# integrations/aegis_gateway.py (existing in VAP, AegisLoop, Content Factory)
result = await gateway.request_tool(
    tool_name="notify_slack",
    payload={...},
    agent_id="...",
    run_id="...",
)
if result.requires_hitl:
    # pause until approval
```

## Env vars

```bash
AEGISAI_API_BASE_URL=https://...
AEGISAI_API_KEY=...
```

## Dev mode

- If gateway URL unset → **fail open** with logged warning (local dev only)
- Never fail open in production configs

## Do not

- Embed policy logic in orchestrator prompts — policy lives in AegisAI/OPA
- Bypass gateway "temporarily" in production code paths

## Reference

`aegisai-enterprise-agent-platform` — gateway SDK + `POST /api/gateway/tool-request`
