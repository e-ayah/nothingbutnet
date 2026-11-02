import time

import numpy as np
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import get_db

router = APIRouter()


@router.get("")
def health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "db": True}
    except Exception as e:
        print(f"Database connection error: {type(e).__name__}: {e}")
        return {"status": "ok", "db": False}


@router.get("/ml")
def health_ml():
    t = time.perf_counter()

    import cv2
    import mediapipe as mp

    from services import ml_pipeline  # noqa: F401

    with mp.solutions.pose.Pose(static_image_mode=True) as pose:
        pose.process(
            np.zeros((256, 256, 3), dtype=np.uint8)
        )

    # `resource` only exists on Mac/Linux - importing it at the top would stop
    # the whole backend from starting on Windows laptops.
    try:
        import resource
        import sys
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        # Linux (Render) reports KB, macOS reports bytes
        peak_memory_mb = round(peak / (1024 * 1024 if sys.platform == "darwin" else 1024))
    except ImportError:
        peak_memory_mb = None

    return {
        "ok": True,
        "mediapipe": mp.__version__,
        "opencv": cv2.__version__,
        "seconds": round(time.perf_counter() - t, 2),
        "peak_memory_mb": peak_memory_mb,
    }
