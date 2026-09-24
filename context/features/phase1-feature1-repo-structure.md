# Feature: Create Repo Structure

- **Phase:** Phase 1: Local Runtime Foundation
- **Feature ID:** phase1-feature1
- **Status:** Not Started
- **Source plan:** docs/mvp-build-plan.md

## Goal

Create the minimum repository structure needed to develop the frontend, backend, documentation, and local runtime data independently.

## Non-Goals

- Implementing application features or API endpoints.
- Installing the complete frontend or backend dependency stacks.
- Adding production deployment infrastructure.

## Why This Matters

A predictable repository layout gives later features clear ownership boundaries and prevents browser code, backend logic, and local runtime data from becoming coupled.

## Prerequisites

- Repository root: `/home/samtha17/projects/new-ai-pa/ai-pa`.
- Git is initialized for the repository.
- The existing documentation and feature files must be preserved.

## Technical Solution

Create `frontend/` for Next.js code, `backend/` for FastAPI code, `docs/` for project documentation, and `data/` for ignored local runtime data. Add a root `.env.example` containing safe placeholders and update `.gitignore` so databases, uploads, generated files, dependency caches, build output, and secret environment files remain local.

Do not place application code in `data/`, and do not commit real credentials. The directory structure should remain compatible with the later LangGraph and MCP work.

## Implementation Steps

### Step 1: Create top-level directories

- **What to do:** Add `frontend/`, `backend/`, and `data/` directories if they do not exist.
- **Where:** Repository root.
- **How:** Keep frontend and backend source trees separate. Add a small placeholder file only when needed to preserve an empty directory in Git.
- **Done when:** The three runtime directories exist and have clear ownership.

### Step 2: Confirm the documentation boundary

- **What to do:** Keep project documentation under `docs/` and do not move existing documents.
- **Where:** `docs/`.
- **How:** Use repository-relative paths in future feature specs and setup instructions.
- **Done when:** Existing ADD and build-plan documents remain accessible from `docs/`.

### Step 3: Add the environment contract

- **What to do:** Create a safe root `.env.example`.
- **Where:** `.env.example`.
- **How:** Include placeholders for frontend URL, backend URL, SQLite path, application environment, and session-secret placeholder. Do not include real secrets.
- **Done when:** A developer can identify required configuration without seeing credentials.

### Step 4: Protect local files

- **What to do:** Update `.gitignore` for local runtime files.
- **Where:** `.gitignore`.
- **How:** Ignore `.env` files containing secrets, SQLite databases, uploads, generated artifacts, dependency caches, and frontend/backend build output while keeping `.env.example` tracked.
- **Done when:** Local runtime output does not appear as accidental source changes.

## Interface and Data Contracts

- Frontend code belongs under `frontend/`.
- Backend code belongs under `backend/`.
- Runtime data belongs under `data/` and must be safe to delete.
- Configuration is documented through `.env.example`.
- Project documentation remains under `docs/`.

## Verification

1. **Command:** TBD; inspect the repository tree from the repository root.
2. Confirm `frontend/`, `backend/`, `data/`, and `.env.example` exist.
3. Create a local test database or runtime artifact and confirm it is ignored by Git.

## Acceptance Criteria

- [ ] `frontend/`, `backend/`, and `data/` exist at the repository root.
- [ ] Existing documentation remains under `docs/`.
- [ ] `.env.example` documents safe local configuration placeholders.
- [ ] `.gitignore` excludes secrets, databases, uploads, caches, and build output.
- [ ] No real credentials or sensitive client data are added.

## Out of Scope

- Frontend scaffolding.
- FastAPI application setup.
- SQLite migrations or authentication.
- LangGraph, MCP, AG-UI, or LLM integration.

## Notes

This feature should be completed before the other Phase 1 features. Do not overwrite existing repository changes made by another contributor.
