# Current Feature: Add Startup Docs

<!-- Feature Name -->

## Status

<!-- Not Started|In Progress|Completed -->

Completed

## Goals

- Document clean-checkout prerequisites and local environment setup.
- Document frontend and backend installation, startup, ports, API docs, tests, migrations, and reset commands.
- Clearly state the local-only, non-production limitations of demo authentication and SQLite data.

## Notes

Implement the documentation in a root developer guide. Keep commands aligned with
the current frontend package scripts, backend pyproject, Alembic configuration,
and `.env.example`. Do not add credentials or document production deployment.

## History

- Completed: Create Repo Structure
  - Added dedicated `frontend/`, `backend/`, and `data/` runtime directories.
  - Added a tracked `.env.example` template for safe local configuration.
  - Updated `.gitignore` to protect secrets, SQLite files, generated output, and local caches.
  - Kept documentation in `docs/` for later feature work.
- Completed: Initialize Frontend Stack
  - Created the Next.js App Router frontend in `frontend/`.
  - Enabled TypeScript, Tailwind CSS, and the local app shell.
  - Added placeholder routes for login, dashboard, clients, calendar, and settings.
  - Added loading, error, and not-found states plus a typed API client boundary.
  - Verified the app compiles successfully with `npm run build`.
- Completed: Initialize Backend Stack
  - Added the FastAPI app package with typed settings and application wiring.
  - Created the versioned `/api/v1` route structure and health endpoint.
  - Added correlation IDs, local CORS middleware, and structured JSON error responses.
  - Verified behavior with pytest: 2 backend API tests passed.
- Completed: Add SQLite Layer
  - Added configurable SQLAlchemy sessions and Alembic migrations for local SQLite.
  - Added provider and demo-session foundation tables with timestamps, foreign keys, indexes, and revocation state.
  - Added database readiness reporting and isolated migration tests.
  - Verified the backend suite with 5 passing tests.
- Completed: Add Demo Auth
  - Added idempotent demo-provider seeding and server-validated cookie sessions.
  - Added login, logout, current-user, and protected backend auth routes.
  - Connected frontend login, logout, session state, and protected-route redirects.
  - Verified the backend suite with 7 passing tests and the frontend production build.
