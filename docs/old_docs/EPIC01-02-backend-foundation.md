# Feature: Backend Foundation

- **EPIC:** EPIC-01
- **Feature ID:** 02
- **Status:** Not Started
- **Source spec:** context/features/phase1-spec.md

## Goal

Establish a versioned FastAPI API boundary with configuration, routing, CORS, health checks, readiness checks, and consistent errors.

## Why This Matters

The frontend and future agent workflows need one stable backend boundary for authorization, validation, persistence, and integrations.

## Prerequisites

- Feature 01 application setup is available.
- FastAPI, Uvicorn, and Pydantic settings are installed.
- The database session boundary from Feature 03 can be imported or represented by a temporary health dependency.

## Implementation Steps

### Step 1: Create the FastAPI application

- **What to do:** Build the application factory and entry point.
- **Where:** `backend/app/main.py`.
- **How:** Create the FastAPI instance, set the application title/version, and include the `/api/v1` router. Keep startup wiring separate from route business logic.
- **Done when:** Uvicorn starts the application and `/docs` is available locally.

### Step 2: Add settings management

- **What to do:** Load configuration from environment variables with safe local defaults.
- **Where:** `backend/app/core/config.py` or the repository's equivalent settings module.
- **How:** Define typed settings for environment name, API version, frontend origins, SQLite URL, and session configuration. Fail clearly for required production-only settings, but allow documented local defaults.
- **Done when:** The application reports a useful configuration error instead of a traceback when configuration is invalid.

### Step 3: Add versioned routers

- **What to do:** Create a router hierarchy for future resources.
- **Where:** `backend/app/api/v1/router.py` and resource modules under `backend/app/api/v1/`.
- **How:** Mount health and auth routers under `/api/v1`. Keep route handlers thin and call services for behavior.
- **Done when:** The generated OpenAPI document lists `/api/v1/health` and `/api/v1/ready`.

### Step 4: Add health and readiness endpoints

- **What to do:** Separate process health from dependency readiness.
- **Where:** `backend/app/api/v1/health.py`.
- **How:** Return HTTP 200 from health with service status and version. Check SQLite connectivity in readiness and return HTTP 503 with a structured error if it is unavailable.
- **Done when:** Health succeeds even when a dependency check is not performed, while readiness reflects database availability.

### Step 5: Configure CORS

- **What to do:** Allow the configured local frontend to call the API.
- **Where:** `backend/app/main.py` or middleware configuration module.
- **How:** Read an explicit allowlist from settings. Do not use unrestricted origins with credentials enabled.
- **Done when:** Browser requests from the configured frontend origin succeed and an unconfigured origin is not silently accepted.

### Step 6: Add shared errors and request IDs

- **What to do:** Make API failures consistent and traceable.
- **Where:** `backend/app/core/errors.py` and middleware modules.
- **How:** Return a machine-readable error code, human-readable message, and request ID. Add the request ID to response headers. Log request metadata without raw client or session content.
- **Done when:** An invalid request returns predictable JSON and no stack trace or sensitive content.

## Interface and Data Contracts

- `GET /api/v1/health` returns HTTP 200 with service status and version.
- `GET /api/v1/ready` returns HTTP 200 when SQLite is reachable and HTTP 503 otherwise.
- Error responses include a stable error code, message, and request ID.
- API versioning begins at `/api/v1`.

## Verification

1. Start the backend and request `/api/v1/health`; confirm HTTP 200.
2. Request `/api/v1/ready` with a working database; confirm HTTP 200.
3. Temporarily point the database setting at an unavailable location; confirm HTTP 503 and structured JSON.
4. Send a request from the configured frontend origin and confirm CORS headers are present.

## Acceptance Criteria

- [ ] FastAPI starts through a documented Uvicorn command.
- [ ] Health and readiness endpoints return the specified statuses.
- [ ] Routes are mounted under `/api/v1`.
- [ ] CORS uses a configured allowlist.
- [ ] Errors are structured and do not expose stack traces.
- [ ] Request IDs are available for debugging without logging sensitive content.

## Out of Scope

- Business endpoints for clients, summaries, appointments, or tasks.
- Agent orchestration and external adapters.
- Production identity provider integration.

## Notes

Keep route handlers small. This boundary should allow later features to add services and repositories without moving database or policy code into the frontend.
