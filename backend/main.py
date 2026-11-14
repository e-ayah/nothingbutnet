
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import (
    health,
    auth,
    upload,
    sessions,
    analysis,
    progress,
    goals,
    feedback,
    insights,
    friends,
    compare,
)

app = FastAPI(title="NothingButNet API")

# Only allow approved websites and local development addresses.
origins = [
    origin.strip()
    for origin in os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:8081,http://localhost:19006"
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registered once here — other tickets don't edit this file.
app.include_router(health.router, prefix="/health")
app.include_router(auth.router, prefix="/auth")
app.include_router(upload.router, prefix="/sessions")
# compare before sessions so GET /sessions/compare isn't captured by /sessions/{session_id}
app.include_router(compare.router, prefix="/sessions")
app.include_router(sessions.router, prefix="/sessions")
app.include_router(analysis.router, prefix="/analysis")
app.include_router(progress.router, prefix="/progress")
app.include_router(goals.router, prefix="/goals")
app.include_router(feedback.router, prefix="/feedback")
app.include_router(insights.router, prefix="/insights", tags=["insights"])
app.include_router(friends.router, prefix="/friends", tags=["friends"])
