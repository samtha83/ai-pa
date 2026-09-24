# Feature: Add SQLite Layer

- **Phase:** Phase 1: Local Runtime Foundation
- **Feature ID:** phase1-feature4
- **Status:** Not Started
- **Source plan:** docs/mvp-build-plan.md

## Goal

Add a local SQLite database with migrations, provider/session foundation tables, and readiness checks that later MVP features can extend safely.

## Non-Goals

- Implementing all final product entities.
- Storing raw session content or uploaded files in database rows.
- Building production database infrastructure or PostgreSQL deployment.

## Why This Matters

Every workflow needs durable provider-scoped state. A migration-backed SQLite boundary makes the local demo repeatable and gives the later application a clear path to PostgreSQL.

## Prerequisites

- Backend application exists from `phase1-feature3-initialize-backend`.
- Local runtime directory and SQLite path are defined by `phase1-feature1-repo-structure`.
- The repository must select one migration approach before implementation, preferably SQLAlchemy with Alembic unless an existing standard says otherwise.

## Technical Solution

Use SQLAlchemy models and Alembic migrations, unless the repository has already standardized on an equivalent migration tool. Store the SQLite file under the ignored local data directory. Add provider and demo-session tables with UTC timestamps, foreign keys, indexes, and session revocation fields. Expose a readiness check that verifies a database connection without modifying application data.

Keep raw notes, transcript files, and generated artifacts outside SQLite behind a future file-storage boundary. Repositories must accept provider identity from the authenticated backend context rather than from arbitrary browser input.

## Implementation Steps

### Step 1: Configure the database connection

- **What to do:** Add typed SQLite configuration and a database session factory.
- **Where:** Proposed locations `backend/app/db/` and `backend/app/core/config.py`.
- **How:** Build the database URL from environment configuration and keep local data outside source files.
- **Done when:** The backend can open and close a SQLite connection during startup/readiness checks.

### Step 2: Add migration tooling

- **What to do:** Initialize versioned migrations.
- **Where:** Proposed location `backend/migrations/`.
- **How:** Ensure first startup or an explicit documented command applies migrations without manual SQL editing.
- **Done when:** A clean local data directory produces the expected schema.

### Step 3: Add provider foundation tables

- **What to do:** Create the provider and demo session models.
- **Where:** Proposed locations `backend/app/models/` and migration files.
- **How:** Include provider ID, name, business name, timezone, timestamps, session ID, provider ID, expiry, created-at, and revoked-at. Store only an opaque session identifier or hash, never plaintext credentials.
- **Done when:** Migrations create the tables with foreign keys and lookup indexes.

### Step 4: Add database readiness

- **What to do:** Add a readiness check that reports SQLite availability.
- **Where:** Backend health/readiness route module.
- **How:** Return HTTP 200 when SQLite is reachable and a dependency failure response when it is unavailable.
- **Done when:** Readiness can distinguish process health from database readiness.

### Step 5: Add isolated test database setup

- **What to do:** Create test fixtures that do not modify developer data.
- **Where:** Proposed location `backend/tests/fixtures/`.
- **How:** Use a temporary database or test-specific path and verify migrations run against it.
- **Done when:** Database tests are repeatable and leave the developer database unchanged.

## Interface and Data Contracts

- SQLite path is configurable and defaults to ignored local runtime data.
- `providers` table owns provider identity and timestamps.
- `demo_sessions` references a provider and stores expiry/revocation state.
- Readiness route reports database connectivity separately from process health.
- Raw session content and credentials are not stored in logs or this foundation schema.

## Verification

1. **Command:** Run the repository's migration command; mark it `TBD` until the backend package defines it.
2. Start with a clean temporary data directory and confirm migrations create the schema.
3. Stop or point away from the database and confirm readiness reports failure without exposing secrets.

## Acceptance Criteria

- [ ] SQLite path is configurable and stored outside source files.
- [ ] Versioned migrations apply on a clean local database.
- [ ] Provider and demo-session tables exist with foreign keys and timestamps.
- [ ] Readiness verifies SQLite connectivity.
- [ ] Test database fixtures do not modify developer data.
- [ ] Raw client/session content and credentials are not written to ordinary logs.

## Out of Scope

- Full client, summary, task, appointment, or audit schemas.
- File upload storage.
- PostgreSQL deployment.
- Authentication endpoints that consume the session tables.

## Notes

The selected migration tool and checkpointer table strategy must remain compatible with later LangGraph checkpoint storage. Keep application tables and checkpoint tables clearly separated.
