from pydantic import BaseModel
from typing import List

# everything per api contract

class Angles(BaseModel):
    elbow_angle: float
    knee_angle: float
    shoulder_angle: float

class FeedbackItem(BaseModel):
    checkpoint: str
    angle: float
    status: str
    tip: str

class AnalysisResponse(BaseModel):
    session_id: str
    release_frame: int
    angles: Angles
    feedback: List[FeedbackItem]
    overall_score: float
    annotated_video_url: str
    processed_at: str

