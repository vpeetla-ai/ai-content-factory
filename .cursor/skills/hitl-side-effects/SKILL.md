---
name: hitl-side-effects
description: >-
  Add human-in-the-loop gates for irreversible actions: LangGraph
  interrupt_before, AegisAI approval queue, UI approve/resume endpoints. Use
  when shipping, publishing, notifying, or merging agent-generated changes.
---

# HITL for Side Effects

## LangGraph pattern

```python
graph.compile(checkpointer=MemorySaver(), interrupt_before=["hitl"])
# First invoke stops before hitl node
# After human approval:
await graph.ainvoke({"hitl_approved": True}, config)
```

## AegisAI pattern

- `POST /api/gateway/tool-request` → `pending` | `approved` | `denied`
- UI polls or webhook; agent resumes on approval

## Content Factory

- Draft → review queue → human edit → publish (gateway-wrapped)

## LoopForge repo-fix

- `interrupt_before=["hitl"]` before push/PR when `create_pr=true`
- `POST /api/repo-fix/{run_id}/approve` resumes graph

## UX requirements

- Show **what** will happen (diff, channel, recipient)
- Show **why** agent chose this action (trace excerpt)
- Approve / Reject / Edit-and-approve

## Never

- Auto-approve production side effects without explicit env flag
- Skip audit log on approval/denial
