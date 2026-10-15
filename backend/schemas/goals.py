from pydantic import BaseModel

class GoalCreate(BaseModel):
    checkpoint: str
    target_angle: float

class GoalOut(BaseModel):
    id: str
    checkpoint: str
    target_angle: float
    current_angle: float
    progress: float