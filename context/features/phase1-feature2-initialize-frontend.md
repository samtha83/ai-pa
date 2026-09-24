# Feature: Initialize Frontend Stack

- **Phase:** Phase 1: Local Runtime Foundation
- **Feature ID:** phase1-feature2
- **Status:** Not Started
- **Source plan:** docs/mvp-build-plan.md

## Goal

Create a runnable Next.js App Router frontend with React, TypeScript, Tailwind CSS, and a basic route shell that later features can extend.

## Non-Goals

- Building provider onboarding, client workflows, chat, calendar, or review panels.
- Connecting to LangGraph, AG-UI, MCP, Azure OpenAI, or FastAPI beyond a future-ready configuration boundary.
- Implementing production authentication.

## Why This Matters

The frontend is the provider-facing entry point. A stable shell, routing structure, and predictable loading/error behavior let later features add workflows without rebuilding the application foundation.

## Prerequisites

- `frontend/` exists from `phase1-feature1-repo-structure`.
- Node.js and the repository-supported package manager are available.
- The root environment contract is documented.

## Technical Solution

Initialize a strict TypeScript Next.js App Router application under `frontend/`. Configure Tailwind CSS and use the repository-selected component library if one is already established; otherwise leave the component-library decision explicit for the next feature. Add a shared layout with placeholder routes for `/login`, `/dashboard`, `/clients`, `/calendar`, and `/settings`, plus route-level loading, error, and not-found states.

Keep API calls behind a small typed client boundary rather than placing fetch logic in presentational components. Use accessible semantic landmarks, visible keyboard focus, and text labels for state.

## Implementation Steps

### Step 1: Initialize the Next.js application

- **What to do:** Create the frontend application with App Router, React, and strict TypeScript checks.
- **Where:** `frontend/`.
- **How:** Use the repository-supported package manager and preserve the standard development, build, lint, and type-check scripts.
- **Done when:** The frontend development server can import and render the application.

### Step 2: Configure Tailwind and UI foundations

- **What to do:** Add Tailwind CSS and the selected component-library foundation.
- **Where:** `frontend/` configuration and shared UI directories.
- **How:** Keep shared styles and primitives separate from feature pages. Do not add a custom design system beyond what the shell needs.
- **Done when:** A styled shell renders without compilation errors.

### Step 3: Add the route shell

- **What to do:** Create the initial route structure.
- **Where:** `frontend/app/` or the framework-generated App Router location.
- **How:** Add `/login`, `/dashboard`, `/clients`, `/calendar`, and `/settings` placeholders with a shared layout and navigation.
- **Done when:** Every placeholder route resolves without crashing.

### Step 4: Add loading and error states

- **What to do:** Add route-level loading, error, and not-found UI.
- **Where:** App Router route segments and shared UI components.
- **How:** Show recoverable messages and actions. Ensure status is communicated through text, not color alone.
- **Done when:** Slow or failed route rendering shows an understandable state instead of a blank page.

### Step 5: Add the typed API boundary

- **What to do:** Create a small client module for future FastAPI requests.
- **Where:** Proposed location `frontend/lib/api/`.
- **How:** Read the backend URL from environment configuration and keep request logic out of presentational components.
- **Done when:** The client boundary can be imported by later features without coupling UI components to transport details.

## Interface and Data Contracts

- Frontend runtime location: `frontend/`.
- Backend URL must be configurable through frontend environment settings.
- Initial routes: `/login`, `/dashboard`, `/clients`, `/calendar`, `/settings`.
- The shell must expose accessible navigation and a main content landmark.

## Verification

1. **Command:** Use the repository's documented frontend start command; if not yet documented, mark the command `TBD`.
2. Open each initial route in a browser and confirm it renders.
3. Resize to a narrow viewport and navigate using only the keyboard; confirm focus is visible and route errors show text.

## Acceptance Criteria

- [ ] Next.js App Router frontend starts without compilation errors.
- [ ] React and strict TypeScript checks are enabled.
- [ ] Tailwind CSS is configured and the shell is styled.
- [ ] All five initial routes resolve without crashing.
- [ ] Loading, error, and not-found states are present.
- [ ] Main navigation is keyboard usable and status is communicated with text.

## Out of Scope

- Provider authentication behavior.
- FastAPI integration.
- CopilotKit chat, AG-UI streaming, and LangGraph workflows.
- Client, calendar, and settings feature behavior.

## Notes

The component library is intentionally repository-dependent. Do not invent a second UI library if the frontend repository already has an approved choice.
