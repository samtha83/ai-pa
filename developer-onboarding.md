# Developer Onboarding

This guide describes the local development workflow for the AI Personal Assistant MVP foundation. It is intended for a clean checkout and uses local-only services and data.

## Prerequisites

Install the following before starting:

- Git.
- Node.js 20.9 or newer, with npm.
- Python 3.11 or newer.
- SQLite support through Python's standard-library `sqlite3` module.

No external service account or credential is required for the local foundation.

## Initial Setup

From the repository root:

```bash
cp .env.example .env
```

The example file contains safe local placeholders. Review `.env` and keep these values aligned with the local services:

- `APP_ENV=development` selects local behavior.
- `NEXT_PUBLIC_API_URL=http://localhost:8000` is the browser-facing backend URL.
- `BACKEND_API_URL=http://localhost:8000` is the server-side frontend backend URL.
- `DATABASE_URL=sqlite:///./data/local.db` stores the local database in `data/local.db` relative to the repository root.
- `SESSION_SECRET` is a local development placeholder. Replace it with a private local value and never commit `.env`.

## Backend

Create and activate a virtual environment, then install the backend and development dependencies:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
cd ..
```

Apply the database migrations after exporting the root environment values:

```bash
set -a
source .env
set +a
cd backend
PYTHONPATH=. python -m alembic upgrade head
cd ..
```

### Validate migrations

The migration command should finish without an error and create `data/local.db`.
From the repository root, verify the applied revision and the expected tables:

```bash
set -a
source .env
set +a
cd backend
PYTHONPATH=. .venv/bin/python -m alembic current
PYTHONPATH=. .venv/bin/python - <<'PY'
import sqlite3

connection = sqlite3.connect("../data/local.db")
tables = connection.execute(
	"SELECT name FROM sqlite_master "
	"WHERE type = 'table' ORDER BY name"
).fetchall()
revision = connection.execute(
	"SELECT version_num FROM alembic_version"
).fetchone()
print("tables:", [name for (name,) in tables])
print("alembic revision:", revision[0] if revision else None)
connection.close()
PY
cd ..
```

The database should contain `providers`, `demo_sessions`, and `alembic_version`.
To see the SQL changes that would be applied before running them, use:

```bash
cd backend
PYTHONPATH=. .venv/bin/python -m alembic upgrade head --sql
cd ..
```

### Provider and user records

The current MVP does not have a `users` table. A provider is the current local
identity model, with these fields:

- `id`: stable string primary key.
- `name`: required display name.
- `business_name`: optional organization name.
- `timezone`: required timezone, defaulting to `UTC`.

Starting the backend calls `ensure_demo_provider()` and idempotently creates this
development record if it does not exist:

```text
id=demo-provider
name=Demo Provider
business_name=Local development provider
timezone=UTC
```

Confirm the seeded provider with:

```bash
backend/.venv/bin/python - <<'PY'
import sqlite3

connection = sqlite3.connect("data/local.db")
for provider in connection.execute(
		"SELECT id, name, business_name, timezone FROM providers"
):
		print(provider)
connection.close()
PY
```

For local database experiments, add another provider through SQLAlchemy rather
than writing to migration files. Run this from the repository root after the
migrations have been applied:

```bash
set -a
source .env
set +a
PYTHONPATH=backend backend/.venv/bin/python - <<'PY'
from app.db.session import get_session_factory
from app.models import Provider

provider = Provider(
		id="provider-local-001",
		name="Local Provider",
		business_name="Local Practice",
		timezone="UTC",
)

with get_session_factory()() as session:
		session.add(provider)
		session.commit()
PY
```

Use a unique provider ID. The insert is for database development only: demo
authentication currently seeds and resolves `demo-provider`, and there is no
production user-management or provider-registration flow yet. Do not add real
people, credentials, tokens, or regulated data to the local SQLite database.
```

Start the API in a separate terminal from the repository root:

```bash
PYTHONPATH=backend python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The backend is available at `http://localhost:8000`. FastAPI's interactive documentation is at `http://localhost:8000/docs`, and the health endpoint is at `http://localhost:8000/api/v1/health`.

## Frontend

In another terminal, from the repository root:

```bash
cd frontend
npm ci
npm run dev
```

The frontend is available at `http://localhost:3000`. The frontend uses the backend URL from `NEXT_PUBLIC_API_URL` for browser requests and `BACKEND_API_URL` for server-side requests.

## Verification

Run backend tests from the repository root after activating the backend virtual environment:

```bash
cd backend
pytest
cd ..
```

Build the frontend for production validation:

```bash
cd frontend
npm run build
cd ..
```

The frontend currently provides `npm run lint`, but the Next.js 16 migration means lint configuration should be confirmed before treating it as a required quality gate. A dedicated frontend test command is `TBD`.

## Local Reset

To reset local runtime state while preserving source files:

```bash
rm -f data/local.db
rm -rf backend/.pytest_cache frontend/.next
set -a
source .env
set +a
cd backend
PYTHONPATH=. python -m alembic upgrade head
cd ..
```

Do not remove the `backend/`, `frontend/`, or `context/` directories. The migration command recreates the schema in the local SQLite database. Test fixtures use isolated databases and do not require deleting the development database.

## MVP Limitations

- Demo authentication is for local development only. It uses seeded demo identities and server-side sessions; it is not production authentication.
- SQLite is the local development database, not a production deployment recommendation.
- The local MVP is not configured for regulated healthcare data, production operations, or external service credentials.
- Real Azure OpenAI, MCP, calendar, messaging, and other integrations are out of scope for this local foundation.
- Keep secrets, tokens, and sensitive data out of source files, logs, screenshots, and test fixtures.
