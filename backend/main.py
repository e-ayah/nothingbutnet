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
)

app = FastAPI(title="NothingButNet API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registered once here — other tickets don't edit this file.
app.include_router(health.router, prefix="/health")
app.include_router(auth.router, prefix="/auth")
app.include_router(upload.router, prefix="/sessions")
app.include_router(sessions.router, prefix="/sessions")
app.include_router(analysis.router, prefix="/analysis")
app.include_router(progress.router, prefix="/progress")
app.include_router(goals.router, prefix="/goals")
app.include_router(feedback.router, prefix="/feedback")