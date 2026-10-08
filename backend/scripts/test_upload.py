import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.cloudinary import upload_video

# Videos aren't committed (*.mp4 is gitignored) — pass your own clip path,
# or drop a local test_clip.mp4 next to this script.
DEFAULT_CLIP = os.path.join(os.path.dirname(__file__), "test_clip.mp4")

if __name__ == "__main__":
    clip = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CLIP
    if not os.path.exists(clip):
        sys.exit(f"No video at {clip} — usage: python scripts/test_upload.py path/to/clip.mp4")
    print(f"Uploading {clip} ...")
    url = upload_video(clip)
    print(f"Uploaded! Video URL: {url}")
