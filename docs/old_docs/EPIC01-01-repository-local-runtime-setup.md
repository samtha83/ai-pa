# Feature: Repository and Local Runtime Setup

- **EPIC:** EPIC-01
- **Feature ID:** 01
- **Status:** Not Started
- **Source spec:** context/features/phase1-spec.md

## Goal

Create a reproducible local development environment in which the Next.js frontend and FastAPI backend can be installed, configured, and started by following the repository documentation.

## Why This Matters

Every later feature depends on both services being available with predictable commands, environment variables, and repository boundaries.

## Prerequisites

- Node.js and the repository-supported package manager.
- Python 3.11+ and the repository-supported Python package manager.
- SQLite available locally.
- The repository root at `/home/samtha17/projects/new-ai-pa/ai-pa`.

## Implementation Steps

### Step 1: Create the application directories

- **What to do:** Add separate frontend and backend application directories.
- **Where:** `frontend/` and `backend/` at the repository root.
- **How:** Keep browser code under `frontend/` and Python API code under `backend/`. Do not put database or agent logic in frontend components.
- **Done when:** Both services have their own dependency manifest and can be developed independently.

### Step 2: Initialize the frontend

- **What to do:** Initialize a Next.js App Router application with React, TypeScript, and Tailwind CSS.
- **Where:** `frontend/`.
- **How:** Use the repository-supported Node package manager and enable strict TypeScript checks. Keep the default start, build, lint, and type-check commands documented.
- **Done when:** The frontend starts locally and renders a page without compilation errors.

### Step 3: Initialize the backend

- **What to do:** Create the FastAPI application package and development entry point.
- **Where:** `backend/app/` and `backend/pyproject.toml` or the selected Python dependency file.
- **How:** Add FastAPI, Uvicorn, Pydantic settings, SQLAlchemy, and the migration tool selected by the repository. Keep application construction in `app/main.py`.
- **Done when:** Uvicorn can import and start the FastAPI app.

### Step 4: Add environment configuration

- **What to do:** Define safe local configuration defaults and placeholders.
- **Where:** Root `.env.example`, plus frontend/backend environment files if the frameworks require them.
- **How:** Document frontend URL, backend URL, SQLite path, application environment, and session-secret placeholder. Never commit real secrets or `.env` files.
- **Done when:** A new developer can copy the example configuration and start both services.

### Step 5: Protect generated and runtime files

- **What to do:** Update ignore rules for local-only files.
- **Where:** `.gitignore`.
- **How:** Ignore databases, uploads, generated artifacts, build output, dependency caches, and secret environment files. Keep an example environment file tracked.
- **Done when:** Running the services does not produce accidental source-control changes for local data.

### Step 6: Document local commands

- **What to do:** Document installation, startup, testing, and shutdown commands.
- **Where:** `README.md` or a dedicated local development section.
- **How:** Include separate frontend/backend commands, expected ports, API docs URL, environment setup, SQLite location, and the fact that demo auth is not production authentication.
- **Done when:** A developer unfamiliar with the project can follow the document from a clean checkout.

## Interface and Data Contracts

- Frontend local origin and backend API origin must be configurable.
- The backend must expose its API under `/api/v1`.
- Runtime data must be stored outside source files and must be safe to delete for a clean local reset.

## Verification

1. Install frontend and backend dependencies from a clean environment.
2. Start both services using only the documented commands.
3. Open the frontend and confirm it renders; open the backend API docs and confirm they load.
4. Confirm `.env`, SQLite, uploads, and build output are ignored by Git.

## Acceptance Criteria

- [ ] Frontend starts without compilation errors.
- [ ] Backend starts without import or configuration errors.
- [ ] Environment variables and local defaults are documented.
- [ ] Runtime files and secrets are excluded from source control.
- [ ] README contains reproducible local setup instructions.

## Out of Scope

- Provider onboarding behavior.
- LLM, LangGraph, MCP, calendar, CRM, or messaging integrations.
- Production deployment or authentication.

## Notes

Use the architecture document's local-first approach. Do not add infrastructure that requires a separate database or external service for the Phase 1 demo.
