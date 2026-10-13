
import os
import tempfile

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from database import get_db
from models import ShotSession
from schemas.sessions import UploadResponse
from services.cloudinary import upload_video
from services.deps import get_current_user

router = APIRouter()


@router.get("/upload/ping")
def ping():
    return {"router": "upload"}


@router.post("/upload", response_model=UploadResponse)
def upload(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if not file.content_type or not file.content_type.startswith("video/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a video file",
        )

    temp_path = None

    try:
        suffix = os.path.splitext(file.filename or "")[1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_path = temp_file.name

            while chunk := file.file.read(1024 * 1024):
                temp_file.write(chunk)

        video_url = upload_video(temp_path)

    
    except Exception as exc:
        print(f"Cloudinary upload failed: {type(exc).__name__}: {exc}")
        raise HTTPException(
            status_code=502,
            detail="Couldn't save the video. Try again.",
        )


    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        file.file.close()

    session = ShotSession(
        user_id=current_user["id"],
        video_url=video_url,
        status="processing",
    )

    try:
        db.add(session)
        db.commit()
        db.refresh(session)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Couldn't save the session.",
        )

    return UploadResponse(
        session_id=str(session.id),
        video_url=session.video_url,
        status=session.status,
    )
