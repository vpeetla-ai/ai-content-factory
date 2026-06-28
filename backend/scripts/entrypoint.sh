#!/bin/bash
set -euo pipefail

cd /app

echo "==> AI Content Factory API starting (APP_ENV=${APP_ENV:-development})"

if [ "${RUN_MIGRATIONS_ON_STARTUP:-false}" = "true" ]; then
  echo "==> Running Alembic migrations"
  alembic upgrade head
fi

PORT="${PORT:-8000}"
WORKERS="${WORKERS:-2}"

if [ "${APP_ENV:-development}" = "production" ]; then
  echo "==> Starting Gunicorn with ${WORKERS} workers on port ${PORT}"
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
