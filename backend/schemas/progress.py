from typing import List
from pydantic import BaseModel
from backend.schemas.analysis import Angles

class ProgressSession(BaseModel): # used as list for sessions in ProgressResponse
    session_id: str
    created_at: str
    angles: Angles
    score: float

class Trends(BaseModel): # used as object for trends in Progres Response
    elbow_angle: List[float]
    knee_angle: List[float]
    shoulder_angle: List[float]

class ProgressResponse(BaseModel):
    sessions: List[ProgressSession]
    trends: Trends
    improvement_summary: str