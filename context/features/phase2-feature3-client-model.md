# Feature: Client Model

- **Phase:** Phase 2: Provider and Client Data Foundation
- **Feature ID:** phase2-feature3
- **Status:** Completed
- **Source plan:** docs/mvp-build-plan.md

## Goal

Add the client record model so a provider can create and manage client identities, contact data, and service context for later session and scheduling workflows.

## Non-Goals

- Building full CRM functionality or multi-provider client sharing.
- Creating complex patient intake workflows beyond the MVP needs.
- Implementing appointment booking or research workflows.

## Why This Matters

The client model is the operational center for the rest of the product. Session summaries, action plans, chat retrieval, and scheduling all depend on client records being available, readable, and owned by the correct provider.

## Prerequisites

- Provider profile and preferences models exist.
- The backend has a provider-scoped persistence pattern available.
- The app has a valid local demo provider context.

## Technical Solution

Create a client SQLAlchemy model with the core fields needed for the MVP: name, contact details, timezone, service type, goals, status, and provider ownership. Store the record in SQLite with a provider foreign key so clients remain private to their owning provider. Add validation and repository methods for creating, listing, updating, and retrieving a single client record.

Do not add overbroad legal or healthcare compliance fields in this feature. Keep the schema close to the immediate MVP user story and avoid data that would require production governance work.

## Implementation Steps

### Step 1: Define the client model

- **What to do:** Add the `Client` model and database schema.
- **Where:** `backend/app/models/` and the Alembic migration files.
- **How:** Include provider ownership, contact information, timezone, service type, goals, and status. Use a stable unique ID and provider foreign key.
- **Done when:** A client record can be saved and retrieved from SQLite.

### Step 2: Validate client payloads

- **What to do:** Add request/response schemas for client creation and updates.
- **Where:** `backend/app/schemas/`.
- **How:** Enforce relevant required fields and reject blank names or invalid provider references. Keep validation focused on the MVP data contract.
- **Done when:** Invalid client payloads return clear API errors.

### Step 3: Add repository and API access

- **What to do:** Create repository methods and API routes for listing/creating/updating clients.
- **Where:** `backend/app/repositories/`, `backend/app/services/`, and `backend/app/api/v1/`.
- **How:** Scope all client reads and writes to the authenticated provider and allow retrieval by provider and client ID. Do not allow cross-provider access.
- **Done when:** A provider can create and inspect their own client records.

## Interface and Data Contracts

- Each client is provider-owned and linked to the active provider record.
- The client object includes identity, service details, goals, and status.
- Client list/create/update APIs are provider-scoped in the backend.
- All reads and writes require a valid provider context or they fail.

## Verification

1. Run `cd backend && pytest` to validate the new model and API changes.
2. Create a client via the repository or API and confirm it is stored with the correct provider ID.
3. Confirm cross-provider access is blocked and invalid data is rejected.

## Acceptance Criteria

- [x] The client model persists in the local SQLite database.
- [x] A provider can create and list clients scoped to their own account.
- [x] Client data includes the fields required for later summary and scheduling workflows.
- [x] Cross-provider client access is rejected.

## Out of Scope

- Calendar integrations and real scheduling logic.
- Advanced CRM fields or production-regulated data models.
- Multi-provider shared client networks or enterprise roles.

## Notes

The client model is intentionally the simplest working record that supports session summaries and action plans later in the MVP. It should be stable and provider-scoped before later workflow features are built on top.
