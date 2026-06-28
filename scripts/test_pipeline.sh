#!/usr/bin/env bash
# End-to-end smoke test for AI Content Factory API
set -euo pipefail

API="${API_BASE_URL:-http://localhost:8000/api/v1}"
TOPIC="${TEST_TOPIC:-The future of AI agents in enterprise content workflows}"

echo "==> Health"
curl -sf "http://localhost:8000/health" | python3 -m json.tool

echo ""
echo "==> Auth"
TOKEN=$(curl -sf -X POST "$API/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"clerk_token":"dev@acf.local"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
echo "Token acquired"

echo ""
echo "==> Start pipeline"
RUN=$(curl -sf -X POST "$API/pipelines/run" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"topic\":\"$TOPIC\",\"platforms\":[\"linkedin\",\"x\"]}")
RUN_ID=$(echo "$RUN" | python3 -c "import sys,json; print(json.load(sys.stdin)['run_id'])")
echo "Run ID: $RUN_ID"

echo ""
echo "==> Poll status (max 120s)"
for i in $(seq 1 60); do
  STATE=$(curl -sf "$API/pipelines/$RUN_ID" -H "Authorization: Bearer $TOKEN")
  STATUS=$(echo "$STATE" | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
  echo "  [$i] status=$STATUS"
  if [ "$STATUS" = "hitl_wait" ] || [ "$STATUS" = "done" ] || [ "$STATUS" = "error" ]; then
    break
  fi
  sleep 2
done

if [ "$STATUS" = "hitl_wait" ]; then
  echo ""
  echo "==> HITL approve"
  REVIEW=$(curl -sf "$API/hitl/$RUN_ID/review" -H "Authorization: Bearer $TOKEN")
  DECISIONS=$(echo "$REVIEW" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(json.dumps([{'platform': x['platform'], 'approved': True, 'edited_content': x['draft_content']} for x in d['drafts']]))
")
  curl -sf -X POST "$API/hitl/$RUN_ID/approve" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"decisions\": $DECISIONS}" | python3 -m json.tool

  echo ""
  echo "==> Poll after approve"
  for i in $(seq 1 30); do
    STATE=$(curl -sf "$API/pipelines/$RUN_ID" -H "Authorization: Bearer $TOKEN")
    STATUS=$(echo "$STATE" | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
    echo "  [$i] status=$STATUS"
    if [ "$STATUS" = "done" ] || [ "$STATUS" = "error" ]; then
      break
    fi
    sleep 2
  done
fi

echo ""
echo "==> Final state"
curl -sf "$API/pipelines/$RUN_ID" -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

echo ""
echo "==> Drafts"
curl -sf "$API/content/$RUN_ID/drafts" -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

echo ""
echo "==> Published"
curl -sf "$API/content/$RUN_ID/published" -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

echo ""
echo "✅ Smoke test complete — final status: $STATUS"
