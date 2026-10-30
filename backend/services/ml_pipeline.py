import subprocess
import imageio_ffmpeg
import os, sys, tempfile
from pathlib import Path
import requests

def shrink_video(src: str) -> str:
    """Copy of the video at most 640 px wide and 10 s long."""
    out = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name

    subprocess.run(
        [
            imageio_ffmpeg.get_ffmpeg_exe(),
            "-y", "-i", src,
            "-t", "10",
            "-vf", "scale='min(640,iw)':-2",
            "-an", out
        ],
        check=True,
        capture_output=True
    )

    return out
 
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
        small = shrink_video(src)
        output = analyze(small)
        if isinstance(output, tuple) and len(output) == 2:
            result, annotated = output
        else:
            result = output
            annotated = None
            small = None
        result["session_id"] = session_id
        result["annotated_video_url"] = upload_video(annotated) if annotated and annotated != src else video_url
        return result
    finally:
        for p in (src, small, annotated):
            if p and os.path.exists(p):
                os.remove(p)
