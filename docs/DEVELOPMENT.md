# Development Setup

## Prerequisites
- Node.js 18+
- Python 3.12+
- Docker and Docker Compose

## Backend Setup
1. `cd backend`
2. Create virtual environment: `python -m venv .venv`
3. Activate it: `source .venv/Scripts/activate` (Windows) or `source .venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -e .[dev]`
5. Start dev server: `uvicorn src.tech_samachar.main:app --reload`

## Database Setup & Migrations
1. Start PostgreSQL: `make db-up` (or `docker-compose up -d`)
2. Generate migration (if model changes): `cd backend && alembic revision --autogenerate -m "Initial"`
3. Apply migrations: `cd backend && alembic upgrade head`

## Data Seeding & Ingestion
To populate the database with initial topics and default RSS sources:
`python src/tech_samachar/manage.py --seed`

To run one cycle of the ingestion pipeline to fetch new articles:
`python src/tech_samachar/manage.py --ingest`

## Frontend Setup
1. `cd frontend`
2. Install dependencies: `npm install`
3. Start dev server: `npm run dev`

## Daily Briefing Generation
To run the daily briefing generation manually (for testing or cron job):
`cd backend && python src/tech_samachar/manage.py --briefing`

## Testing
- Backend tests: `cd backend && pytest tests/`
- Frontend tests: `cd frontend && npm run test`

## Production Deployment
### Backend
1. Build the image: `docker build -t tech-samachar-backend ./backend`
2. Run it (provide secrets via env): 
   `docker run -p 8000:8000 -e DATABASE_URL=... -e AI_PROVIDER=... tech-samachar-backend`

### Frontend
1. Build the production image: `docker build -t tech-samachar-frontend ./frontend`
2. Run the NGINX container:
   `docker run -p 80:80 tech-samachar-frontend`

Ensure you pass appropriate CORS configurations for the backend in production using the `CORS_ORIGINS` environment variable.
