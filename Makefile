.PHONY: help db-up db-down setup-backend setup-frontend

help:
	@echo "Tech Samachar Development Commands"
	@echo "make db-up         - Start PostgreSQL database"
	@echo "make db-down       - Stop PostgreSQL database"
	@echo "make setup-backend - Install backend dependencies"
	@echo "make setup-frontend- Install frontend dependencies"
	@echo "make dev-backend   - Run backend dev server"
	@echo "make dev-frontend  - Run frontend dev server"

db-up:
	docker-compose up -d

db-down:
	docker-compose down

setup-backend:
	cd backend && pip install -r requirements.txt || pip install -e .

setup-frontend:
	cd frontend && npm install

dev-backend:
	cd backend && uvicorn src.tech_samachar.main:app --reload

dev-frontend:
	cd frontend && npm run dev
