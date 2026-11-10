import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, ForeignKey, Text, func, Boolean, Column, String, UniqueConstraint

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(20), unique=True, index=True, nullable=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    name: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

class ShotSession(Base):
    __tablename__ = "sessions"
    
    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    made = Column(Boolean, nullable=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    video_url: Mapped[str]
    annotated_video_url: Mapped[Optional[str]]
    overall_score: Mapped[Optional[float]]
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    status: Mapped[str] = mapped_column(default="processing")
    error: Mapped[Optional[str]]

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[UUID] = mapped_column(ForeignKey("sessions.id"))
    elbow_angle: Mapped[float]
    knee_angle: Mapped[float]
    shoulder_angle: Mapped[float]
    release_frame: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

class FeedbackItem(Base):
    __tablename__ = "feedback_items"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[UUID] = mapped_column(ForeignKey("sessions.id"))
    checkpoint_name: Mapped[str]
    angle_value: Mapped[float]
    status: Mapped[str]
    tip: Mapped[str] = mapped_column(Text)

class Goal(Base):
    __tablename__ = "goals"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id")) 
    checkpoint: Mapped[str]
    target_angle: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

class Friendship(Base):
    __tablename__ = "friendships"
    
    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    requester_id = Column(ForeignKey("users.id"), nullable=False, index=True)
    addressee_id = Column(ForeignKey("users.id"), nullable=False, index=True)
    status = Column(String(10), nullable=False, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    __table_args__ = (UniqueConstraint("requester_id", "addressee_id"),)
