# Feature: Add Startup Docs

- **Phase:** Phase 1: Local Runtime Foundation
- **Feature ID:** phase1-feature6
- **Status:** Not Started
- **Source plan:** docs/mvp-build-plan.md

## Goal

Document the exact local setup, configuration, startup, testing, and reset workflow so a new developer can run the MVP foundation from a clean checkout.

## Non-Goals

- Documenting unfinished feature behavior as if it exists.
- Creating production deployment or operations documentation.
- Adding external service credentials to the repository.

## Why This Matters

A local MVP is only useful if the team can reproduce it. Clear startup documentation reduces setup time, exposes missing dependencies, and keeps local demo expectations honest.

## Prerequisites

- Repository structure exists from `phase1-feature1-repo-structure`.
- Frontend and backend setup is available from the preceding Phase 1 features.
- The final frontend and backend commands are known or can be marked `TBD` until those features are implemented.

## Technical Solution

Add a local development section to the repository README or the agreed developer guide. Document prerequisites, environment-file setup, frontend and backend install commands, startup commands, expected ports, API documentation URL, SQLite/data location, test commands, local reset procedure, and the non-production status of demo authentication.

Keep secrets out of examples. Where a command depends on a package manager or migration tool that has not yet been selected, use `TBD` rather than inventing a command.

## Implementation Steps

### Step 1: Document prerequisites

- **What to do:** List required Node.js, Python, package manager, SQLite, and Git versions or supported ranges.
- **Where:** `README.md` or the repository's developer onboarding document.
- **How:** Keep requirements consistent with the actual manifests and scripts.
- **Done when:** A new developer can determine what to install before starting.

### Step 2: Document environment setup

- **What to do:** Explain how to copy `.env.example` and configure safe local values.
- **Where:** Local development documentation.
- **How:** Describe frontend URL, backend URL, SQLite path, application environment, and development session placeholder without including secrets.
- **Done when:** Configuration setup is clear and reproducible.

### Step 3: Document service startup

- **What to do:** Add separate frontend and backend installation and startup instructions.
- **Where:** Local development documentation.
- **How:** Include expected ports, FastAPI docs URL, and the order or terminal layout for running both services.
- **Done when:** A clean-checkout developer can start both services by following the document.

### Step 4: Document testing and reset

- **What to do:** Explain available lint, type-check, backend test, frontend test, migration, and local reset commands.
- **Where:** Local development documentation.
- **How:** Use exact repository scripts when known; mark unresolved commands as `TBD` until the corresponding feature defines them.
- **Done when:** Developers know how to verify the foundation and safely delete local runtime data.

### Step 5: Document MVP limitations

- **What to do:** Clearly label demo auth, local SQLite, mock integrations, and sensitive-data limitations.
- **Where:** README and/or developer onboarding document.
- **How:** State that the local MVP is not production authentication or a regulated-data deployment.
- **Done when:** The documentation does not imply production readiness.

## Interface and Data Contracts

- Documentation must reference the actual frontend/backend ports.
- Environment variable names must match `.env.example` and application settings.
- Commands must match package scripts and Python tooling once selected.
- Local data location and reset procedure must be explicit.

## Verification

1. **Command:** Follow the documented setup from a clean checkout; use `TBD` for any command not yet defined.
2. Ask a developer unfamiliar with the repository to start both services using only the documentation.
3. Confirm the frontend, health endpoint, API docs, and local login are reachable.
4. Confirm the reset procedure removes local data without deleting source files.

## Acceptance Criteria

- [ ] Prerequisites are documented.
- [ ] Environment setup and safe placeholder values are documented.
- [ ] Frontend and backend startup commands are documented.
- [ ] Expected ports and API docs URL are documented.
- [ ] Test and reset procedures are documented or marked `TBD`.
- [ ] Demo authentication and local MVP limitations are clearly stated.

## Out of Scope

- Production deployment instructions.
- CI/CD pipeline configuration.
- Real Azure OpenAI, MCP, calendar, or messaging credentials.
- Documentation for features not yet implemented.

## Notes

This feature is best completed after the other Phase 1 features so commands and paths reflect the actual implementation. It should still be updated whenever a later feature changes the local developer workflow.
