# Feature: API Routes

- **Phase:** Phase 2: Provider and Client Data Foundation
- **Feature ID:** phase2-feature5
- **Status:** Completed
- **Source plan:** docs/mvp-build-plan.md

## Goal

Add the backend API routes that let the current provider read and write their profile, preferences, and client records through the versioned application interface. Derive the provider ID exclusively from the authenticated session for every operation; never trust a provider ID supplied by the request when selecting records to read or modify.

## Non-Goals

- Building a full admin API or multi-provider platform access layer.
- Adding summary generation, chat retrieval, or scheduling APIs.
- Handling production-level compliance or enterprise authorization patterns.

## Why This Matters

The MVP depends on explicit backend endpoints for provider onboarding and client management. These routes provide the stable contract between the frontend and the persistence layer and keep provider actions scoped to the signed-in identity.

## Prerequisites

- Provider profile, preferences, and client models must exist.
- The app must have a local SQLite-backed database and working demo auth.
- The repository layer must provide provider-scoped access methods.

## Technical Solution

Add versioned API routes under `backend/app/api/v1/` for provider profile reads/writes, provider preference reads/writes, and client list/create/update operations. Resolve the provider ID from the validated session dependency and pass that trusted ID to provider-scoped services; do not accept a provider ID from request bodies, query parameters, or path parameters as the authorization scope. Validate input using Pydantic schemas and keep errors explicit and consistent with the rest of the FastAPI backend.

These routes are the bridge between browser actions and the provider-scoped service layer. The local demo should remain simple and predictable, with clear validation responses for invalid data and unauthorized access.

## Implementation Steps

### Step 1: Add provider endpoints

- **What to do:** Create routes for reading and updating the current provider profile.
- **Where:** `backend/app/api/v1/provider.py` or equivalent route module.
- **How:** Read the active provider identity from the session context and return the profile record or a not-found/validation response. Ignore or reject caller-supplied provider IDs as a scope selector. Keep values consistent with the provider schema.
- **Done when:** A provider can fetch and update their own profile through the backend.

### Step 2: Add preferences endpoints

- **What to do:** Create routes for retrieving and updating provider preferences.
- **Where:** `backend/app/api/v1/preferences.py` or equivalent route module.
- **How:** Use the signed-in provider ID to load or initialize preferences and validate the payload before saving. Return explicit errors for malformed schedules or unsupported values.
- **Done when:** A provider can read and save preference defaults using API calls.

### Step 3: Add client endpoints

- **What to do:** Add list, create, and detail update endpoints for client records.
- **Where:** `backend/app/api/v1/clients.py` or equivalent route module.
- **How:** Include endpoints for listing all clients for a provider, creating a client, fetching a client by ID, and updating its values. Restrict all reads and writes to the current provider account.
- **Done when:** The UI can create and manage client records through API calls.

## Interface and Data Contracts

- API routes live under `/api/v1` and are keyed to the signed-in provider context.
- The provider ID used for data access comes from the validated session, not request-controlled input.
- Provider and client payloads use Pydantic schemas validated by backend request models.
- All writes are scoped to the current provider and reject cross-provider data access.
- Response payloads return normalized provider/client records with explicit error states.

## Verification

1. Run `cd backend && pytest` after the routes are added.
2. Exercise the provider and client endpoints through the local API and confirm the returned records match the database state.
3. Attempt to access another provider's record while authenticated as the current provider and confirm it is not returned or modified, including when a request supplies another provider ID.
4. Confirm unauthenticated or invalid requests return explicit backend errors.

## Acceptance Criteria

- [x] Provider-specific API routes exist and return the current provider data.
- [x] Preference endpoints support read and update operations for the active provider.
- [x] Client list/create/detail routes are provider-scoped and validate payloads.
- [x] Every provider/client data operation derives its provider scope from the authenticated session and rejects cross-provider access even if the request supplies another provider ID.
- [x] Invalid or cross-provider requests fail cleanly with explicit errors.

## Out of Scope

- Future workflow APIs for summaries, chat, or scheduling.
- Multi-provider administration or enterprise-level permissions.
- External service integrations.

## Notes

This feature is the API boundary that turns the provider and client models into usable application functionality. It should be small, explicit, and consistent with the backend's local demo security model.

The authenticated provider profile, preference, and client routes were already implemented and registered before this feature started. Added regression coverage for unauthenticated profile/client requests, request-supplied provider IDs in query/body data, and prevention of cross-provider client updates. Verified the complete backend suite with 31 passing tests.
