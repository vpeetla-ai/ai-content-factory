# AI Content Factory API — production image
# Build from repository root (required for agents/ + backend/):
#   docker build -t acf-api .
#
# Render: use Dockerfile path = ./Dockerfile, Docker context = .

FROM python:3.12-slim AS base

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app /app/app
COPY backend/alembic /app/alembic
COPY backend/alembic.ini /app/alembic.ini
COPY backend/scripts/entrypoint.sh /app/entrypoint.sh
COPY agents /app/agents

RUN chmod +x /app/entrypoint.sh

ENV PYTHONPATH=/app
ENV APP_ENV=production
ENV RUN_MIGRATIONS_ON_STARTUP=true

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

ENTRYPOINT ["/app/entrypoint.sh"]
