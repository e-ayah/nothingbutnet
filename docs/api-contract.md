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
- **Request:** `{ email, password, name, username }` — `username` is optional
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

**## PATCH /sessions/:id**

- **Token required:** Yes
- **Request:** `{ made }` — `made` is a boolean (`true` or `false`)
- **Response:** the updated session, including `made`

Error responses:

| Code | Message |
|---|---|
| 401 | Authentication required |
| 403 | Session belongs to another user |
| 404 | Session not found |

---

**## POST /friends/requests**

- **Token required:** Yes
- **Request:** `{ username }`
- **Response:** `{ request_id, status }` — `status` is `"pending"`

Example response:

```json
{
  "request_id": "request-001",
  "status": "pending"
}
```

Error responses:

| Code | Message |
|---|---|
| 400 | Already friends or cannot send a friend request to yourself |
| 401 | Authentication required |
| 404 | User not found |
| 409 | A pending friend request already exists |

---

**## GET /friends/requests**

- **Token required:** Yes
- **Response:** `{ incoming, outgoing }` — `incoming` contains requests received, and `outgoing` contains requests sent.

Example response:

```json
{
  "incoming": [
    {
      "request_id": "request-001",
      "from": {
        "user_id": "user-001",
        "name": "John Doe",
        "username": "johndoe"
      }
    }
  ],
  "outgoing": [
    {
      "request_id": "request-002",
      "to": {
        "user_id": "user-002",
        "name": "Jane Doe",
        "username": "janedoe"
      }
    }
  ]
}
```

Error responses:

| Code | Message |
|---|---|
| 401 | Authentication required |

---

**## POST /friends/requests/:id/accept**

- **Token required:** Yes
- **Response:** `{ friend: { user_id, name, username } }`

Example response:

```json
{
  "friend": {
    "user_id": "user-001",
    "name": "John Doe",
    "username": "johndoe"
  }
}
```

Error responses:

| Code | Message |
|---|---|
| 401 | Authentication required |
| 403 | User is not the recipient of this request |
| 404 | Friend request not found |

---

**## POST /friends/requests/:id/decline**

- **Token required:** Yes
- **Response:** `204 No Content`

Error responses:

| Code | Message |
|---|---|
| 401 | Authentication required |
| 403 | User is not the recipient of this request |
| 404 | Friend request not found |

---

**## GET /friends**

- **Token required:** Yes
- **Response:** list of `{ user_id, name, username }`

Example response:

```json
[
  {
    "user_id": "user-001",
    "name": "John Doe",
    "username": "johndoe"
  }
]
```

Returns an empty array (`[]`) if the user has no friends.

Error responses:

| Code | Message |
|---|---|
| 401 | Authentication required |

---

**## DELETE /friends/:user_id**

- **Token required:** Yes
- **Response:** `204 No Content`

Error responses:

| Code | Message |
|---|---|
| 401 | Authentication required |
| 404 | Friend not found |

---

**## GET /leaderboard?period=week\|all**

- **Token required:** Yes
- **Response:** list of `{ rank, user_id, name, made, attempts, make_pct, avg_score, is_me }`

Definitions:
- `week` = current calendar week.
- `all` = all-time statistics.
- `made` = number of successful shots.
- `attempts` = total number of attempts.
- `make_pct` = successful shots divided by total attempts.
- `avg_score` = average session score.
- `is_me` = whether the entry belongs to the authenticated user.
- `rank` = position ordered by `avg_score` (descending). Tied users receive the same rank.

Example response:

```json
[
  {
    "rank": 1,
    "user_id": "user-001",
    "name": "John Doe",
    "made": 12,
    "attempts": 20,
    "make_pct": 0.60,
    "avg_score": 85.5,
    "is_me": false
  },
  {
    "rank": 2,
    "user_id": "user-002",
    "name": "Jane Doe",
    "made": 15,
    "attempts": 20,
    "make_pct": 0.75,
    "avg_score": 82.3,
    "is_me": true
  }
]
```

Error responses:

| Code | Message |
|---|---|
| 401 | Authentication required |

---

**## GET /sessions/compare?a=<id>&b=<id>**

- **Token required:** Yes
- **Response:** `{ a: SessionDetail, b: SessionDetail, changes }` — `changes` contains the differences between the two sessions, calculated as `b - a`. Positive values indicate increases; negative values indicate decreases. Missing measurements return `null`.

Example response:

```json
{
  "a": {
    "session_id": "session-001",
    "score": 70
  },
  "b": {
    "session_id": "session-002",
    "score": 75
  },
  "changes": {
    "score": 5
  }
}
```

---

**## GET /auth/me**

- **Token required:** Yes
- **Response:** `{ id, name, email, username }`

Example response:
```json
{
  "id": "12345",
  "name": "Maya Player",
  "email": "maya@example.com",
  "username": "maya482"
}
```

**## PATCH /auth/me**

- **Token required:** Yes
- **Request:** `{ username }`
- **Response:** `{ id, name, email, username }`

Error responses:

| Code | Message |
|---|---|
| 400 | Username must be between 3 and 20 characters / Username already taken |
| 401 | Authentication required |