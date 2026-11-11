# Run NothingButNet locally

Audited November 10, 2026 against `develop` commit `55b077f`. Run commands from the repository root unless a section explicitly changes directories. This guide separates successful setup from known application defects; the [verification record](#verification-and-teammate-walkthrough) is not a teammate sign-off.

## Prerequisites

- Git; access to this repository.
- Python **3.11** (`python3.11 --version`). Newer Python is not the supported MediaPipe environment.
- PostgreSQL **16**, including `psql`, `createdb`, and a running local server.
- Node.js **20+** and npm (`node --version`, `npm --version`). Use an actively supported Node version with Expo SDK 58.
- For iPhone: compatible Expo Go or an SDK 58 development build; phone and computer on the same Wi-Fi. Web testing needs only a browser.
- Cloudinary credentials from a PM for actual upload/analysis; no credentials are needed for standalone ML or the existing automated tests.

On macOS with Homebrew, if these tools are missing:

```bash
brew install python@3.11 postgresql@16 node
brew services start postgresql@16
export PATH="$(brew --prefix postgresql@16)/bin:$PATH"
```

The PATH command applies to the current terminal. Add it to your shell profile if needed. Windows/Linux contributors should install the same major versions using their supported installers/package manager and start PostgreSQL before proceeding.

## Checkout and Python environment

```bash
git clone https://github.com/e-ayah/nothingbutnet.git
cd nothingbutnet
git checkout develop
git pull origin develop
python3.11 -m venv venv
source venv/bin/activate
python --version
python -m pip install -r backend/requirements.txt
```

On Windows, create the environment with `py -3.11 -m venv venv` and activate with `venv\Scripts\activate.bat` in Command Prompt, or `venv\Scripts\Activate.ps1` in PowerShell. Activate the environment again in each terminal that runs Python commands.

The backend requirements include ML and test packages. MediaPipe also installs GUI OpenCV transitively; normalize to **one** headless OpenCV distribution, matching Render and CI:

```bash
python -m pip uninstall -y opencv-python opencv-contrib-python
python -m pip install --no-deps --force-reinstall opencv-contrib-python-headless==4.10.0.84
python -c "import mediapipe as mp, cv2, numpy; print(mp.__version__, cv2.__version__, numpy.__version__)"
```

Expected versions: `0.10.21`, `4.10.0`, `1.26.4`. Headless OpenCV supports the pipeline's video/image operations without desktop display libraries. A dependency checker may still report MediaPipe's declared GUI OpenCV requirement; don't install multiple `cv2` distributions to satisfy it.

## Backend and database

### Create a local database and environment file

```bash
createdb nothingbutnet
createdb nothingbutnet_test
cp backend/.env.example backend/.env
python -c "import secrets; print(secrets.token_hex(32))"
```

If a database already exists, reuse only your own local development/test database. Never run the tests against a shared database; they drop tables. In Windows, use `copy backend\.env.example backend\.env` instead of `cp`.

Edit **backend/.env** locally:

```dotenv
DATABASE_URL=postgresql://localhost/nothingbutnet
SECRET_KEY=<paste-your-new-random-value>
CLOUDINARY_CLOUD_NAME=<from-PM>
CLOUDINARY_API_KEY=<from-PM>
CLOUDINARY_API_SECRET=<from-PM>
```

Replace placeholders; don't paste real values into a PR, screenshot, or chat. For PostgreSQL installations requiring password authentication, use `postgresql://YOUR_USER:YOUR_PASSWORD@localhost:5432/nothingbutnet` and URL-encode special characters. Cloudinary values may stay blank while checking health/auth/ML, but actual video uploads will fail until configured.

### Create tables and run the API

```bash
cd backend
alembic upgrade head
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Expected: both migrations complete and Uvicorn listens on port 8000. Keep this terminal open. Binding to `0.0.0.0` allows a phone on your local network to reach the API; use trusted Wi-Fi.

- [Health](http://localhost:8000/health): expect `{"status":"ok","db":true}`. `db:false` is a database problem even if HTTP is 200.
- [ML health](http://localhost:8000/health/ml): expect `ok:true` with library versions, runtime and peak memory. The first initialization may be slower.
- [Swagger UI](http://localhost:8000/docs) / [OpenAPI JSON](http://localhost:8000/openapi.json): source-generated route/schema definitions.

### Verify auth in Swagger

The current signup endpoint requires this **nested** JSON body (see the [contract](api-contract.md#authentication)):

```json
{
  "body": { "email": "new-player@example.com", "password": "local-demo-password", "name": "New Player" },
  "username": "new_player"
}
```

Use your own disposable test identity. `POST /auth/signup` should return 200 with `user_id` and `token`; the optional username must be 3–20 letters/numbers/underscores. Login uses a flat `{ "email": "…", "password": "…" }` body. Click **Authorize** in Swagger and paste the returned token into its HTTPBearer value field; call `GET /auth/me` and `GET /sessions` (initially `[]`).

**Known blocker:** the app and existing signup tests send flat signup data and get 422. Do not change the docs' nested example to make it match the broken client; the endpoint/client owners must agree on and fix one shape. The docs/CI ticket does not change application files.

## ML setup and tests

If you completed backend installation, the core ML dependencies are already installed. For **ML only**, use a separate Python 3.11 environment and:

```bash
python -m pip install -r ml/requirements.txt pandas
python -m pip install numpy==1.26.4
python -m pip uninstall -y opencv-python opencv-contrib-python
python -m pip install --no-deps --force-reinstall opencv-contrib-python-headless==4.10.0.84
```

From the repository root:

```bash
python -m pytest ml/tests -q
python -m ml.analysis_pipeline ml/tests/data/pose_clip.mp4
```

The suite includes bundled `tiny.mp4` and `pose_clip.mp4`; it should not need the team Drive set. The CLI prints JSON, runtime and the annotated temporary MP4 path. A clip without a detectable release can return null angles/score and no annotated video. The larger ten-clip evaluation set is linked in [testing/test-videos.md](../testing/test-videos.md); download authorized clips to a folder outside the repo, such as `~/clips`.

```bash
python -m ml.tools.eval_release /absolute/path/to/clips data/release_frames.csv
```

Do not commit original/generated player recordings. This pipeline measures form; a high score is not proof of a made shot or a validated prediction.

## Frontend: web and iPhone

In a second terminal:

```bash
cd frontend
npm ci
cp .env.example .env.local
```

Edit `.env.local`:

```dotenv
EXPO_PUBLIC_API_URL=http://localhost:8000
```

For a **physical phone**, replace `localhost` with your computer's LAN address, for example `http://192.168.1.50:8000`. A phone's localhost is the phone itself. The API must still be running, your firewall must allow the local connection, and both devices must share Wi-Fi.

```bash
npm start
```

Press **w** for web. For iPhone, scan the terminal QR code and open in compatible Expo Go. The API URL and Expo/Metro URL are different: don't use the Metro port as the API port. Restart Expo after `.env.local` changes. Never put Cloudinary secrets, database passwords or JWT signing keys in an `EXPO_PUBLIC_` variable; those are bundled into the app.

The app should show onboarding only on first launch, then Login, or Home if a saved login exists. Blank saved-login storage can be reset through your browser's site data or the app's local storage. To test signup before its integration fix lands, use Swagger's nested signup first, then log in through the app.

### What connects to real data?

| Client setting/path | Current state |
|---|---|
| `services/config.ts`: auth/upload/sessions/analysis | Real API (`false`) |
| `MOCKS.progress` | Mock progress/goals (`true`) |
| `compareApi.ts`, `madeApi.ts`, `leaderboardApi.ts` | Each has its own `USE_MOCK = true` |
| `insightsApi.ts` | Tests the `MOCKS` object itself, so always returns mocks |
| Friends/Leaderboard buttons | Routes not yet registered in `App.tsx` on audited develop |

Don't assume that setting the API URL makes every screen live. Finals #01/#02 and the feature owners handle those integrations. Follow your own ticket's ownership rules before changing mock settings/navigation.

### Optional build checks

```bash
# From frontend/:
npx tsc --noEmit
npx expo export --platform web --output-dir /tmp/nbn-web
```

Choose a writable output directory appropriate to your OS. The web deployment is documented in [deploy-web.md](deploy-web.md); a successful export alone does not validate every runtime endpoint.

## Backend tests and CI

From the repository root with the Python environment active:

```bash
export TEST_DATABASE_URL=postgresql://localhost/nothingbutnet_test
export SECRET_KEY=local-test-only
python -m pytest backend/tests -q
```

Use the same PostgreSQL user/password/port as your local server, but the database name **must** be `nothingbutnet_test`. In PowerShell, use `$env:TEST_DATABASE_URL = "…"` and `$env:SECRET_KEY = "local-test-only"`. Environment variables override `.env` values in this terminal. The fixture sets `DATABASE_URL` to the test URL, refuses a different database name and recreates tables for fixture-based tests; several tests use the real test database directly. Don't run suites in parallel against the same database.

[tests.yml](../.github/workflows/tests.yml) runs the full ML and API suites on every PR, on pushes to `develop`, and by manual dispatch. Jobs use Python 3.11; the backend gets a disposable PostgreSQL 16 service. CI uses only a throwaway JWT value and no production Cloudinary/database credentials. Each job uploads a JUnit report even after test failure. Neither job suppresses failures or skips known-broken tests. Passing API tests currently does not prove Cloudinary upload, live-server performance, or genuine shot accuracy.

## Troubleshooting

| Symptom | Check |
|---|---|
| Python/MediaPipe install fails | Use Python 3.11 and the pinned MediaPipe version; recreate a stale environment rather than upgrading MediaPipe. |
| `createdb`/`psql` not found | PostgreSQL 16 `bin` must be on PATH. On macOS use the Homebrew PATH command above. |
| PostgreSQL role missing | Use the account created by your PostgreSQL installer in `DATABASE_URL`; Homebrew normally uses your macOS username. |
| `/health` says `db:false` | PostgreSQL running, database created, correct URL, migrations applied; restart the API after editing `.env`. |
| Signup 422 mentions `body` | Existing signup-shape regression; use the nested Swagger example, then log in. |
| Cloudinary upload 502 | All three local Cloudinary variables must be valid; ask a PM privately. |
| iPhone cannot connect | Use the computer's LAN IP, bind Uvicorn to `0.0.0.0`, check Wi-Fi/firewall. `npx expo start --tunnel` can help Metro but does not expose a localhost API. |
| Expo reports incompatible SDK | Install a matching SDK 58 Expo Go build or use a development build; coordinate dependency upgrades with the team. |
| OpenCV complains about `libGL`/`cv2` | Normalize to the single headless distribution above; don't add another OpenCV package. |
| MediaPipe `NSOpenGLPixelFormat` on macOS | Run in a normal local terminal with graphics access; the sandboxed run failed while the normal run passed. Ubuntu CI uses the headless runtime. |
| Friends/Leaderboard navigation or comparison fails | See the known integration/runtime gaps in the [API contract](api-contract.md#known-gaps-and-deployment-parity). |
| API test job fails on signup | Read the assertion/422 detail. Don't weaken CI to conceal the frontend/server/test mismatch. |

## Verification and teammate walkthrough

The implementer verified installation into a new temporary Python 3.11 environment, PostgreSQL 16 startup, both Alembic migrations on an empty local database, and local OpenAPI generation on November 10, 2026. Local full-suite results: **ML 56 passed**; **API 35 passed, 3 failed, 4 errors**. The seven API failures/errors trace to flat signup requests versus the nested endpoint. Hosted Actions results must be checked on the PR; local results are not a hosted-green claim. The live API schema request timed out after 60 seconds, so deployment parity remains unverified.

**Required independent walkthrough — pending.** A teammate who has never configured all three parts must follow this guide on their own laptop. The implementer's isolated install does not satisfy that requirement. Give the reviewer this checklist and have them report the failing command, OS/version, expected vs actual output, and a redacted error for each obstacle:

- [ ] Reviewer name/date and OS: pending.
- [ ] Fresh checkout, Python 3.11 environment and dependency import check.
- [ ] Local database, `.env`, migrations and `/health` with `db:true`.
- [ ] Swagger signup/login and authorized `/auth/me`.
- [ ] Full ML suite and a local analysis command.
- [ ] Full API suite; distinguish the documented signup failure from environment problems.
- [ ] Web login/upload/results with real credentials; phone API URL and Expo startup.
- [ ] All obstacles documented and guide corrections re-tested; PM confirms final sign-off.

Ask a teammate to do this walkthrough before marking Finals #08 complete. No teammate has been contacted or signed off by this document.
