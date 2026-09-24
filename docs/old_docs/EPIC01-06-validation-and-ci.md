# Feature: Validation and CI

- **EPIC:** EPIC-01
- **Feature ID:** 06
- **Status:** Not Started
- **Source spec:** context/features/phase1-spec.md

## Goal

Create focused automated checks and a CI workflow that prove the foundation boots, the database is reachable, authentication works, and the frontend shell remains navigable.

## Why This Matters

The app shell and service boundaries will be used by every later epic. Automated smoke checks catch broken startup or auth contracts before feature work builds on them.

## Prerequisites

- Features 01 through 05 are implemented or have stable test seams.
- The repository has a supported CI platform and package manager commands.
- Test dependencies are installed for the frontend and backend.

## Implementation Steps

### Step 1: Add backend test configuration

- **What to do:** Configure the backend test runner and isolated environment.
- **Where:** `backend/tests/`, `pyproject.toml`, and `backend/tests/conftest.py`.
- **How:** Create temporary database fixtures, configure a FastAPI test client, and prevent tests from using the developer SQLite file.
- **Done when:** A test can create an app client against an empty temporary database.

### Step 2: Test health and readiness

- **What to do:** Verify process and dependency checks.
- **Where:** `backend/tests/test_health.py`.
- **How:** Test HTTP 200 for health, HTTP 200 for readiness with a working SQLite database, and HTTP 503 for an unavailable readiness dependency.
- **Done when:** The tests prove the distinction between process health and dependency readiness.

### Step 3: Test database initialization

- **What to do:** Verify migration and model setup.
- **Where:** `backend/tests/test_database.py`.
- **How:** Start with a temporary empty database, apply migrations, check provider/session tables, and verify foreign-key behavior and timestamps.
- **Done when:** Tests pass without modifying the developer database.

### Step 4: Test authentication and authorization

- **What to do:** Test the complete local session flow.
- **Where:** `backend/tests/test_auth.py` and protected-route tests.
- **How:** Test login, current-user lookup, logout, missing session, expired session, revoked session, and rejection of client-supplied provider identity.
- **Done when:** All protected behavior is verified through real HTTP requests against the test app.

### Step 5: Add frontend checks

- **What to do:** Verify login rendering, navigation, route protection, and failure states.
- **Where:** `frontend/` test files using the repository-selected test framework.
- **How:** Render the login page, exercise the login result, check navigation labels/routes, and verify loading/error UI. Keep mocks limited to external boundaries and test user-visible behavior.
- **Done when:** Tests fail if the shell loses its primary routes or auth behavior.

### Step 6: Add browser smoke coverage

- **What to do:** Validate the local vertical path when the CI environment supports browsers.
- **Where:** `frontend/tests/e2e/` or the repository's browser-test directory.
- **How:** Start both services, open login, sign in with the demo credential, navigate through each shell route, log out, and confirm the login redirect.
- **Done when:** One smoke test proves the foundation works across frontend and backend boundaries.

### Step 7: Add CI jobs

- **What to do:** Run checks automatically for every change.
- **Where:** `.github/workflows/ci.yml` or the repository's CI configuration.
- **How:** Install dependencies, run backend formatting/lint/type checks and tests, then run frontend lint/type checks/tests. Add browser setup only if supported by the runner.
- **Done when:** CI reports failures clearly and a clean change passes all required checks.

### Step 8: Document validation commands

- **What to do:** Make local verification repeatable.
- **Where:** `README.md` and package/project scripts.
- **How:** Document exact commands for backend tests, frontend tests, linting, type checks, migrations, and the optional browser smoke test.
- **Done when:** A junior engineer can run the same checks locally that CI runs.

## Interface and Data Contracts

- Tests must use the public HTTP/API behavior for health and auth.
- Test databases and test sessions must be isolated from local developer data.
- CI must run the same focused checks documented for local development.

## Verification

1. Run backend tests against a fresh temporary database; confirm all pass.
2. Run frontend lint, type checks, and tests; confirm all pass.
3. Run the browser smoke flow if browser tooling is available.
4. Push a harmless branch change and confirm CI executes the documented jobs.

## Acceptance Criteria

- [ ] Backend health/readiness tests exist and pass.
- [ ] Database migration/connectivity tests exist and pass.
- [ ] Login, session lookup, logout, and unauthorized access are tested.
- [ ] Frontend shell navigation and loading/error behavior are tested.
- [ ] CI runs the focused frontend/backend checks.
- [ ] README documents the commands used by developers and CI.

## Out of Scope

- Evaluation of generated summaries or agent quality.
- Production load testing, security certification, or deployment pipelines.
- Tests for workflows that belong to later epics.

## Notes

Prefer real behavior through the FastAPI test client and rendered user flows. Avoid tests that only assert mocked implementation calls or add production methods solely to make tests easier.
