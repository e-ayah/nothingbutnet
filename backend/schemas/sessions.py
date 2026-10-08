from typing import List, Literal, Optional
from pydantic import BaseModel
from schemas.analysis import Angles, FeedbackItem

class UploadResponse(BaseModel):
    session_id: str
    video_url: str
    status: str

class SessionSummary(BaseModel):
    session_id: str
    created_at: str
    overall_score: Optional[float] = None  # null while processing
    status: Literal['processing', 'done', 'failed'] # has to be one of these choices
    error: Optional[str] = None

class SessionDetail(BaseModel):
    session_id: str
    video_url: str
    annotated_video_url: Optional[str] = None  # null while processing
    angles: Optional[Angles] = None  # optional
    feedback: Optional[List[FeedbackItem]] = None  # optional
    score: Optional[float] = None  # null while processing
    status: Literal['processing', 'done', 'failed']
    error: Optional[str] = None