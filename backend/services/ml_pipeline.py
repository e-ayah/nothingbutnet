

import os, sys, tempfile
from pathlib import Path
import requests
 
# make the repo root importable so `import ml...` works when uvicorn runs from backend/
sys.path.append(str(Path(__file__).resolve().parents[2]))
from ml.analysis_pipeline import analyze
from services.cloudinary import upload_video
 
def run(video_url: str, session_id: str) -> dict:
    """Download the video, run the ML pipeline, upload the annotated video.
    Returns the contract's analysis dict. Raises on failure (the router marks the session failed)."""
    src = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
    annotated = None
    try:
        with requests.get(video_url, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(src, "wb") as f:
                for chunk in r.iter_content(1 << 20):
                    f.write(chunk)
        output = analyze(src)
        if isinstance(output, tuple) and len(output) == 2:
            result, annotated = output
        else:
            result = output
            annotated = None
        result["session_id"] = session_id
        result["annotated_video_url"] = upload_video(annotated) if annotated and annotated != src else video_url
        return result
    finally:
        for p in (src, annotated):
            if p and os.path.exists(p):
                os.remove(p)
