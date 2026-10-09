from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tech_samachar.api.v1.router import api_router
from tech_samachar.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for Tech Samachar",
    version="0.1.0"
)

import logging
from fastapi.responses import JSONResponse
from fastapi import Request

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.CORS_ORIGINS.split(',')] if settings.CORS_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected internal error occurred."},
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

# Legacy health for root level
@app.get("/health")
def root_health_check():
    return {"status": "ok", "message": "Tech Samachar Backend is running"}
