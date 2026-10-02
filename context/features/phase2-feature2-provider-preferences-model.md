# Feature: Provider Preferences Model

- **Phase:** Phase 2: Provider and Client Data Foundation
- **Feature ID:** phase2-feature2
- **Status:** Completed
- **Source plan:** docs/mvp-build-plan.md

## Goal

Add a provider preferences model that captures the working assumptions the MVP needs for scheduling, summaries, and operational defaults without overbuilding the first release.

## Non-Goals

- Creating a fully configurable enterprise settings system.
- Building external calendar integrations or real business rules engine logic.
- Defining all later Phase 5 scheduling features in one step.

## Why This Matters

The provider's preferences define the working window, session cadence, and summary defaults. These values drive the later scheduling and summary workflow and keep the MVP aligned with the provider's operational boundaries.

## Prerequisites

- Phase 2 provider profile data model is available.
- The backend app can persist provider-scoped SQLite records.
- Demo auth provides a valid provider identity for the local app.

## Technical Solution

Create a provider preferences model with a one-to-one relationship to the provider profile. Track local working hours, session duration, buffer time, blackout dates, max sessions per day, and the selected summary template or tone configuration. Keep this model provider-scoped and validated by Pydantic schemas. Add repository/service accessors for reading and updating preferences securely.

This is a local demo-only configuration layer and should remain intentionally simple: no external settings sync, no production secrets, and no complex scheduling engine integration yet.

## Implementation Steps

### Step 1: Define provider preferences schema

- **What to do:** Add a SQLAlchemy model for provider preferences with the required operational defaults.
- **Where:** `backend/app/models/` and any associated migration files.
- **How:** Include `working_hours`, `session_duration`, `buffer_time`, `blackout_dates`, `max_sessions_per_day`, and summary template choices. Keep these fields simple and deterministic for the MVP.
- **Done when:** The preferences object can be created and stored in SQLite for the active provider.

### Step 2: Add backend validation and service logic

- **What to do:** Add Pydantic request validation and a service repository for get/update operations.
- **Where:** `backend/app/schemas/`, `backend/app/repositories/`, and `backend/app/services/`.
- **How:** Ensure values are numeric or structured correctly, enforce provider scoping, and reject malformed schedules or invalid working hours.
- **Done when:** Invalid preference input fails cleanly with explicit errors.

### Step 3: Expose the provider preference API

- **What to do:** Add API routes to read and update preferences.
- **Where:** `backend/app/api/v1/`.
- **How:** Keep the endpoint provider-scoped and map it to the active session provider ID. Return defaults when preferences have not yet been set and preserve explicit provider ownership.
- **Done when:** A provider can fetch and write their preference record without crossing provider boundaries.

## Interface and Data Contracts

- Preferences are stored as a provider-scoped record in SQLite.
- The API exposes read/write access for provider defaults and scheduling assumptions.
- Preference values remain local and deterministic for the MVP.
- These fields are used as inputs to later scheduling and summary generation features.

## Verification

1. Run `cd backend && pytest` after adding the new model and routes.
2. Insert or update a provider preference record and confirm it persists under the provider's ID.
3. Confirm invalid preference payloads fail validation and that the active provider can read only their own settings.

## Acceptance Criteria

- [x] A provider preference model exists and saves under the correct provider record.
- [x] Required scheduling and summary defaults are stored and validated.
- [x] Provider-specific preferences are protected by scoping rules.
- [x] The backend exposes a read/update path for preferences.

## Out of Scope

- Real calendar sync with external systems.
- Production-level enterprise configuration features.
- AI-driven personalization beyond MVP defaults.

## Notes

This feature is the application-level configuration layer for the local demo. Working-hour values are local clock times without timezone offsets and are interpreted using the provider profile's IANA timezone. Future chat responses and appointment message text should show the provider's local time with the date-appropriate timezone label (for example, EST or EDT). Plain email prose is not automatically converted by mail clients; a structured calendar invitation may be rendered in the recipient's timezone. The API derives provider scope from the authenticated session and does not accept caller-selected provider IDs. Frontend settings UI and external calendar integration remain out of scope.
