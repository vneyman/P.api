# Repository Guidelines

# Project Documentation  
 - Always use Context7 MCP when I need library/API documentation, code generation, setup or configuration steps without me having to explicitly ask.  

## Project Structure & Module Organization
- `app/` contains the FastAPI application code. Entry point is `app/main.py`.
- `app/api/` holds versioned routes (e.g., `app/api/v1/`).
- `app/core/` contains settings and configuration helpers.
- `app/services/` encapsulates integrations like database access.
- `tests/` contains pytest tests (start with `test_`).
- `scripts/` includes developer scripts such as `test_postgres.py`.

## Build, Test, and Development Commands
- `uv venv` and `source .venv/bin/activate`: create/activate a local virtualenv.
- `uv pip install -e .` and `uv pip install -e ".[dev]"`: install runtime and dev deps.
- `uvicorn app.main:app --reload`: run the API locally with auto-reload.
- `pytest`: run the test suite (quiet mode via project config).
- `docker compose up --build`: run the app in Docker (requires `neyman-net` network).

## Coding Style & Naming Conventions
- Python 3.11+, 4-space indentation, and type hints where practical.
- Module and function names use `snake_case`; classes use `PascalCase`.
- Keep API route files small and delegate DB logic to `app/services/`.
- No enforced formatter/linter; keep code readable and consistent with existing files.

## Testing Guidelines
- Framework: pytest; tests live in `tests/`.
- Naming: files `test_*.py`, test functions `test_*`.
- Focus on API behavior (e.g., health checks) and database boundaries.

## Commit & Pull Request Guidelines
- No formal commit convention exists; use short, imperative messages (e.g., "Add events upsert").
- PRs should describe the change, list commands run (if any), and note DB/env updates.
- Include example requests or payloads when adding or modifying API endpoints.

## Security & Configuration Tips
- Copy `.env.example` to `.env` and set `DATABASE_URL` for local usage.
- The Events API writes to `misc.events.event`; ensure the `"name"` field is unique.
