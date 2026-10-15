from datetime import datetime, timezone

def run(video_url: str, session_id: str) -> dict:
    return {
        "session_id": session_id,
        "release_frame": 45,
        "angles": {"elbow_angle": 92.3, "knee_angle": 165.1, "shoulder_angle": 58.7},
        "feedback": [
            {"checkpoint": "elbow_alignment", "angle": 92.3, "status": "good",
             "tip": "Great elbow alignment"},
        ],
        "overall_score": 67,
        "annotated_video_url": video_url,
        "processed_at": datetime.now(timezone.utc).isoformat(),
    }
