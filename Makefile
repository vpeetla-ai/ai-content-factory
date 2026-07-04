.PHONY: up down migrate api frontend install test dev lint invite

up:
	docker compose up -d postgres redis qdrant

down:
	docker compose down

migrate:
	cd backend && source .venv/bin/activate && alembic upgrade head

api:
	source backend/.venv/bin/activate && APP_ENV=development PYTHONPATH=backend:. uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

frontend:
	cd frontend && npm run dev

install:
	cd backend && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
	cd frontend && npm install

test:
	PYTHONPATH=backend:. pytest tests/ -q
	./scripts/test_pipeline.sh

dev: up
	@echo "Run in separate terminals:"
	@echo "  make api"
	@echo "  make frontend"

lint:
	cd backend && python -c "from app.main import app; from agents.graph import build_graph; print('ok')"

invite:
	source backend/.venv/bin/activate && PYTHONPATH=backend:. python backend/scripts/create_invite_code.py $(ARGS)
