# Security Review

## 1. Secret and File Checks

**Check: Search Git history for exposed secrets**
- Result: No confirmed real credentials found in the reviewed output.
- Action: Continue keeping passwords and API keys out of Git.

**Check: Verify `.env` and `venv/` are ignored**
- Result: Passed. No matching files were tracked by Git.
- Action: Keep these files in `.gitignore`.

## 2. Authentication Checks

**Check: Protected endpoints**
- Result: Core session, friend, upload, analysis, and progress routes require authentication.
- Action: Public health and ping routes remain accessible.

**Check: Missing authentication token**
- Result: Passed. Returns 401.

**Check: Invalid authentication token**
- Result: Passed. Returns 401.

**Check: Token with invalid user ID**
- Result: Passed. Returns 401.
- Action: Updated `backend/services/deps.py` to handle invalid user IDs safely.

## 3. User Privacy Checks

**Check: User B viewing User A's session**
- Result: Passed. Returns 404.

**Check: User B updating User A's session**
- Result: Passed. Returns 404.

**Check: User B comparing User A's sessions**
- Result: Passed. Returns 404.

**Check: Session deletion**
- Result: No DELETE endpoint found.
- Action: Reported as an issue for the PM.

**Check: Leaderboard privacy**
- Result: No leaderboard endpoint found.
- Action: Reported as an issue for the PM.

## 4. Input Validation

**Check: Non-video upload**
- Result: Passed. Returns 400.

**Check: Empty email and short password**
- Result: Not verified.
- Action: Needs review by the auth developer.

**Check: Very long username**
- Result: Not verified.
- Action: Needs review by the auth developer.

## 5. CORS Configuration

- Replaced wildcard CORS access with an approved origins list.
- Syntax check passed.
- Action: Confirm the production Vercel URL is configured in `ALLOWED_ORIGINS`.

## 6. Test Results

- 7 privacy and authentication tests passed.
- Non-video upload rejection passed.
- Full backend test suite still has signup-related failures.

**Reason for existing test failures:**
- Signup in `backend/routers/auth.py` expects a different request format than the tests provide.
- Signup returns 422, which also causes login tests to fail.
- This file is outside my assigned files and needs review by the auth developer.

## 7. Files Changed

- `backend/main.py`
- `backend/services/deps.py`
- `backend/tests/test_privacy.py`
- `docs/writeups/security.md`

## 8. Outstanding Issues

1. Fix signup request handling in `backend/routers/auth.py`.
2. Confirm email, password, and username validation.
3. Confirm whether session deletion is required.
4. Add or confirm leaderboard privacy protections.
5. Configure the production Vercel URL in `ALLOWED_ORIGINS`.