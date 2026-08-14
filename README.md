 # FastAPI App

A production-grade FastAPI project scaffold — ready for AI integrations, database layers, authentication, and more.

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # Application factory (create_app)
│   ├── server.py            # ASGI entrypoint for uvicorn
│   ├── config.py            # Pydantic Settings (env-based config)
│   ├── api/
│   │   └── v1/
│   │       ├── router.py    # Aggregates all v1 routers
│   │       └── endpoints/
│   │           ├── health.py # Health check endpoint
│   │           └── items.py  # Sample CRUD endpoints
│   ├── core/
│   │   ├── exceptions.py    # Custom exceptions & handlers
│   │   └── dependencies.py  # FastAPI dependency injection
│   ├── schemas/
│   │   └── items.py         # Pydantic request/response schemas
│   ├── models/              # Database/ORM models (add later)
│   └── services/            # Business logic layer (add later)
├── tests/
│   ├── conftest.py          # Shared test fixtures
│   ├── test_health.py
│   └── test_items.py
├── pyproject.toml           # Project config, deps, and tooling
├── Dockerfile
├── .env.example
└── .gitignore
```

## Quick Start

### 1. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
```

### 2. Install dependencies

```bash
pip install -e ".[dev]"
```

### 3. Run the server

```bash
uvicorn app.server:app --reload
```

The API will be available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

### 4. Run tests

```bash
pytest
```

### 5. Lint & type check

```bash
ruff check .
mypy app/
```

## Docker

```bash
docker build -t fastapi-app .
docker run -p 8000:8000 --env-file .env fastapi-app
```

## Adding New Features

1. **New endpoint domain** (e.g., `users`):
   - Create schema in `app/schemas/users.py`
   - Create endpoint in `app/api/v1/endpoints/users.py`
   - Register in `app/api/v1/router.py`
   - Add service in `app/services/users.py` (business logic)
   - Add model in `app/models/users.py` (when DB is added)

2. **Database integration**: Add SQLAlchemy/Tortoise ORM with migrations (Alembic)

3. **Authentication**: Add JWT auth with `python-jose` and OAuth2 password flow

4. **AI integration**: Add AI service clients in `app/services/` and wire them into endpoints

## Design Principles

- **Application Factory** — `create_app()` enables clean testing and multiple configs
- **Versioned API** — `/api/v1/` prefix for backward compatibility
- **Pydantic v2** — Strict validation with `from_attributes` for ORM support
- **Dependency Injection** — Use `Annotated[T, Depends(...)]` for clean DI
- **Custom Exceptions** — Consistent error responses across the entire API
- **Lifespan Handler** — Modern resource management (replaces deprecated `on_event`)
- **Environment Config** — `pydantic-settings` for type-safe env var loading
