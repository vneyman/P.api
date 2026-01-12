# P.api

FastAPI-based access to databases (e.g., Postgres) and other data sources.

## Repository layout

- `fastapi-app/`: FastAPI service (code, tests, Docker, and scripts).

## Quick start

```bash
cd fastapi-app
uv venv
source .venv/bin/activate
uv pip install -e .
uv pip install -e ".[dev]"
cp .env.example .env
uvicorn app.main:app --reload
```

## Configuration

The app reads settings from `fastapi-app/.env` using Pydantic settings.

Supported variables:
- `APP_NAME`
- `DATABASE_URL` (optional; if unset, the `POSTGRES_*` values are used)
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `POSTGRES_DB`
