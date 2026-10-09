from fastapi import APIRouter
from tech_samachar.api.v1.endpoints import news, topics, search, health, preferences, bookmarks, feedback, briefing

api_router = APIRouter()
api_router.include_router(news.router, prefix="/news", tags=["news"])
api_router.include_router(topics.router, prefix="/topics", tags=["topics"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(preferences.router, prefix="/preferences", tags=["preferences"])
api_router.include_router(bookmarks.router, prefix="/bookmarks", tags=["bookmarks"])
api_router.include_router(feedback.router, prefix="/feedback", tags=["feedback"])
api_router.include_router(briefing.router, prefix="/briefing", tags=["briefing"])
