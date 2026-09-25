# Current Feature: Add Demo Auth

<!-- Feature Name -->

## Status

<!-- Not Started|In Progress|Completed -->

Completed

## Goals

<!-- Goals & requirements -->

- Seed a single local demo provider with idempotent startup initialization.
- Implement login, logout, and current-user auth flows using server-side session validation.
- Protect backend routes using provider identity resolved from the session.
- Connect frontend session state to login/logout and protected-route redirects.
- Keep the demo flow clearly marked as local-development-only and replaceable later.

## Notes

<!-- Any extra notes -->

- This feature depends on the SQLite foundation and provider/session tables created in the previous feature.
- Use a server-validated HTTP-only session or equivalent cookie-based transport; never trust browser-supplied provider IDs.
- Keep session data minimal: store only opaque identifiers or hashes, not plaintext credentials or raw session content.
- The implementation should proceed in the order in the feature file: seed provider, auth service, auth API routes, protected-route dependency, frontend session behavior.
- Validate each step before continuing to the next.

## Verification

- Review verdict: Ready to complete.
- Backend auth tests: 7 passed.
- Frontend production build: passed.

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
