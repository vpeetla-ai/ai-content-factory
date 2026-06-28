#!/bin/bash
set -euo pipefail

cd /app

echo "==> AI Content Factory API starting (APP_ENV=${APP_ENV:-development})"

if [ "${RUN_MIGRATIONS_ON_STARTUP:-false}" = "true" ]; then
  echo "==> Running Alembic migrations"
  alembic upgrade head
fi

PORT="${PORT:-8000}"

if [ "${APP_ENV:-development}" = "production" ]; then
  # Render free tier: single uvicorn process (gunicorn multi-worker OOMs)
  echo "==> Starting Uvicorn on port ${PORT} (production, 1 process)"
  exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port "${PORT}" \
    --timeout-keep-alive 120 \
    --log-level info
else
  echo "==> Starting Uvicorn (development) on port ${PORT}"
  exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT}" --reload
fi
