# Finals #06: Full Regression Test + Automated Smoke Test

## Problem
Before the freeze, nothing automatically checked that NothingButNet's deployed API could run the core flow (sign up, upload a clip, analyze it, view results) from start to finish. Testing was manual, slow, and easy to skip, so a broken deploy could go unnoticed until someone opened the app.

## What we built / found
- **`scripts/smoke_test.py`:** one command that runs the core flow against any server and prints PASS/FAIL for each step, then exits with an error code on the first failure. Steps: health, signup, upload, analyze, wait for analysis to finish, get session, list sessions, progress. The server is chosen with `NBN_API` (default `http://localhost:8000`).
- **`testing/beta-checklist.md`:** added 14 manual steps for the newer features (Did it go in?, Share, Friends, Leaderboard, Compare, recurring-mistake card, Profile, Onboarding), with pass/fail columns for both regression passes.
- **Finding:** running the script against the live server on Fri 11/13 showed two problems that block the core flow (see Numbers and Known issues).

## Numbers

### Smoke test against the live server (https://nothingbutnet-0l0a.onrender.com), Fri 11/13

**Run 1:** current signup request shape
```
PASS health (0.7s)
FAIL signup - RuntimeError: 422 ... "loc":["body","email"],"msg":"Field required" ...
```
Result: 1 passed, 1 failed. The live server rejected the request shape that `develop` uses (`{"body": {...}, "username": ...}`) and appears to expect the older flat shape.

**Run 2:** script retries the old flat shape if the new one is rejected
```
PASS health (0.2s)
WARN: new signup shape rejected, retrying old flat shape (server may be outdated)
PASS signup (2.0s)
FAIL upload - RuntimeError: 502: {"detail":"Couldn't save the video. Try again."}
```
Result: 2 passed, 1 failed, 5 not run. `analyze`, `analysis done`, `get session`, `list sessions` and `progress` could not run because they need an uploaded session.

### Smoke test against a local backend
Health and signup passed. Upload failed with the same 502. The server log showed `Cloudinary upload failed: ValueError: Must supply api_key`, because local Cloudinary keys were not available. This is probably also the cause on the live server, but I could not see the live logs, so it is unconfirmed.

### Manual regression passes

| | Pass 1 (Thu 11/12) | Pass 2 (Sat 11/14) |
|---|---|---|
| Smoke test (live) | FAIL at signup (Run 1), FAIL at upload (Run 2) | not yet run |
| Checklist, web | not yet run | not yet run |
| Checklist, iPhone | not yet run | not yet run |

Per-step results are recorded in `testing/beta-checklist.md`. Manual checklist passes will be added once the live server can complete an upload. [FILL IN: if you ran any manual steps, replace "not yet run" with the real counts, e.g. 9/14 PASS.]

## Pictures
[FILL IN: add screenshots saved in `docs/writeups/img/`, for example:]
![Live smoke test output](img/smoke-test-live.png)

## Known issues

| Issue | What fails | Severity | Workaround |
|---|---|---|---|
| #115 | Live `/auth/signup` rejects the current request shape (nested `body` + `username`); live server looks older than `develop` | High: new app builds cannot sign up on live | None. The smoke test falls back to the old shape. |
| #116 | Live `POST /sessions/upload` returns 502 "Couldn't save the video" | High: blocks the core flow, so every later step is untested on live | None found |

## What's left
- The live server needs to be redeployed from `develop` and its video storage checked (Cloudinary config is the first suspect, unconfirmed). Then rerun the smoke test.
- Run the full manual checklist on web and iPhone for both passes once uploads work. Pass 2 results will follow in a second small PR.
- Local smoke-test runs need Cloudinary keys in `backend/.env`.
- Limits of this test: it checks that each step succeeds, not that the analysis results are correct, and it does not cover the social features (they are covered by the manual checklist).