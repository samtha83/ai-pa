# Current Feature: Provider Preferences Model


## Status

Completed

## Goals

- Persist provider-specific working hours, session duration, buffer time, blackout dates, daily capacity, and summary-template defaults.
- Validate preference values and schedule structure before persistence.
- Provide provider-scoped read/update operations and authenticated API access with defaults for first use.

## Notes

Implement only preferences and their API surface. Reuse the existing provider profile, database session, schemas/repository/service patterns, and session authentication; resolve provider scope from the authenticated session, never request-supplied IDs. Preserve unrelated worktree changes.

## History

- In Progress: Provider Preferences Model
  - Started on branch `feature-provider-preferences-model`.
  - Added a provider-owned one-to-one preference record with validation and authenticated read/update endpoints.
- Completed: Provider Preferences Model
  - Added a one-to-one provider preferences model and Alembic migration `0003_provider_preferences`.
  - Added validated schedule, session, blackout-date, daily-capacity, and summary-template settings with first-read defaults.
  - Added provider-scoped repository/service operations and authenticated `GET`/`PUT /api/v1/providers/me/preferences` routes.
  - Required offset-free local working-hour times and documented provider-time display behavior for future chat and appointment messages.
  - Verified the focused preferences and migration tests (7 passed), full backend suite (15 passed), and `git diff --check`.
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
