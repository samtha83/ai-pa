# Feature: Add Demo Auth

- **Phase:** Phase 1: Local Runtime Foundation
- **Feature ID:** phase1-feature5
- **Status:** Not Started
- **Source plan:** docs/mvp-build-plan.md

## Goal

Provide a clearly labeled local authentication flow that creates a provider session, protects application routes, and leaves a clean replacement point for production identity later.

## Non-Goals

- Production identity, OAuth, OIDC, RBAC, or multi-provider administration.
- Password recovery, email verification, or external identity providers.
- Trusting a provider ID supplied by the browser.

## Why This Matters

Provider-scoped access is required before client and session data can be added safely. Demo auth gives the local MVP a realistic session boundary without pretending to solve production authentication.

## Prerequisites

- FastAPI application exists from `phase1-feature3-initialize-backend`.
- Provider and demo-session tables exist from `phase1-feature4-add-sqlite-layer`.
- Frontend shell exists from `phase1-feature2-initialize-frontend`.

## Technical Solution

Seed one clearly identified development provider. Implement an auth service with login, logout, and current-user operations. Use an HTTP-only cookie or equivalent server-validated session transport. Store only an opaque session identifier or hash in the database, derive provider identity on the server, and expose the development-only nature of the flow in the UI and documentation.

Add backend authentication dependencies for protected routes and a frontend session loader/provider for protected pages. The same provider identity must be passed into future repositories and workflow calls by the server.

## Implementation Steps

### Step 1: Seed the development provider

- **What to do:** Add one clearly labeled local provider during development initialization.
- **Where:** Proposed location `backend/app/db/seed.py` or startup seed module.
- **How:** Make seeding idempotent and do not create duplicate providers on restart.
- **Done when:** A clean local database has one usable demo provider.

### Step 2: Implement the auth service

- **What to do:** Create login, logout, and current-session operations.
- **Where:** Proposed locations `backend/app/auth/` and `backend/app/api/v1/auth.py`.
- **How:** Issue a server-validated session token through an HTTP-only cookie or equivalent. Apply expiry and revocation using the session table.
- **Done when:** The service can create, resolve, and revoke a provider session.

### Step 3: Add auth API routes

- **What to do:** Expose the local auth endpoints.
- **Where:** `backend/app/api/v1/auth.py`.
- **How:** Add `POST /api/v1/auth/login`, `POST /api/v1/auth/logout`, and `GET /api/v1/auth/me`. Return safe errors for invalid or expired sessions.
- **Done when:** The three endpoints work against the local database.

### Step 4: Protect backend routes

- **What to do:** Add an authentication dependency for protected routes.
- **Where:** Proposed location `backend/app/auth/dependencies.py`.
- **How:** Resolve provider identity from the server-side session and reject unauthenticated requests. Never accept arbitrary provider identity from request payloads.
- **Done when:** A protected test route rejects missing sessions and accepts the valid demo session.

### Step 5: Connect frontend session behavior

- **What to do:** Add login form, logout action, session loading, and protected-route redirect.
- **Where:** Frontend login route, shared layout, and proposed session module.
- **How:** Display a development-only label and show provider/session state in the app shell.
- **Done when:** Successful login reaches the dashboard and unauthenticated protected routes return to login.

## Interface and Data Contracts

- `POST /api/v1/auth/login` creates a local session.
- `POST /api/v1/auth/logout` revokes or clears the local session.
- `GET /api/v1/auth/me` returns the current provider identity.
- Browser identity is represented by a server-validated session, not a client-supplied provider ID.
- Protected endpoints receive provider identity from an auth dependency.

## Verification

1. **Command:** Run backend API tests using the repository's configured test command; mark it `TBD` until defined.
2. Log in through the frontend and confirm the dashboard shows the demo provider.
3. Clear the session and request a protected route; confirm the request is rejected or redirected to login.
4. Log out and confirm the same session cannot access protected backend routes.

## Acceptance Criteria

- [ ] One development provider is seeded idempotently.
- [ ] Login, logout, and current-user endpoints work.
- [ ] Sessions have expiry and revocation behavior.
- [ ] Protected routes reject unauthenticated requests.
- [ ] Provider identity is resolved server-side.
- [ ] Frontend redirects unauthenticated users to login.
- [ ] Development-only auth limitations are visible in the UI and docs.

## Out of Scope

- Production authentication and authorization.
- Multi-provider tenancy or roles.
- Client-facing accounts.
- OAuth, OIDC, password reset, or account registration.

## Notes

This feature depends on the SQLite layer and should be completed before provider-scoped domain features. Do not log session tokens or credentials.
