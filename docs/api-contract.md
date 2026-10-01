POST /auth/signup
  Request:  { email, password, name }
  Response: { user_id, token }
  Method + path: POST /auth/signup
  Token required: No
  Example response: {
    "user_id": "12345"
    "token": "example-token"
  }
  Error responses: {
    400: "Invalid signup information"
    404: "Session not found"
  }
 
POST /auth/login
  Request:  { email, password }
  Response: { user_id, token }
  Method + path: POST /auth/login
  Token required: No
  Example response: {
    "user_id": "12345"
    "token": "example-token"
  }
  Error responses: {
    400: "Invalid login information"
    404: "Session not found"
  }
 
POST /sessions/upload
  Request:  video file (multipart form)
  Response: { session_id, video_url, status: 'processing' }
  Method + path: POST /sessions/upload
  Token required: Yes
  Example response: {
    "session_id": "session-001"
    "video_url": "https://cloudinary.com/..."
    "status": "processing"
  }
  Error responses: {
    400: "Invalid video file"
    401: "Authentication required"
    404: "Session not found"
  }
 
GET /sessions
  Response: [ { session_id, created_at, overall_score, status: done } ]
  Method + path: GET /sessions
  Token required: Yes
  Example response: {
    "session_id": "session-001"
    "created_at": "2026-09-30T15:30:00PT"
    "overall_score": 67
    "status": "done"
    "error": null
  }
  Error responses: {
    401: "Authentication required"
    404: "Session not found"
  }
 
GET /sessions/:id
  Response: { session_id, video_url, annotated_video_url, angles, feedback, score, status: processing }
  Method + path: GET /sessions/:id
  Token required: Yes
  Example response: {
    "session_id": "session-001"
    "video_url": "https://cloudinary.com/..."
    "annotated_video_url": "https://cloudinary.com/..."
    "angles": { "elbow_angle": 92.3, "knee_angle": 165.1, "shoulder_angle": 58.7 }
    "feedback": [
    { "checkpoint": "elbow_alignment", "angle": 92.3, "status": "good", "tip": "Great elbow alignment" }
    ]
    "score": 67
    "status": "processing
    "error": null
  }
  Error responses: {
    401: "Authentication required"
    404: "Session not found"
  }
 
POST /analysis/analyze
  Request: { session_id, video_url }
  Response:
{
  "session_id": "abc123",
  "release_frame": 45,
  "angles": { "elbow_angle": 92.3, "knee_angle": 165.1, "shoulder_angle": 58.7 },
  "feedback": [
    { "checkpoint": "elbow_alignment", "angle": 92.3, "status": "good", "tip": "Great elbow alignment" }
  ],
  "overall_score": 67,
  "annotated_video_url": "https://cloudinary.com/...",
  "processed_at": "2026-09-15T10:30:00Z"
}
  Method + path: POST /analysis/analyze
  Token required: Yes
  Error responses: {
    401: "Authentication required"
    404: "Session not found"
  }
 
GET /progress
  Response:
{
  "sessions": [ { session_id, created_at, angles, score } ],
  "trends": {
    "elbow_angle":    [92.3, 88.1, 94.5],
    "knee_angle":     [165.1, 168.2, 170.0],
    "shoulder_angle": [58.7, 61.2, 63.0]
  },
  "improvement_summary": "Your elbow angle improved 2.2 degrees"
}
  Method + path: GET /progress
  Token required: Yes
  Error responses: {
    401: "Authentication required"
    404: "Session not found"
  }

POST /goals
    Request: { checkpoint, target_angle }
    Method + path: POST /goals
    Token required: Yes
    Error responses: {
        401: "Authentication required"
        404: "Session not found"
    }

GET /goals
    Response: { id, checkpoint, target_angle, current_angle, progress (0–1) }
    Method + path: POST /goals
    Token required: Yes
    Example response: {
        "id": "12345"
        "checkpoint": "elbow_alignment"
        "target_angle": 92.3
        "current_angle": 81.6
        "progress": 0.86
    }
    Error responses: {
        401: "Authentication required"
        404: "Session not found"
    }

DELETE /sessions/:id 
    Method + path: DELETE /sessions/:id 
    Token required: Yes
    Error responses: {
        401: "Authentication required"
        404: "Session not found"
    }

POST /feedback
    Request: { message, rating 1–5, screen }
    Method + path: POST /feedback
    Token required: Yes
    Error responses: {
        401: "Authentication required"
        404: "Session not found"
    }
    

  
 
status on GET /sessions and GET /sessions/:id:  'processing' | 'done' | 'failed', plus error (text or null)
POST /goals        { checkpoint, target_angle }  →  goal
GET /goals         →  [ { id, checkpoint, target_angle, current_angle, progress (0–1) } ]
DELETE /sessions/:id  →  204 No Content
POST /feedback     { message, rating 1–5, screen }
All logged-in requests send the header:  Authorization: Bearer <token>
