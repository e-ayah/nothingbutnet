# NothingButNet Backend

## Prerequisites

* Python 3.11
* PostgreSQL
* Git

## Setup

From the project root:

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

Create the PostgreSQL database:

```bash
createdb nothingbutnet
```

Create your local environment file:

```bash
cp backend/.env.example backend/.env
```

Do not commit the `.env` file.

## Database

Once the Alembic migrations from ticket 1-05 are available, run:

```bash
cd backend
alembic upgrade head
```

## Start the Server

From the project root:

```bash
cd backend
uvicorn main:app --reload
```

The API will be available at:

http://127.0.0.1:8000

Interactive API documentation:

http://127.0.0.1:8000/docs

Health check:

http://127.0.0.1:8000/health/

A healthy database connection should return:

```json
{
  "status": "ok",
  "db": true
}
```

## Run Tests

From the project root:

```bash
python -m pytest
```

## Troubleshooting

### `python3.11: command not found`

Make sure Python 3.11 is installed and available on your PATH.

### `ModuleNotFoundError`

Make sure the virtual environment is activated:

```bash
source venv/bin/activate
```

Then reinstall dependencies:

```bash
pip install -r backend/requirements.txt
```

If you are starting Uvicorn manually, run it from the `backend` directory:

```bash
cd backend
uvicorn main:app --reload
```

### `createdb: command not found`

Make sure PostgreSQL is installed and its command-line tools are available.

With Homebrew on macOS:

```bash
brew install postgresql
brew services start postgresql
```

Then try:

```bash
createdb nothingbutnet
```

### Database connection errors

Make sure PostgreSQL is running and that `backend/.env` contains:

```text
DATABASE_URL=postgresql://localhost/nothingbutnet
```

### `.env` is missing

Create it from the example:

```bash
cp backend/.env.example backend/.env
```

Never commit `.env` to Git.

### Alembic errors

The database migrations are provided by ticket 1-05. Once those migrations are available, run:

```bash
cd backend
alembic upgrade head
```
