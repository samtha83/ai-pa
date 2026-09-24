# EPIC-01 | Phase 1 | Foundation and App Shell

### JIRA #

EPIC-01

### Problem Statement

The AI PA has product and architecture requirements but does not yet have a
runnable application foundation. Without a consistent frontend shell, backend
boundary, local persistence setup, environment configuration, and basic session
flow, the later provider, client, summary, scheduling, and chat features cannot
be developed or demonstrated as one product.

Phase 1 establishes the smallest vertical foundation for the local MVP. It must
prove that the frontend can start, reach the FastAPI backend, persist data in
SQLite, and render a provider-facing shell with clear loading and error states.

### Goals / Non-Goals

#### Goals

- Create a reproducible local development setup for the Next.js frontend and
	FastAPI backend.
- Establish the frontend application shell with a persistent layout, primary
	navigation, route placeholders, loading states, and an error boundary.
- Establish the backend API boundary, versioned route organization, health
	checks, CORS configuration, and structured error responses.
- Establish SQLite connectivity, the initial migration mechanism, and the
	provider-scoped persistence foundation required by later epics.
- Provide a local demo authentication/session flow without pretending to be
	production authentication.
- Define stable contracts that later epics can extend without coupling UI code
	directly to the database or agent services.
- Make the application runnable with documented commands and environment
	variables.

#### Non-goals

- Provider onboarding form behavior or preference management; those belong to
	EPIC-02.
- Client creation, session ingestion, summaries, action plans, scheduling, or
	chat workflows.
- LangGraph workflows, LLM calls, vector search, MCP tools, or real external
	integrations.
- Production authentication, multi-user identity management, RBAC, or regulated
	data compliance.
- A complete dashboard experience. Phase 1 provides the shell and route
	placeholders only.

### Proposed Solution

Build a local-first application with two independently runnable services:

```text
ai-pa/
	frontend/                 Next.js App Router, React, TypeScript, Tailwind
	backend/                  FastAPI application and domain boundary
	backend/migrations/       Versioned SQLite migrations
	data/                     Local runtime data, ignored by git
	.env.example              Documented non-secret defaults
```

The frontend uses a shared app shell for all authenticated routes. The shell
contains a top bar, navigation, page content area, and an explicit session
state. Initial routes are:

- `/login` - local demo sign-in form.
- `/dashboard` - foundation dashboard placeholder.
- `/clients` - placeholder for EPIC-02 and later client workflows.
- `/calendar` - placeholder for later scheduling workflows.
- `/settings` - placeholder for provider preferences.

The backend exposes a versioned API under `/api/v1` and keeps persistence and
policy checks behind service/repository boundaries. The initial API surface is:

- `GET /api/v1/health` - process health and application version.
- `GET /api/v1/ready` - readiness check including SQLite connectivity.
- `POST /api/v1/auth/login` - local demo login; returns a session and provider
	identity.
- `POST /api/v1/auth/logout` - clears the local demo session.
- `GET /api/v1/auth/me` - returns the current provider session.

The demo session uses a seeded local provider or a clearly labeled development
credential. It is isolated behind an auth service so it can later be replaced
by real authentication without changing feature routes. Future client-facing
queries and writes receive provider identity from this boundary rather than
accepting an arbitrary provider ID from the browser.

### Acceptance Criteria

#### Application startup

- A new developer can follow the README to install dependencies and start the
	frontend and backend locally.
- The frontend starts without compilation errors and renders `/login`.
- The backend starts without import or configuration errors and exposes API
	documentation in the local development environment.
- Missing optional environment values produce a useful configuration error or
	documented local default; secrets are not committed.

#### Frontend shell

- A successful local login navigates to `/dashboard` and displays the current
	provider name or session state.
- The shell provides navigation links for Dashboard, Clients, Calendar, and
	Settings; each link resolves to its placeholder route without crashing.
- The shell has a stable responsive layout for desktop and narrow viewport
	widths.
- Initial route loading displays a loading state rather than a blank page.
- A route or API failure displays a recoverable error state with a retry or
	return-to-dashboard action.
- Unauthenticated access to protected placeholder routes redirects to `/login`.

#### Backend and persistence

- `GET /api/v1/health` returns HTTP 200 with service status and version.
- `GET /api/v1/ready` returns HTTP 200 when SQLite is reachable and HTTP 503
	when the readiness dependency is unavailable.
- The first local startup creates the SQLite database and applies migrations
	without manual SQL execution.
- The initial schema contains the provider/session foundation and records
	created-at timestamps. It does not store raw session content or credentials
	in logs.
- Login, current-session lookup, and logout have automated API tests.
- Protected routes reject requests without a valid local session.

#### Quality and delivery

- Frontend and backend have automated smoke checks for boot, health/readiness,
	database connectivity, and the basic login flow.
- A CI check runs formatting/linting and the focused frontend/backend tests.
- The README documents setup, environment variables, startup commands, test
	commands, local data location, and the deliberately non-production nature of
	the demo auth flow.

### Technical Possible Solution

#### Feature #1: Repository and local runtime setup

**Scope:** Create the frontend/backend structure, shared documentation, local
environment configuration, and developer commands.

**Tasks:**

- Initialize Next.js App Router with React, TypeScript, and Tailwind CSS.
- Initialize FastAPI with Uvicorn, Pydantic settings, and a `/api/v1` router.
- Add `.env.example` files or one documented root environment contract for
	frontend URL, backend URL, SQLite path, application environment, and session
	secret placeholder.
- Add gitignore rules for local databases, uploads, build artifacts, caches,
	and environment files containing secrets.
- Document one-command or clearly sequenced local startup for both services.

#### Feature #2: Backend foundation

**Scope:** Establish API composition, configuration, middleware, error
handling, and health/readiness routes.

**Tasks:**

- Create `app/main.py` for FastAPI application construction.
- Create separate modules for settings, API routers, auth/session service,
	database session management, and shared response/error models.
- Configure CORS from an allowlist containing the local frontend origin.
- Return consistent JSON errors with a machine-readable code and human-readable
	message; do not expose stack traces in API responses.
- Add request correlation IDs to responses and use structured logs that exclude
	raw client/session content.
- Keep agent orchestration and external adapters out of this phase.

#### Feature #3: SQLite and migration foundation

**Scope:** Create the first persistent schema and a replaceable data-access
boundary.

**Tasks:**

- Use SQLite for local MVP persistence, with SQLAlchemy models and Alembic
	migrations unless the repository standardizes on an equivalent migration
	tool before implementation.
- Add a `providers` table with `id`, `name`, `business_name`, `timezone`,
	`created_at`, and `updated_at`.
- Add a `demo_sessions` table with session identifier, provider ID, expiry,
	created-at, and revoked-at fields. Store only a hash or opaque identifier,
	never a plaintext credential.
- Add foreign keys, indexes for provider/session lookup, and UTC timestamps.
- Provide an application startup/readiness database check and a test database
	fixture that does not modify developer data.
- Keep raw uploaded files and generated artifacts out of SQLite for now; the
	file-storage boundary will be introduced when session ingestion starts.

#### Feature #4: Local demo authentication

**Scope:** Provide enough authentication to protect the shell during local
development while preserving a production replacement point.

**Tasks:**

- Seed one clearly identified local provider on development initialization.
- Implement login, logout, and current-user endpoints through an auth service.
- Use an HTTP-only cookie or equivalent server-validated session transport;
	avoid trusting provider identity supplied by the client.
- Add an auth dependency for protected API routes and a frontend session
	provider/loader for protected pages.
- Show a clear development-only label in the login UI and documentation.

#### Feature #5: Frontend app shell

**Scope:** Build the shared layout and route placeholders required to begin
future feature work.

**Tasks:**

- Create a root layout with accessible navigation, provider/session status,
	logout action, and main content landmark.
- Add `/login`, `/dashboard`, `/clients`, `/calendar`, and `/settings` routes.
- Add route-level loading and error UI, plus a not-found page.
- Add a small typed API client for backend calls; keep fetch logic out of
	presentational components.
- Add accessible focus states, keyboard navigation, form labels, and status
	messages that do not rely on color alone.
- Keep placeholder pages intentionally minimal and label deferred workflows so
	they are not mistaken for implemented functionality.

#### Feature #6: Validation and CI

**Scope:** Make the foundation verifiable on every change.

**Tasks:**

- Add backend tests for health, readiness, database initialization, login,
	session lookup, logout, and unauthorized access.
- Add frontend tests for login rendering, protected-route behavior, navigation,
	and loading/error states where the chosen test stack supports them.
- Add a browser smoke test for login followed by navigation to each shell route
	if the local CI environment supports it.
- Add CI jobs for dependency installation, backend checks, frontend lint/type
	checks, and focused tests.

### Dependencies

- Node.js and the repository-supported package manager for the Next.js app.
- Python 3.11+ (or the version selected by the repository) and the repository
	package manager for FastAPI dependencies.
- FastAPI, Uvicorn, Pydantic settings, SQLAlchemy, and Alembic or equivalent
	migration tooling.
- SQLite, available locally without a separate database service.
- Frontend component/styling conventions established by the selected Next.js
	starter; do not introduce a second UI framework in this epic.
- A CI runner capable of running frontend and backend checks.
- EPIC-02 depends on the route, provider identity, database, and API contracts
	delivered here. EPIC-01 does not depend on an LLM provider, LangGraph,
	Azure OpenAI, MCP server, or external calendar/messaging system.