# Feature: Frontend App Shell

- **EPIC:** EPIC-01
- **Feature ID:** 05
- **Status:** Not Started
- **Source spec:** context/features/phase1-spec.md

## Goal

Build a responsive, accessible Next.js shell with a local login screen, protected placeholder routes, navigation, session status, loading states, and recoverable errors.

## Why This Matters

The shell gives every later workflow a consistent place to live and lets stakeholders experience the MVP as one application rather than disconnected pages.

## Prerequisites

- Feature 01 frontend setup is available.
- Feature 02 exposes the backend API.
- Feature 04 exposes the local session flow.
- The frontend styling conventions are established before adding new UI libraries.

## Implementation Steps

### Step 1: Create the root layout

- **What to do:** Add the shared document layout and main content landmark.
- **Where:** `frontend/app/layout.tsx` and shared styles/components.
- **How:** Add semantic page structure, global styles, a consistent content width, and responsive behavior without putting business workflows in the layout.
- **Done when:** All app routes share the same document structure and keyboard users can reach the main content.

### Step 2: Add the login page

- **What to do:** Create the local demo login form.
- **Where:** `frontend/app/login/page.tsx`.
- **How:** Add labeled fields, submit state, accessible error text, and a visible development-only label. Use the typed API client rather than calling fetch directly from unrelated components.
- **Done when:** The page renders without a session and shows a useful response for success or failure.

### Step 3: Add protected placeholder routes

- **What to do:** Create dashboard and future-workflow route placeholders.
- **Where:** `frontend/app/dashboard/page.tsx`, `frontend/app/clients/page.tsx`, `frontend/app/calendar/page.tsx`, and `frontend/app/settings/page.tsx`.
- **How:** Add clear page headings and state that the workflows are coming in later epics. Do not imply that placeholder screens implement clients or scheduling.
- **Done when:** Each route loads directly for an authenticated user without crashing.

### Step 4: Build shared navigation and session status

- **What to do:** Add navigation links and logout control.
- **Where:** `frontend/components/app-shell/` or the selected shared component directory.
- **How:** Link Dashboard, Clients, Calendar, and Settings. Display the current provider name/session state and provide a keyboard-accessible logout action.
- **Done when:** Users can navigate between all shell routes and return to login after logout.

### Step 5: Add loading, error, and not-found states

- **What to do:** Make route and API failures visible and recoverable.
- **Where:** Next.js route-level `loading.tsx`, `error.tsx`, and `not-found.tsx` files.
- **How:** Show a progress/status message during loading, a retry or return-to-dashboard action for errors, and a useful not-found response. Do not rely on color alone.
- **Done when:** Delayed or failed route data does not produce a blank page.

### Step 6: Add the typed API client and route protection

- **What to do:** Centralize backend calls and protect authenticated routes.
- **Where:** `frontend/lib/api-client.ts` and the chosen session guard/provider.
- **How:** Define typed functions for login, logout, and current-user lookup. Handle unauthorized responses by redirecting to `/login` and keep credentials/session transport consistent with the backend.
- **Done when:** Protected pages cannot be used without a valid backend session.

### Step 7: Check responsive accessibility

- **What to do:** Verify the shell works at desktop and narrow widths.
- **Where:** Shared layout and components.
- **How:** Use semantic headings, visible focus states, labels, keyboard navigation, and status announcements where needed. Test without relying on color alone.
- **Done when:** Navigation and primary actions remain usable at narrow viewport widths and with keyboard input.

## Interface and Data Contracts

- Routes: `/login`, `/dashboard`, `/clients`, `/calendar`, `/settings`.
- The frontend uses the backend auth endpoints rather than storing provider identity as client-controlled state.
- Placeholder routes must clearly distinguish unavailable future functionality.

## Verification

1. Open `/login`, submit the demo credential, and confirm navigation to `/dashboard`.
2. Visit every protected route and confirm it renders for an authenticated session.
3. Clear the session and visit a protected route; confirm redirect to `/login`.
4. Trigger an API/route failure and confirm a retry or return action appears.
5. Test keyboard navigation and a narrow viewport manually or with a browser smoke test.

## Acceptance Criteria

- [ ] Frontend renders `/login` without compilation errors.
- [ ] Successful login reaches `/dashboard` and shows session/provider state.
- [ ] Dashboard, Clients, Calendar, and Settings navigation works.
- [ ] Unauthenticated users cannot access protected placeholders.
- [ ] Loading, error, and not-found states are visible and recoverable.
- [ ] Shell is responsive and keyboard usable.

## Out of Scope

- Full dashboard widgets or client management.
- Summary review, action plans, calendar logic, chat, or external integrations.
- Production visual design system decisions beyond the Phase 1 shell.

## Notes

Follow the architecture guidance that the frontend renders state and intent while backend services enforce identity and business rules.
