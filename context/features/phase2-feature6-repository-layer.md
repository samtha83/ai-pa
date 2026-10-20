# Feature: Repository Layer

- **Phase:** Phase 2: Provider and Client Data Foundation
- **Feature ID:** phase2-feature6
- **Status:** Completed
- **Source plan:** docs/mvp-build-plan.md

## Goal

Add the repository layer that encapsulates provider-scoped data access for profiles, preferences, and client records so the backend remains easy to test and consistent across API routes and services.

## Non-Goals

- Building a distributed persistence abstraction.
- Introducing service-to-service APIs or external database integration.
- Handling production-grade auditing or access control beyond provider scoping.

## Why This Matters

The repository layer keeps the rest of the backend clean and reliable. By centralizing data access, the MVP avoids duplicate logic and ensures that all provider and client data follows the same scoping, validation, and update principles.

## Prerequisites

- Provider, preference, and client models exist in the backend.
- The app has database sessions and a working local SQLite connection.
- API routes and validation schemas are ready to integrate with repository methods.

## Technical Solution

Create repository classes for provider profiles, provider preferences, and clients. Each repository method should accept the active provider context and query only records belonging to that provider. Keep the repository layer thin but explicit: create, list, update, and fetch by ID operations should be centralized here and used by the service or API layer.

This layer should stay intentionally simple and local; it is not a general-purpose persistence framework and should not add complexity that would be unnecessary for the MVP.

## Implementation Steps

### Step 1: Add provider repository

- **What to do:** Create repository methods for reading and updating the provider record.
- **Where:** `backend/app/repositories/`.
- **How:** Implement lookup by ID and create/update operations using the SQLAlchemy session factory. Keep provider access limited to the active provider context.
- **Done when:** The repository can fetch and update the current provider without writing custom query logic in the route layer.

### Step 2: Add preference repository

- **What to do:** Add repository methods for provider preferences.
- **Where:** `backend/app/repositories/`.
- **How:** Implement get-or-create behavior for preference defaults and update logic for existing values. Ensure the repository only returns records from the active provider.
- **Done when:** Preference retrieval and updates are centralized and deterministic.

### Step 3: Add client repository

- **What to do:** Add repository methods to list, create, update, and fetch clients by provider scope.
- **Where:** `backend/app/repositories/`.
- **How:** Write provider-scoped queries and ensure client-fetch operations reject cross-provider access. Keep methods narrow and easy to reuse in the API layer.
- **Done when:** Client data access is consistent across all API endpoints.

## Interface and Data Contracts

- Repository methods return SQLAlchemy models or normalized records for provider and client data.
- Provider scoping is enforced in the repository layer for every query.
- Repositories are used by the service or route layer instead of direct session access.
- All database actions remain local to the SQLite instance for the MVP.

## Verification

1. Run `cd backend && pytest` after the repository layer is in place.
2. Create and retrieve provider and client records using repository methods and ensure provider scoping is respected.
3. Confirm the repository layer eliminates duplicate logic and handles update failures cleanly.

## Acceptance Criteria

- [x] Provider, preference, and client repositories exist and are used by the backend.
- [x] Repository queries are scoped to the signed-in provider.
- [x] Client and profile update flows return consistent storage results.
- [x] The backend no longer depends on ad hoc database queries in route logic.

## Out of Scope

- Distributed or remote persistence.
- Advanced RBAC or enterprise authorization.
- Complex domain services beyond provider and client scoping.

## Notes

This repository layer forms the backend's systematic storage boundary for Phase 2. It is intentionally small enough to stay maintainable while being general enough to support the rest of the MVP workflow.

Provider creation is available as a repository operation for future internal workflows such as signup; it is not exposed as a profile creation endpoint or UI screen.
