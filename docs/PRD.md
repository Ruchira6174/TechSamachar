# Tech Samachar PRD

## Overview
Tech Samachar is a personalized, AI-powered technology news platform for personal use. It aggregates tech news, categorizes it by topics, summarizes it with AI, and ranks it based on user preferences.

## Core Features
1. **News Aggregation:** RSS feeds, tech blogs, APIs.
2. **AI Summarization & Classification:** Classify articles into tech topics and generate concise summaries.
3. **Personalized Feed:** Ranking algorithm based on topic preference, freshness, source quality, and novelty.
4. **Key Topics:** Quantum Computing, Cloud Computing, Generative AI (default higher priority), plus general tech.
5. **Dashboard:** Personalized feed, bookmarks, topic filters, search, daily briefing.

## Non-Functional Requirements
- Minimal, professional editorial-style UI.
- Maintainable architecture, separate frontend (React) and backend (FastAPI).
- PostgreSQL for data persistence.
- Replaceable AI providers, with fallback if not configured.
- No direct external calls from frontend to news sources/AI.
