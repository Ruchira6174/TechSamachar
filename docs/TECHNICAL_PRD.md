# Technical PRD

## Architecture
- **Frontend:** React, TypeScript, Vite, Tailwind CSS, shadcn/ui.
- **Backend:** Python 3.12, FastAPI, SQLAlchemy, PostgreSQL.
- **Infrastructure:** Docker/Compose for local DB.

## Data Models
- **Article:** ID, Title, URL, Source ID, Published Date, Content, Summary, AI Status.
- **Source:** ID, Name, URL, Feed URL, Quality Score.
- **Topic:** ID, Name, Description.
- **ArticleTopic:** Article ID, Topic ID.
- **UserPreference:** Topic weights, read history.
- **Bookmark:** User ID, Article ID.

## Ranking Algorithm
Initial weights: Topic Preference (40%), Topic Relevance (25%), Freshness (20%), Source Quality (10%), Novelty (5%).

## AI Integration
- Shared interface for AI provider (OpenAI, Anthropic, Gemini).
- Use Pydantic for structured outputs.
- Retries and fallbacks.
