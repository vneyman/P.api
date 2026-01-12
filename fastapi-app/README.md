# FastAPI App

Scaffolded FastAPI application with Docker support and a simple Events API.

## Prerequisites

- Docker (recommended; container-first workflow).
- Postgres reachable via `DATABASE_URL` or the `.env` defaults.
- Python 3.11+ with `uv` installed (only if running locally).

## Docker (recommended)

```bash
cp .env.example .env
docker network create neyman-net
docker compose up --build
```

Health check: `GET http://localhost:3020/api/v1/health`

Notes:
- `docker-compose.yml` runs in dev mode (`--reload`) and bind-mounts `./app` into the container.
- The compose file expects an external `neyman-net` network to exist.
- Postgres is not provided by compose; set `DATABASE_URL` (or POSTGRES_* vars) in `.env`.

## Local development (uv)

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
uv pip install -e ".[dev]"
cp .env.example .env
uvicorn app.main:app --reload
```

Health check: `GET http://localhost:8000/api/v1/health`

## Testing

```bash
pytest
```

Optional DB sanity check (prints rows from `events.event`):

```bash
python scripts/test_postgres.py
```

## Events API

- `GET /api/v1/events?id=123` or `GET /api/v1/events?name=some-name`
- `POST /api/v1/events`

Example payload:

```json
{
  "name": "example",
  "description": "Example event"
}
```

The API reads/writes `events.event` via `DATABASE_URL` (see `.env.example`).
The upsert assumes `"name"` is unique (or has a unique constraint).

## Settings & DB dependencies

The database must contain the `events` schema and `event` table. Minimal DDL:

```sql
CREATE SCHEMA IF NOT EXISTS events;
CREATE TABLE IF NOT EXISTS events.event (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  description TEXT NOT NULL,
  date_insert TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  date_update TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

Settings are provided via a cached dependency (see `app/core/config.py`) and
database connections are injected per request using FastAPI's `Depends`
mechanism (see `app/services/db.py` and `app/api/v1/events.py`).

The events endpoints are `async` and use psycopg's async connection/cursor.
