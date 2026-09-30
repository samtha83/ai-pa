# Feature: Provider Profile Model

- **Phase:** Phase 2: Provider and Client Data Foundation
- **Feature ID:** phase2-feature1
- **Status:** Completed
- **Source plan:** docs/mvp-build-plan.md

## Goal

Add the provider profile data model so the app can persist the signed-in provider's identity, business details, and local preferences in a provider-scoped store.

## Non-Goals

- Implementing client records or scheduling logic.
- Creating a full onboarding wizard or production identity management system.
- Building provider preference UI or chat retrieval flows.

## Why This Matters

Every later workflow depends on provider ownership, timezone awareness, and stable identity metadata. This feature creates the foundation for saving and retrieving provider-specific data safely and consistently.

## Prerequisites

- Phase 1 runtime foundation and demo auth must be complete.
- The backend must have SQLite and Alembic configured.
- The repository root environment contract must be available via `.env`.

## Technical Solution

Create a SQLAlchemy model for provider profile data with fields for `name`, `business_name`, `timezone`, and optional provider metadata such as tone, modality, service type, template settings, and boundary preferences. Keep the record keyed to the current provider and use provider-scoped query logic when reading or writing related records. Add a Pydantic schema for API validation and a repository layer that enforces the signed-in provider context.

The model should support the local MVP's core business flow without introducing production-grade identity or enterprise configuration patterns. Use deterministic validation rules and keep the data local to SQLite during the demo period.

## Implementation Steps

### Step 1: Add the provider model

- **What to do:** Add a SQLAlchemy `Provider` model in the backend app models package.
- **Where:** `backend/app/models/provider.py` and related model package exports.
- **How:** Define required fields for provider identity, `business_name`, and timezone, plus optional metadata fields that are needed for the upcoming provider and client workflows. Add timestamps and a stable primary key.
- **Done when:** The model can be created in a migration and persists successfully via the local SQLite session.

### Step 2: Define provider validation schemas

- **What to do:** Add request/response schemas for profile reads and writes.
- **Where:** `backend/app/schemas/` or the backend API schema package.
- **How:** Validate required fields, timezone format, and empty-string handling. Ensure the schema does not allow confidential or regulated data by design.
- **Done when:** Invalid provider payloads fail validation with explicit API errors.

### Step 3: Wire provider persistence into the backend

- **What to do:** Add the provider repository and service pattern for saving and retrieving the current provider record.
- **Where:** `backend/app/repositories/` and `backend/app/services/`.
- **How:** Use the signed-in provider identity as a scoping boundary and return 404 or validation errors for missing records. Keep this feature focused on profile persistence and not broader workflow logic.
- **Done when:** A provider profile can be created and read without exposing a cross-provider resource.

## Interface and Data Contracts

- Provider identity is stored as a local SQLite-backed record with provider-scoped access.
- API payloads expose required provider metadata, including `name`, `business_name`, and `timezone`.
- Provider ownership is enforced by the signed-in provider context rather than by shared global data.
- The backend uses provider-scoped repository queries for reads and writes.

## Verification

1. Run the backend test suite with `cd backend && pytest`.
2. Create a provider profile through the API or repository layer and confirm it persists to SQLite.
3. Verify the stored record shows the expected provider details and that validation rejects invalid timezone values.

## Acceptance Criteria

- [x] A provider profile model exists and persists in the local SQLite database.
- [x] The required provider fields are validated and stored consistently.
- [x] Provider data remains scoped to the active signed-in provider.
- [x] Missing or invalid provider values produce clear backend validation errors.

## Out of Scope

- Client records or appointment scheduling.
- Frontend provider onboarding screens.
- Real identity provider integrations or production authentication.

## Notes

This feature extends the Phase 1 provider model rather than duplicating it. Provider API routes and frontend onboarding/settings UX remain in their dedicated Phase 2 features.
