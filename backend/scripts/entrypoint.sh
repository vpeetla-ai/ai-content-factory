#!/bin/bash
set -euo pipefail

cd /app

echo "==> AI Content Factory API starting (APP_ENV=${APP_ENV:-development})"

if [ "${RUN_MIGRATIONS_ON_STARTUP:-false}" = "true" ]; then
  echo "==> Running Alembic migrations"
  alembic upgrade head
fi

PORT="${PORT:-8000}"
# Free-tier hosts (Render) OOM with multiple workers — default to 1 in production
if [ "${APP_ENV:-development}" = "production" ]; then
  WORKERS="${WORKERS:-1}"
else
  WORKERS="${WORKERS:-2}"
fi

if [ "${APP_ENV:-development}" = "production" ]; then
  echo "==> Starting Gunicorn with ${WORKERS} worker(s) on port ${PORT}"
  exec gunicorn app.main:app \
    -k uvicorn.workers.UvicornWorker \
    -b "0.0.0.0:${PORT}" \
    --workers "${WORKERS}" \
    --timeout 120 \
    --graceful-timeout 30 \
    --access-logfile - \
    --error-logfile -
else
  echo "==> Starting Uvicorn (development) on port ${PORT}"
  exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT}" --reload
fi
