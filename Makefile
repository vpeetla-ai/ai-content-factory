.PHONY: up down migrate api frontend install test dev

up:
	docker compose up -d postgres redis qdrant litellm

down:
	docker compose down

migrate:
	cd backend && . .venv/bin/activate && alembic upgrade head

api:
	cd .. && source backend/.venv/bin/activate && PYTHONPATH=backend:. uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

frontend:
	cd frontend && npm run dev

install:
	cd backend && python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
	cd frontend && npm install

test:
	./scripts/test_pipeline.sh

dev: up
	@echo "Infrastructure up. Run 'make api' and 'make frontend' in separate terminals."
