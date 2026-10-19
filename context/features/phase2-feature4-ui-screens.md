# Feature: UI Screens

- **Phase:** Phase 2: Provider and Client Data Foundation
- **Feature ID:** phase2-feature4
- **Status:** Completed
- **Source plan:** docs/mvp-build-plan.md

## Goal

Add the core frontend screens needed for provider setup and client management so the local MVP can create and review provider and client data through the UI.

## Non-Goals

- Full application styling overhaul.
- Complex workflow dashboards or production-ready data tables.
- Phase 3 summary generation or scheduling UX.

## Why This Matters

A working MVP needs explicit, reviewable screens to create and edit provider and client data. Without this layer, the backend data model would exist but the provider would have no path to use it in a demo.

## Prerequisites

- Frontend app shell from Phase 1 must be present.
- Backend provider and client APIs must be available.
- Demo auth routes should allow a protected frontend session.

## Technical Solution

Build the minimal UI surfaces for provider onboarding and client management in the Next.js app. Add provider settings and client create/edit/detail screens using the existing App Router shell and typed API library. Keep each screen focused on the data needed for the local demo and use simple forms and validation states rather than a broader design system or component architecture.

The UI should support provider-scoped actions, list data, show saved values after reload, and gracefully handle empty or failed API states without breaking the app shell.

## Implementation Steps

### Step 1: Add provider settings screens

- **What to do:** Add a provider onboarding or settings screen that loads the current provider profile and allows updates.
- **Where:** `frontend/app/` and frontend feature directories.
- **How:** Build a simple form for `name`, `business_name`, and `timezone`, bind it to the backend provider API, and handle loading and save states.
- **Done when:** A provider can view and update their profile and the UI reflects saved values.

### Step 2: Add client creation and list view

- **What to do:** Add screens for listing and creating clients.
- **Where:** `frontend/app/clients/` and related components.
- **How:** Create a client list page, a create form, and a basic detail or summary panel. Use provider-scoped API calls and empty-state handling.
- **Done when:** A provider can create at least one client record from the app and see it appear in the client list.

### Step 3: Add client detail pages

- **What to do:** Add a detail view for individual client records.
- **Where:** `frontend/app/clients/[id]/` or equivalent routing.
- **How:** Fetch the client by ID and display core fields, editing controls, and status. Keep the UI simple and review-oriented.
- **Done when:** The provider can open a client detail page and see their saved profile details and status values.

## Interface and Data Contracts

- The frontend consumes provider and client REST endpoints from the backend.
- Forms align to the provider and client validation schema definitions.
- UI actions are scoped to the authenticated provider.
- Loading, error, and empty states are explicit for all list and detail views.

## Verification

1. Run `cd frontend && npm run build` after implementing the screens.
2. Start the app locally and confirm a provider can create a client from the UI.
3. Refresh the page and verify saved values remain available after reload.

## Acceptance Criteria

- [x] Provider onboarding/settings UI exists and saves profile data.
- [x] A provider can create and view client records from the frontend.
- [x] The UI reflects saved values after reload.
- [x] Empty/error states are explicit and do not block the app shell.

## Out of Scope

- Advanced dashboard layout and analytics.
- Multi-provider roles or admin permissions.
- Scheduling and client summary workflows from later phases.

## Notes

This feature focuses on the minimal UX needed to prove provider and client data entry in the local demo. It should remain simple enough to support the next workflow phases without redesign.

The provider profile screen uses authenticated `GET` and `PATCH /api/v1/providers/me` endpoints added for this feature. The app shell reads its browser session after hydration and refreshes its displayed provider name after profile updates.
