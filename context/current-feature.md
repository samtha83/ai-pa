# Current Feature


## Status

Not Started

## Goals

<!-- Goals & requirements -->

## Notes

<!-- Any extra notes -->

## History

- In Progress: Provider Profile Model
  - Started on branch `feature-provider-profile-model`.
  - Confirmed the Phase 1 provider model and initial migration already exist; implementation will build on them rather than duplicate the table.
- Completed: Provider Profile Model
  - Added provider profile metadata through an additive Alembic migration and extended the existing SQLAlchemy model.
  - Added timezone-aware Pydantic validation, provider-ID-scoped repository/service access, and persistence tests.
  - Migrated the local SQLite database to `0002_provider_profile` and verified all 9 backend tests pass.
  - Left API routes and frontend screens to their dedicated Phase 2 features.
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
- Completed: Add Startup Docs
  - Added clean-checkout setup, environment, startup, migration, testing, and reset instructions.
  - Documented SQLite provider records and the current demo-auth limitation.
  - Verified migrations, provider lookup, backend tests, frontend build, and documentation formatting.
- Completed: Provider Preferences Model
  - Added provider-scoped preferences with defaults, validation, migration, and authenticated read/update routes.
  - Enforced offset-free local working-hour values; verified 7 focused and 15 total backend tests.
