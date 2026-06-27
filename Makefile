.PHONY: dev up down migrate frontend install

up:
	docker compose up -d postgres redis qdrant

down:
	docker compose down

api:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

migrate:
	cd backend && alembic upgrade head

frontend:
	cd frontend && npm run dev

install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

dev: up
	@echo "Run 'make api' and 'make frontend' in separate terminals"
