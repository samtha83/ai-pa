# Feature: Local Demo Authentication

- **EPIC:** EPIC-01
- **Feature ID:** 04
- **Status:** Not Started
- **Source spec:** context/features/phase1-spec.md

## Goal

Provide a clearly labeled local sign-in flow that creates a server-validated session, protects the app shell, and can later be replaced by production authentication.

## Why This Matters

The architecture requires provider-scoped access. Even in a local demo, future client data must not be retrieved using an arbitrary provider ID sent by the browser.

## Prerequisites

- Features 01 and 02 are available.
- Feature 03 provides provider and demo-session persistence.
- A local provider seed or development credential is defined.

## Implementation Steps

### Step 1: Seed a development provider

- **What to do:** Create one provider record for local development.
- **Where:** Development seed script or database initialization module.
- **How:** Use an obvious demo identity and document the credential or selection method without storing a real secret.
- **Done when:** A clean local database can be initialized with one provider for the demo.

### Step 2: Implement the auth service

- **What to do:** Encapsulate login, session creation, session lookup, and revocation.
- **Where:** `backend/app/services/auth_service.py` or the repository's service boundary.
- **How:** Validate the development credential, create an opaque random session value, store only its hash with expiry, and return the provider identity from the server-side lookup.
- **Done when:** The service can distinguish valid, expired, revoked, and unknown sessions.

### Step 3: Add auth API routes

- **What to do:** Implement login, logout, and current-session endpoints.
- **Where:** `backend/app/api/v1/auth.py`.
- **How:** Add `POST /api/v1/auth/login`, `POST /api/v1/auth/logout`, and `GET /api/v1/auth/me`. Use an HTTP-only cookie or another server-validated transport.
- **Done when:** Login establishes a session, `me` returns the provider, and logout invalidates the session.

### Step 4: Add a protected-route dependency

- **What to do:** Provide reusable authentication enforcement for API routes.
- **Where:** `backend/app/core/auth.py` or an equivalent dependency module.
- **How:** Read the session transport, hash/validate it, check expiry and revocation, and inject the provider identity into protected handlers. Never trust a provider ID from the request body as identity.
- **Done when:** A protected endpoint returns an authorization error without a valid session and receives the correct provider with one.

### Step 5: Connect the frontend session flow

- **What to do:** Add login form submission, session loading, and logout behavior.
- **Where:** `frontend/app/login/` and shared session/API client modules.
- **How:** Submit credentials to the backend, preserve the session cookie according to the selected frontend/backend setup, redirect to `/dashboard`, and redirect unauthenticated protected pages to `/login`.
- **Done when:** A user can log in, refresh the dashboard, navigate, and log out.

### Step 6: Label the demo limitation

- **What to do:** Make the non-production nature visible.
- **Where:** Login UI and README.
- **How:** State that this is local demo authentication and is not suitable for production or regulated client data.
- **Done when:** A stakeholder cannot reasonably mistake the flow for production identity management.

## Interface and Data Contracts

- `POST /api/v1/auth/login` creates the local session.
- `POST /api/v1/auth/logout` revokes/clears the local session.
- `GET /api/v1/auth/me` returns the authenticated provider.
- Protected API dependencies provide provider identity from the validated session.
- Session credentials are not logged or stored in plaintext.

## Verification

1. Log in with the documented local demo credential and confirm redirect to `/dashboard`.
2. Call `/api/v1/auth/me` with and without the session; compare the authorized and unauthorized responses.
3. Log out, refresh a protected route, and confirm redirect to `/login`.
4. Revoke or expire a test session and confirm protected requests are rejected.

## Acceptance Criteria

- [ ] One development provider can be seeded.
- [ ] Login, session lookup, and logout work through the API.
- [ ] Sessions are HTTP-only/server-validated and do not trust browser-supplied provider IDs.
- [ ] Expired and revoked sessions are rejected.
- [ ] Protected routes redirect or reject unauthenticated users.
- [ ] Demo-only limitations are documented in the UI and README.

## Out of Scope

- Production authentication, password reset, MFA, RBAC, or multi-tenant identity management.
- Client consent, HIPAA compliance, or external identity providers.

## Notes

Keep the auth service behind an interface so a future identity provider can replace it without changing client, summary, or scheduling route contracts.
