# API contract — implemented snapshot

Audited November 10, 2026 against `develop` **55b077f** by importing `backend/main.py` and generating the same OpenAPI schema used by `/docs`. This branch also includes the user-authorized signup regression fix described below. The live [Swagger UI](https://nothingbutnet-0l0a.onrender.com/docs) / [OpenAPI JSON](https://nothingbutnet-0l0a.onrender.com/openapi.json) was subsequently fetched on November 10, 2026. It serves an older API; the verified deployment differences below distinguish it from this branch.

Base URL: `http://localhost:8000` locally, or the configured deployment URL. UUIDs below are real UUID strings; human-readable IDs in old examples were placeholders.

## Conventions

Protected routes use `Authorization: Bearer <token>`. Obtain a token through signup/login, then use Swagger's HTTPBearer **Authorize** control. Tokens expire after seven days by default. Do not send JWT signing keys to the app.

- Missing auth: **401**, `{"detail":"Not logged in"}`.
- Invalid/expired token: **401**, `{"detail":"Your session expired. Log in again."}`.
- Validation failures on typed paths/query/body/file inputs: **422**, with FastAPI's `detail` list. Business errors use `{"detail":"…"}`.
- Success codes below are explicit; unmodeled responses are described from router code. OpenAPI lists 200/202/204 and automatic validation responses, but most runtime business errors are not annotated in it.
- No request should be assumed to return the full ML analysis object merely because that Pydantic class exists in `schemas/analysis.py`.

## Route inventory

| Method | Path | Auth | Success |
|---|---|---|---|
| GET | `/health` | No | 200 `{status, db}` |
| GET | `/health/ml` | No | 200 `{ok, mediapipe, opencv, seconds, peak_memory_mb}` |
| POST | `/auth/signup` | No | 200 `{user_id, token}` |
| POST | `/auth/login` | No | 200 `{user_id, token}` |
| GET | `/auth/me` | Yes | 200 `{id, name, email, username}` |
| PATCH | `/auth/me` | Yes | 200 `{id, name, email, username}` |
| POST | `/sessions/upload` | Yes | 200 `{session_id, video_url, status}` |
| GET | `/sessions` | Yes | 200 `SessionSummary[]` |
| GET | `/sessions/{session_id}` | Yes | 200 `SessionDetail` |
| PATCH | `/sessions/{session_id}` | Yes | 200 updated session subset plus `made` |
| GET | `/sessions/compare?a=…&b=…` | Yes | 200 `{a, b, changes}` (runtime gap below) |
| POST | `/analysis/analyze` | Yes | **202** `{session_id, status}` |
| GET | `/progress` | Yes | 200 `{sessions, trends, improvement_summary}` |
| GET | `/insights/recurring` | Yes | 200 insight array (runtime gap below) |
| POST | `/friends/requests` | Yes | 200 `{request_id, status:"pending"}` |
| GET | `/friends/requests` | Yes | 200 `{incoming, outgoing}` |
| POST | `/friends/requests/{id}/accept` | Yes | 200 `{friend}` |
| POST | `/friends/requests/{id}/decline` | Yes | **204**, no body |
| GET | `/friends` | Yes | 200 `Friend[]` |
| DELETE | `/friends/{user_id}` | Yes | **204**, no body |

Public diagnostic routes also registered: `GET /sessions/upload/ping`, `/sessions/ping`, `/progress/ping`, `/goals/ping`, `/feedback/ping`; each returns 200 `{"router":"<area>"}`. Goals and feedback have no other routes.

## Authentication

### POST /auth/signup

**The request is one flat JSON object**, matching the app. The optional username is part of `SignupRequest`, not a second body parameter:

```json
{
  "email":"player@example.com", "password":"example-password",
  "name":"Example Player", "username":"example_player"
}
```

`email`, `password`, `name` are required strings. `username` is optional/null. An omitted username is derived from the name with a random three-digit suffix. Supplied usernames are lowercased and validated for 3–20 lowercase letters, digits or underscores. Email is lowercased. No password-length validator is currently declared in the schema.

Returns `{"user_id":"<uuid>","token":"<jwt>"}`. Business errors: **400** `Email already registered`, `Username must be between 3 and 20 characters`, `Username must contain only lowercase letters, numbers, or underscores`, or `Username already taken`. Missing required fields or an invalid field type return **422**. The previous endpoint accidentally required a nested `body`; this branch fixes that regression without changing username normalization, validation or generated defaults.

### POST /auth/login

Flat request: `{"email":"player@example.com","password":"example-password"}`. Returns the same auth response. Wrong email/password: **401** `Wrong email or password`.

### GET /auth/me and PATCH /auth/me

GET returns `{id, name, email, username}` for the authenticated user. PATCH accepts `{"username":"new_name"}` and returns that same shape; it uses the signup username validation/error messages and **400** for conflicts. Username is nullable in the database and may be null for legacy data.

## Sessions and analysis

### POST /sessions/upload

Multipart request with a single required field **`file`** (`UploadFile`). The supplied content type must begin with `video/`. Returns `{session_id, video_url, status:"processing"}` after Cloudinary upload and database insert. It does **not** start analysis itself.

Errors: **400** `Please upload a video file`; **502** `Couldn't save the video. Try again.`; **500** `Couldn't save the session.`; **422** missing form field. The route does not currently enforce the planned file-size/duration/darkness/person validator. Analysis preprocessing later truncates to 10 seconds; that is not upload validation.

### GET /sessions

Current user's sessions, newest first:

```json
[{
  "session_id":"<uuid>", "created_at":"2026-11-10T12:00:00",
  "overall_score":null, "status":"processing", "error":null
}]
```

`SessionSummary` contains `session_id:string`, `created_at:string`, `overall_score:number|null`, `status:"processing"|"done"|"failed"`, `error:string|null`. **Current mapping omission:** the route does not pass the stored error into the schema, so this list's `error` stays null even on failed sessions. Read the detail endpoint for the real failure message.

### GET /sessions/{session_id}

Returns:

```json
{
  "session_id":"<uuid>", "video_url":"https://res.cloudinary.com/…",
  "annotated_video_url":null, "angles":null, "feedback":null,
  "score":null, "status":"processing", "error":null
}
```

When available, `angles` is `{elbow_angle:number, knee_angle:number, shoulder_angle:number}`; `feedback` is `[{checkpoint:string, angle:number, status:string, tip:string}]`. `score`/annotated URL are nullable. Status is processing/done/failed. **404** `Session not found` covers both absent and other users' sessions; malformed UUID gives **422**. The current detail response does **not** include `made`, `created_at`, `release_frame` or `processed_at`.

### PATCH /sessions/{session_id}

Body: `{"made":true}` (or false). Returns **200** `{session_id, video_url, annotated_video_url, score, status, error, made}`. It does not return angles/feedback. `made` is a user label, not a detector prediction; null is allowed in the database but not in this patch request. Wrong owner/missing session: **404**, not 403. Malformed UUID/missing boolean: **422**.

### POST /analysis/analyze

Body: `{"session_id":"<uuid>","video_url":"https://res.cloudinary.com/…"}`. Both strings are required by the current schema. The server checks session ownership and uses the URL stored in the session; it does not use the caller-supplied URL for processing.

Returns **202 Accepted** immediately: `{"session_id":"<uuid>","status":"processing"}`. Missing/other-user session or an invalid session ID string: **404** `Session not found`. Poll `GET /sessions/{session_id}` for terminal status:

- **done:** saved score, angles/feedback and annotated video URL.
- **failed:** `error` is filming advice when no release is detected, or `Something went wrong while analyzing your video. Please try again.` on other pipeline errors.

This uses FastAPI background tasks with a process-local lock, not a durable queue. Restarting a worker can lose in-flight work. Repeat requests can enqueue repeat work; no idempotency guard is implemented. The former synchronous 200 analysis contract was inaccurate.

### GET /sessions/compare

Required query strings `a`, `b`. Intended response: `{a:CompareSession, b:CompareSession, changes}`. `CompareSession` is `{session_id, created_at, video_url, annotated_video_url, angles, score}`; changes contains the three angle keys and score, each computed as **b minus a**, rounded to one decimal. Missing angle values yield null deltas. Missing/non-owned/not-done sessions give **404** `Session not found`; missing query arguments give **422**.

**Known runtime defect:** `load()` reads `AnalysisResult.annotated_video_url` and `.overall_score`, neither of which exists on that model (both are stored on `ShotSession`). A real matching row can raise **500**. Existing comparison tests stub `load`, so passing them does not establish a working database integration. Query IDs are typed as strings, so malformed UUID strings are not guaranteed a clean validation response.

## Progress and recurring feedback

### GET /progress

Returns `{sessions, trends, improvement_summary}`. `sessions` contains completed, owned sessions with all three angle measurements, in oldest-first order: `{session_id, created_at, angles, score}`. `trends` contains elbow/knee/shoulder arrays in that same order. `improvement_summary` is a string generated by `services/summary.py`. Empty history yields empty arrays and a summary string; score should be numeric for complete records. The app currently returns mock progress by default.

### GET /insights/recurring

Intended output: `[{checkpoint, label, count, out_of, latest_tip}]`. It looks at the five newest done sessions, requires at least three sessions, and reports a checkpoint with at least three `needs_work` feedback rows. Fewer than three sessions returns `[]`.

**Known runtime defect:** the route uses `FeedbackItem.checkpoint`, while the database model calls it `checkpoint_name`. With qualifying feedback rows it can raise **500**. Unit tests use fake rows with `checkpoint`; they do not exercise this mismatch. The frontend currently always returns mock insights because it checks the truthiness of the `MOCKS` object.

## Friends

`Friend = {user_id:string, name:string, username:string|null}`. Only names/usernames are returned by these endpoints, never emails. Request/user IDs are UUIDs.

### POST /friends/requests

Body: `{"username":"exact_username"}`. Performs an exact lowercased lookup, returning **200** `{request_id, status:"pending"}`. Errors:

| Code | Detail |
|---|---|
| 400 | `You can't add yourself` |
| 400 | `You're already friends or have a pending request` |
| 404 | `No user with that username` |

The duplicate case is **400**, not the formerly documented 409. Whitespace is not trimmed by the real server. The schema requires a string; route lookup, not a search endpoint, determines whether it exists.

### GET /friends/requests

Returns `{incoming:[{request_id, from:Friend}], outgoing:[{request_id, to:Friend}]}` for pending requests only. Both arrays may be empty. No ordering guarantee is declared.

### POST /friends/requests/{id}/accept

No request body. **200** `{friend:Friend}`. Request must be pending and the caller must be its recipient: **404** `Friend request not found`, **403** `User is not the recipient of this request`, or **422** malformed UUID.

### POST /friends/requests/{id}/decline

No body. Same pending/recipient rules and error messages; **204**, no content, on success. Decline deletes the pending request. There is no separate outgoing-cancellation endpoint in this snapshot.

### GET /friends

Returns a list of Friends for accepted relationships in either direction, or `[]`. No ordering guarantee is declared.

### DELETE /friends/{user_id}

**204**, no content. Deletes the caller's relationship to the given user, in either direction. Current implementation can delete a pending relationship too; it does not filter status to accepted. **404** `Friend not found` if no relationship exists; **422** malformed UUID. The target is the other user's ID, not the relationship/request ID.

## Health and diagnostics

`GET /health` returns `{"status":"ok","db":true|false}` with HTTP 200 even if a database query fails. Use the `db` field to assess readiness.

`GET /health/ml` initializes MediaPipe with a blank frame and returns `{ok:true, mediapipe:string, opencv:string, seconds:number, peak_memory_mb:number|null}`. This confirms dependency/model initialization, not shot-analysis accuracy or database health. An initialization exception can return 500.

## Known gaps and deployment parity

The following former contract entries are **not implemented** on audited develop:

- `DELETE /sessions/{session_id}` (only GET/PATCH exist).
- `GET /leaderboard` (the screen/client remains mocked).
- `GET /goals`, `POST /goals`, `POST /feedback` (only public ping scaffolds exist).

Do not treat a hypothetical schema for those routes as a live API promise. Clients currently reference some missing routes, and the Friends UI is pending PR #103. Friends/Leaderboard navigation registration is also pending. Track changes as Finals feature-owner PRs merge.

### Verified live deployment differences

The public deployed schema was successfully fetched and compared with this branch's generated schema on November 10, 2026, following earlier timeouts. It exposes **14 operations**, compared with **25** locally. These are observed schema differences, not inferred production behavior:

| Area | Live `/openapi.json` | This branch / source |
|---|---|---|
| Signup | Flat `SignupRequest` with email/password/name only | Same flat shape plus optional username, with validation/default generation |
| Analysis | `POST /analysis/analyze` advertises **200** | **202** background-task acceptance, then poll session detail |
| Friends | No friends paths | Six friends operations registered |
| Profile/session updates | No PATCH routes | `PATCH /auth/me`, `PATCH /sessions/{session_id}` |
| Progress, insights, comparison | Only progress ping; no real routes | `GET /progress`, `/insights/recurring`, `/sessions/compare` |
| ML diagnostics | No `/health/ml` | `GET /health/ml` |
| Analysis ping | `GET /analysis/ping` exists | No analysis ping registered |
| Session response schemas | Detail/summary fields match this branch | Shapes described above; runtime mapper caveats still apply |

The deployment therefore needs an owner/PM update before the live service can be described as matching the latest source. This documentation/CI work does not deploy or merge application code. After deployment, repeat the method/path, field and status-code comparison and verify authenticated flows; Swagger alone does not expose the comparison/recurring runtime defects or prove mock-backed app calls are live. This live schema audit was read-only and created no production users/videos.
