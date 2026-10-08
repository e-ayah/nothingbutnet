# NothingButNet API Contract

The shared agreement between the frontend and backend. Field names here must match `backend/schemas/`.

## General rules

- All logged-in requests send the header: `Authorization: Bearer <token>`
- Any endpoint marked **Token required: Yes** returns `401 "Authentication required"` if the token is missing, invalid, or expired.
- A request body with missing or wrong-typed fields returns `422` (FastAPI's default validation error).
- Timestamps are ISO 8601 in UTC, e.g. `"2026-09-30T15:30:00Z"`.
- Session `status` is one of `'processing' | 'done' | 'failed'`, plus `error` (text, or `null` unless status is `failed`).
- A session that doesn't exist, or belongs to another user, returns `404 "Session not found"`.

## Summary

| Method | Path | Token | Success |
|---|---|---|---|
| POST | `/auth/signup` | No | 200 `{ user_id, token }` |
| POST | `/auth/login` | No | 200 `{ user_id, token }` |
| POST | `/sessions/upload` | Yes | 200 `{ session_id, video_url, status }` |
| GET | `/sessions` | Yes | 200 list of sessions |
| GET | `/sessions/:id` | Yes | 200 one session |
| DELETE | `/sessions/:id` | Yes | 204 No Content |
| POST | `/analysis/analyze` | Yes | 200 analysis result |
| GET | `/progress` | Yes | 200 progress |
| POST | `/goals` | Yes | 200 goal |
| GET | `/goals` | Yes | 200 list of goals |
| POST | `/feedback` | Yes | 200 |

---

## POST /auth/signup

- **Token required:** No
- **Request:** `{ email, password, name }`
- **Response:** `{ user_id, token }`

Example response:

```json
{
  "user_id": "12345",
  "token": "example-token"
}
```

Error responses:

| Code | Message |
|---|---|
| 400 | Invalid signup information |
| 409 | Email already registered |

## POST /auth/login

- **Token required:** No
- **Request:** `{ email, password }`
- **Response:** `{ user_id, token }`

Example response:

```json
{
  "user_id": "12345",
  "token": "example-token"
}
```

Error responses:

| Code | Message |
|---|---|
| 401 | Invalid email or password |

## POST /sessions/upload

- **Token required:** Yes
- **Request:** video file (multipart form)
- **Response:** `{ session_id, video_url, status: 'processing' }`

Example response:

```json
{
  "session_id": "session-001",
  "video_url": "https://cloudinary.com/...",
  "status": "processing"
}
```

Error responses:

| Code | Message |
|---|---|
| 400 | Invalid video file |
| 401 | Authentication required |

## GET /sessions

- **Token required:** Yes
- **Response:** list of `{ session_id, created_at, overall_score, status, error }`
- `overall_score` is `null` while the session is still processing.

Example response:

```json
[
  {
    "session_id": "session-001",
    "created_at": "2026-09-30T15:30:00Z",
    "overall_score": 67,
    "status": "done",
    "error": null
  }
]
```

Error responses:

| Code | Message |
|---|---|
| 401 | Authentication required |

## GET /sessions/:id

- **Token required:** Yes
- **Response:** `{ session_id, video_url, annotated_video_url, angles, feedback, score, status, error }`
- While `status` is `processing`, `annotated_video_url`, `angles`, `feedback`, and `score` are `null`.

Example response (finished session):

```json
{
  "session_id": "session-001",
  "video_url": "https://cloudinary.com/...",
  "annotated_video_url": "https://cloudinary.com/...",
  "angles": { "elbow_angle": 92.3, "knee_angle": 165.1, "shoulder_angle": 58.7 },
  "feedback": [
    { "checkpoint": "elbow_alignment", "angle": 92.3, "status": "good", "tip": "Great elbow alignment" }
  ],
  "score": 67,
  "status": "done",
  "error": null
}
```

Error responses:

| Code | Message |
|---|---|
| 401 | Authentication required |
| 404 | Session not found |

## DELETE /sessions/:id

- **Token required:** Yes
- **Response:** `204 No Content`

Error responses:

| Code | Message |
|---|---|
| 401 | Authentication required |
| 404 | Session not found |

## POST /analysis/analyze

- **Token required:** Yes
- **Request:** `{ session_id, video_url }`
- **Response:** `{ session_id, release_frame, angles, feedback, overall_score, annotated_video_url, processed_at }`

Example response:

```json
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
```

Error responses:

| Code | Message |
|---|---|
| 401 | Authentication required |
| 404 | Session not found |

## GET /progress

- **Token required:** Yes
- **Response:** `{ sessions: [ { session_id, created_at, angles, score } ], trends, improvement_summary }`

Example response:

```json
{
  "sessions": [
    {
      "session_id": "session-001",
      "created_at": "2026-09-30T15:30:00Z",
      "angles": { "elbow_angle": 92.3, "knee_angle": 165.1, "shoulder_angle": 58.7 },
      "score": 67
    }
  ],
  "trends": {
    "elbow_angle": [92.3, 88.1, 94.5],
    "knee_angle": [165.1, 168.2, 170.0],
    "shoulder_angle": [58.7, 61.2, 63.0]
  },
  "improvement_summary": "Your elbow angle improved 2.2 degrees"
}
```

Error responses:

| Code | Message |
|---|---|
| 401 | Authentication required |

## POST /goals

- **Token required:** Yes
- **Request:** `{ checkpoint, target_angle }`
- **Response:** the created goal, same shape as one item from `GET /goals`

Error responses:

| Code | Message |
|---|---|
| 401 | Authentication required |

## GET /goals

- **Token required:** Yes
- **Response:** list of `{ id, checkpoint, target_angle, current_angle, progress }` — `progress` is 0–1

Example response:

```json
[
  {
    "id": "12345",
    "checkpoint": "elbow_alignment",
    "target_angle": 92.3,
    "current_angle": 81.6,
    "progress": 0.86
  }
]
```

Error responses:

| Code | Message |
|---|---|
| 401 | Authentication required |

## POST /feedback

- **Token required:** Yes
- **Request:** `{ message, rating, screen }` — `rating` is 1–5

Error responses:

| Code | Message |
|---|---|
| 401 | Authentication required |
