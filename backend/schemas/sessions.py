from typing import List, Literal, Optional
from pydantic import BaseModel
from backend.schemas.analysis import Angles, FeedbackItem

class UploadResponse(BaseModel):
    session_id: str
    video_url: str
    status: str

class SessionSummary(BaseModel):
    session_id: str
    created_at: str
    overall_score: float
    status: Literal['processing', 'done', 'failed'] # has to be one of these choices
    error: Optional[str] = None

class SessionDetail(BaseModel):
    session_id: str
    video_url: str
    annotated_video_url: str
    angles: Optional[Angles] = None  # optional
    feedback: Optional[List[FeedbackItem]] = None  # optional
    score: float
    status: Literal['processing', 'done', 'failed']
    error: Optional[str] = None