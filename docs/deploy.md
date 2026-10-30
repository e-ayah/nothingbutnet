Step 1: create .env file in the backend folder with DATABASE_URL url containing Supabase direct connection URL
Step 2: cd backend
Step 3: alembic upgrade head
Step 4: create nothingbutnet render environment using the following values: CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, CLOUDINARY_CLOUD_NAME, DATABASE_URL(session pooler), PYTHON_VERSION, SECRET_KEY
Step 5: https://nothingbutnet-0l0a.onrender.com/health

## ML on the server (Valkyries#06)

- `render.yaml` uses `plan: free`, no rootDir, and starts with `uvicorn main:app --app-dir backend`.
- The build installs `backend/requirements.txt`, then swaps in headless OpenCV (`opencv-contrib-python-headless==4.10.0.84`).
- Check the ML works: https://nothingbutnet-0l0a.onrender.com/health/ml should return `"ok": true` with the mediapipe and OpenCV versions.
- Before analysis, `shrink_video()` in `backend/services/ml_pipeline.py` cuts videos to at most **480 px wide and 10 s** (`MAX_WIDTH`, `MAX_SECONDS`).

### Memory and time per clip

Measured locally (macOS, Python 3.11, the same pinned packages) on a 12 s, 1080×1920 phone-style clip. Peak memory is the whole process, including about 154 MB for the app and ML libraries.

| Shrink setting | Frames analyzed | Seconds | Peak memory |
|---|---|---|---|
| None | 352 | 24.8 | 925 MB |
| 640 px, 10 s | 293 | 16–19 | 510–537 MB |
| 480 px, 10 s (used) | 293 | 11.0 | 383 MB |

Render's free plan allows 512 MB, so 640 px is too close; 480 px leaves about 130 MB of headroom. The release frame was the same at both widths.

**To do after deploying:** upload one real clip on Render and record its seconds and the `peak_memory_mb` from `/health/ml` here. Linux numbers may differ a little from the Mac numbers above.
