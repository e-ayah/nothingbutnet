def analyze(video_path):
    # Returns fake analysis data in the format that the backend expects
    # (POST /analysis/analyze). The backend fills in session_id.
    result = {
        "session_id": None,
        "release_frame": 45,
        "angles": {
            "elbow_angle": 92.3,
            "knee_angle": 165.1,
            "shoulder_angle": 58.7
        },
        "feedback": [
            {
                "checkpoint": "elbow_alignment",
                "angle": 92.3,
                "status": "good",
                "tip": "Great elbow alignment"
            }
        ],
        "overall_score": 67,
        "annotated_video_url": "https://cloudinary.com/...",
        "processed_at": "2026-09-15T10:30:00Z"
    }

    return result

