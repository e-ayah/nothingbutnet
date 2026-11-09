# Testing Guide

## 1. Backend Test Setup

The backend tests use a separate PostgreSQL database to avoid modifying the development database.

Create the test database:

```bash
createdb nothingbutnet_test
```

Make sure PostgreSQL is running and the database exists.

The backend test configuration automatically connects to `nothingbutnet_test`.

## 2. Running Backend Tests

From the project root, run:

```bash
python -m pytest backend/tests -v
```

This runs all backend authentication and session tests.

### Test Coverage

**`backend/tests/conftest.py`**
- Configures the separate test database.
- Creates clean database tables for each test.
- Provides a FastAPI test client and database session fixture.
- Provides an authenticated test user.

**`backend/tests/test_auth.py`**
- Successful signup.
- Duplicate email rejection.
- Successful login.
- Incorrect password rejection.
- Accessing `/auth/me` with a valid token.
- Rejecting requests without a token.

**`backend/tests/test_sessions.py`**
- New users have no sessions.
- Users cannot access another user's sessions.
- Sessions are returned newest first.

## 3. Running ML Tests

Run the ML end-to-end test:

```bash
python -m pytest ml/tests/test_pipeline_e2e.py -v
```

The test uses `ml/tests/data/pose_clip.mp4` by default.

To use another video clip, set the `NBN_TEST_CLIP` environment variable:

```bash
NBN_TEST_CLIP=/path/to/video.mp4 python -m pytest ml/tests/test_pipeline_e2e.py -v
```

### Test Coverage

**`ml/tests/test_pipeline_e2e.py`**
- Runs the complete analysis pipeline using `analyze()`.
- Checks that the result contains angles, feedback, and an overall score.
- Verifies that the score is between 0 and 100.
- Checks that an annotated video file is generated.

## 4. Running All Tests

Run backend and ML tests separately:

```bash
python -m pytest backend/tests
python -m pytest ml/tests/test_pipeline_e2e.py
```

Both test suites should pass consistently without depending on previous test runs.