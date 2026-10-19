# Current Feature: API Routes


## Status

Completed

## Goals

- Provide authenticated versioned API routes for provider profile, provider preferences, and client records.
- Derive every provider data scope from the validated session, never from request-controlled provider IDs.
- Validate payloads and return explicit errors for invalid, unauthenticated, missing, and cross-provider requests.

## Notes

- Scope: API boundary only; do not expand into admin, scheduling, chat, or summary APIs.
- Existing repository-scoped services, Pydantic schemas, and demo-auth dependency are prerequisites; reuse them.
- Verify profile/preferences/client reads and writes, invalid payloads, unauthenticated requests, and cross-provider denial.
- Source: `context/features/phase2-feature5-api-routes.md`.

## History

- Completed: Client Model
  - Started from `context/features/phase2-feature3-client-model.md`.
  - Added provider-owned client persistence, an Alembic migration, payload schemas, provider-scoped repository/service methods, and authenticated list/create/detail/update routes.
  - Verified migration and persistence behavior, invalid payload rejection (including explicit null status on update), and cross-provider denial; full backend suite passes with 27 tests.
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
- Completed: Client Model
  - Added provider-scoped client persistence, validation, migration, and authenticated CRUD endpoints; verified with 27 passing backend tests.
- Completed: UI Screens
  - Added provider settings and provider-scoped client create, list, detail, and edit screens with explicit loading, error, and empty states.
  - Added authenticated provider profile read/update endpoints and fixed app-shell session hydration and profile-name refresh behavior.
  - Verified the frontend production build, all 29 backend tests, and local browser flows for settings and client persistence after refresh.
- Completed: UI Screens
  - Merged provider settings and provider-scoped client list, create, detail, and edit screens into `main`.
  - Added authenticated provider profile endpoints and verified the production build, 29 backend tests, and browser persistence flows.
- Completed: API Routes
  - Verified authenticated, provider-scoped profile, preferences, and client endpoints were already registered and wired to their scoped services.
  - Added regression tests for unauthenticated profile/client requests, rejection or ignoring of request-supplied provider IDs, and denial of cross-provider client updates.
  - Verified all 31 backend tests pass.
