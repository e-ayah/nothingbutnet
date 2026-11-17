# NothingButNet API

FastAPI routes for authentication, video upload/analysis, sessions, progress, friends and comparison. PostgreSQL stores application records; Cloudinary stores video assets; ML runs in the API process as a background task.

Follow [the setup guide](../docs/setup.md#backend-and-database) for Python 3.11, PostgreSQL 16, environment variables and Alembic migrations. For the actual request/response shapes and current integration gaps, read the [API contract](../docs/api-contract.md).

```bash
# From the repository root, after setup:
source venv/bin/activate
cd backend
alembic upgrade head
uvicorn main:app --reload --host 0.0.0.0
```

Open [local Swagger docs](http://localhost:8000/docs). `/health` reports database reachability in `db`; HTTP 200 by itself does not prove the database works. `/health/ml` initializes MediaPipe and reports dependency versions and peak memory.

```bash
# From the repository root; uses a disposable, correctly named test database:
TEST_DATABASE_URL=postgresql://localhost/nothingbutnet_test \
  SECRET_KEY=local-test-only python -m pytest backend/tests -q
```

Tests drop/recreate tables in the test database. No Cloudinary keys are needed for the current API tests. Real upload/analysis needs all three Cloudinary variables. See [testing](../docs/testing.md), [architecture](../docs/architecture.md), and [Render deployment](../docs/deploy.md).
