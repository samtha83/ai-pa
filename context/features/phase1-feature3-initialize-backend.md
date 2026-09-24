# Feature: Initialize Backend Stack

- **Phase:** Phase 1: Local Runtime Foundation
- **Feature ID:** phase1-feature3
- **Status:** Not Started
- **Source plan:** docs/mvp-build-plan.md

## Goal

Create a runnable FastAPI backend served by Uvicorn with versioned routes, configuration loading, middleware, and consistent error responses.

## Non-Goals

- Implementing provider, client, session, or assistant workflows.
- Adding LangGraph, Azure OpenAI, MCP, AG-UI, or SSE behavior.
- Implementing production authentication or authorization.

## Why This Matters

FastAPI is the backend trust boundary for the product. Establishing its application structure and error behavior early gives every later feature a stable place for validation, authorization, and workflow endpoints.

## Prerequisites

- `backend/` exists from `phase1-feature1-repo-structure`.
- Python 3.11+ and the repository-supported package manager are available.
- The local environment contract is defined.

## Technical Solution

Create a Python application package with application construction in `backend/app/main.py`. Add Pydantic settings, a versioned `/api/v1` router, CORS restricted to the configured local frontend origin, request correlation IDs, and structured error models. Keep persistence, authentication, and agent orchestration behind separate modules so the main application does not become a monolith.

Run the service with Uvicorn. The initial health route may be implemented here, while database readiness belongs to the SQLite feature.

## Implementation Steps

### Step 1: Create the Python application package

- **What to do:** Add the FastAPI application package and dependency manifest.
- **Where:** `backend/app/` and `backend/pyproject.toml` or the selected dependency file.
- **How:** Add FastAPI, Uvicorn, Pydantic settings, and the repository-supported test tooling.
- **Done when:** Uvicorn can import the application object.

### Step 2: Add configuration loading

- **What to do:** Define typed application settings.
- **Where:** Proposed location `backend/app/core/config.py`.
- **How:** Load environment values for application environment, frontend origin, API prefix, and local data paths. Provide safe local defaults where appropriate.
- **Done when:** The application starts with documented local configuration and reports useful errors for invalid required settings.

### Step 3: Add versioned API composition

- **What to do:** Create the `/api/v1` router structure.
- **Where:** Proposed locations `backend/app/api/` and `backend/app/main.py`.
- **How:** Keep route modules separate from domain services. Register the health route under the versioned prefix.
- **Done when:** The generated API documentation shows the versioned route.

### Step 4: Add middleware and error responses

- **What to do:** Configure local CORS, correlation IDs, and consistent JSON errors.
- **Where:** Proposed locations `backend/app/core/` and `backend/app/main.py`.
- **How:** Return a machine-readable error code, human-readable message, and correlation ID. Never expose stack traces in API responses.
- **Done when:** invalid requests return the agreed error shape and include a correlation identifier.

### Step 5: Add the health endpoint

- **What to do:** Implement a process health check.
- **Where:** Proposed location `backend/app/api/v1/health.py`.
- **How:** Return service status and application version without requiring a model, MCP service, or database write.
- **Done when:** `GET /api/v1/health` returns HTTP 200 while the service is running.

## Interface and Data Contracts

- Backend application object: proposed `backend/app/main.py`.
- API prefix: `/api/v1`.
- Health route: `GET /api/v1/health`.
- Error response includes a stable code, readable message, and correlation ID.
- CORS allows only the configured local frontend origin.

## Verification

1. **Command:** Run Uvicorn using the repository's documented backend command; mark as `TBD` if not yet documented.
2. Open the local FastAPI docs and request `GET /api/v1/health`.
3. Send an invalid request and confirm the response is structured and does not expose a traceback.

## Acceptance Criteria

- [ ] FastAPI starts without import or configuration errors.
- [ ] Uvicorn serves the application.
- [ ] `/api/v1` route organization exists.
- [ ] Health endpoint returns HTTP 200 with service status and version.
- [ ] Local CORS and correlation IDs are configured.
- [ ] Errors use a consistent safe response shape.

## Out of Scope

- SQLite connectivity and migrations.
- Local login/session behavior.
- LangGraph or assistant endpoints.
- Real external integrations.

## Notes

The backend should remain a transport and policy boundary. Keep business logic in services and repositories introduced by later features.
