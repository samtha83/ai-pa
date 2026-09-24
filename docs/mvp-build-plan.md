# MVP Build Plan

## Document Control

- Product: Agentic AI Personal Assistant (AI PA)
- Release: Local MVP / internal demonstration
- Status: Draft
- Date: 2026-09-21
- Source: Product Requirements Document and Architecture Design Document

## 1. Goal

Build the smallest version of the AI PA that proves the product core end-to-end in a local demo environment while keeping the implementation open for future scale.

The MVP must be able to demonstrate:

1. provider onboarding,
2. client creation and notes intake,
3. session summary generation and approval,
4. action plan generation,
5. chat-based retrieval,
6. mock scheduling with conflict prevention,
7. provider approval checkpoints for writes,
8. local persistence and audit history,
9. research from approved sources via simple MCP tooling.

This plan is intentionally narrow and implementation-first. It avoids features that are not needed for the first working demo.

## 2. Build Principles

- Start with the smallest working workflow loop and do not build ahead of the need.
- Put every write behind explicit provider approval.
- Keep the frontend and backend in separate runtime units.
- Use SQLite and local files for the MVP, not a production-grade stack.
- Keep LangGraph, AG-UI, and MCP boundaries clean so the system can evolve later.
- Prefer deterministic domain logic for scheduling and validation instead of letting the model make final write decisions.
- Keep all records provider-scoped and audit every meaningful action.

## 3. Scope of the MVP

### Included

- local auth for a demo provider,
- provider profile + preferences,
- client records,
- session input capture,
- summary drafting and approval,
- action plan generation,
- chat retrieval and intent routing,
- mock scheduling and conflict checks,
- approval-gated appointment creation,
- research from approved sources using mock MCP tools,
- audit log and basic observability.

### Excluded from the first build

- real external calendar or messaging integrations,
- production compliance work,
- multi-provider enterprise features,
- payment or billing flows,
- multilingual or complex workflow personalization beyond core preferences,
- advanced vector search or complex retrieval tuning,
- autoscaling, queue workers, distributed systems, or production deployment.

## 4. Delivery Strategy

The MVP is delivered in six phases. Each phase ends with a runnable demo slice and a visible product result.

| Phase | Objective | Primary deliverable | Exit gate |
| --- | --- | --- | --- |
| Phase 1 | Local runtime foundation | runnable frontend + backend + SQLite | app boots with demo auth |
| Phase 2 | Provider and client data foundation | provider onboarding and client records | provider can create and save data |
| Phase 3 | Session summary workflow | notes intake + summary draft + approval | summary is generated and approved |
| Phase 4 | Action plan + chat retrieval | task plan + chat flow | client context and plan are retrievable |
| Phase 5 | Scheduling + daily plan | slot search and appointment approval | mock booking works without conflicts |
| Phase 6 | Research + demo polish | mock research + audit + final refinements | internal demo is ready |

## 5. Phase-by-Phase Build Plan

## Phase 1: Local Runtime Foundation

### Objective

Get the project into a working local state with both app layers running and a safe developer workflow.

### Work items

1. Create repo structure
   - frontend/
   - backend/
   - docs/
   - data/
   - .env.example
   - .gitignore

2. Initialize frontend stack
   - Next.js App Router
   - React + TypeScript
   - Tailwind CSS
   - routing shell
   - loading/error states

3. Initialize backend stack
   - FastAPI
   - Uvicorn
   - Pydantic settings
   - versioned `/api/v1` routes
   - basic middleware and structured error responses

4. Add SQLite layer
   - provider tables
   - session tables
   - migration support
   - database connection + readiness checks

5. Add demo auth
   - local provider session
   - login + logout + current-user route
   - protected route handling

6. Add startup docs
   - install commands
   - environment setup
   - local run instructions

### Acceptance criteria

- frontend boots successfully,
- backend health endpoint works,
- SQLite connection is healthy,
- local demo login succeeds,
- route shell renders for dashboard and placeholder pages,
- missing config produces clear developer guidance,
- README explains the local run flow.

### Exit gate

The team can start both services locally and reach an authenticated app shell.

---

## Phase 2: Provider and Client Data Foundation

### Objective

Add the data and screens needed for provider setup and client management. This is the operational foundation for all later workflows.

### Work items

1. Provider profile model
   - name
   - business name
   - timezone
   - tone
   - modality/service type
   - template settings
   - boundaries

2. Provider preferences model
   - working hours
   - session duration
   - buffer time
   - blackout dates
   - max sessions/day
   - summary template choice

3. Client model
   - name
   - contact info
   - timezone
   - service type
   - goals
   - status
   - provider ownership

4. UI screens
   - provider onboarding form
   - provider settings page
   - client Create/Edit page
   - client detail page

5. API routes
   - provider read/write APIs
   - client list/create/update APIs
   - client detail lookup

6. Repository layer
   - provider repository
   - client repository
   - preference repository
   - scoped queries by provider

### Acceptance criteria

- provider can create and save profile and preference data,
- client can be created and edited,
- data is scoped to the signed-in provider,
- server validation rejects invalid or incomplete profile data,
- UI shows saved values after reload or refresh.

### Exit gate

The provider can configure the base profile and create at least one client record.

---

## Phase 3: Session Summary Workflow

### Objective

Allow a provider to attach notes or transcripts and generate a structured, reviewable summary draft.

### Work items

1. Session input model
   - client id
   - input type
   - file reference or raw text
   - created timestamp
   - processing status
   - checksum or reference metadata

2. Notes upload and capture flow
   - text note entry
   - transcript file upload
   - save input with provider scope
   - display status in UI

3. Summary generation flow
   - provider template selection
   - structured draft generation
   - source support markers
   - uncertainty / missing info labeling

4. Review and approval workflow
   - draft display panel
   - edit summary
   - regenerate summary
   - approve / reject / save draft states
   - audit event on approval

5. Persistence layer
   - summary records
   - status transitions
   - approved summary versions
   - traceability to session input

6. Backend orchestration
   - LangGraph summary node
   - approval checkpoint
   - resume on approval/rejection

### Acceptance criteria

- provider can attach rough notes or transcript content,
- summary draft is generated from the provider's template,
- generated summary distinguishes facts vs inference vs missing info,
- provider can edit, regenerate, reject, or approve,
- approved summary is saved and visible in the client detail screen,
- approval is recorded in the audit log.

### Exit gate

A provider can create a session input and produce an approved summary tied to a client.

---

## Phase 4: Action Plan + Chat Retrieval

### Objective

Turn approved summary content into actionable follow-up work and give the provider a conversational way to retrieve client info.

### Work items

1. Action plan model
   - client id
   - summary reference
   - draft/approved/rejected status
   - action items

2. Action item model
   - title
   - description
   - owner
   - due date
   - follow-up date
   - status

3. Action plan generation
   - create action plan from approved summary
   - generate task list
   - allow editing before approval

4. Chat retrieval workflow
   - chat shell and message list
   - assistant request endpoint
   - natural-language intent routing
   - retrieve latest summary / open tasks / next appointment

5. Clarification flow
   - ask for missing client or date if ambiguous
   - do not guess a client record

6. UI review panel
   - show final answer with source references
   - show record references and audit state when relevant

### Acceptance criteria

- provider can generate an action plan and approve it,
- each task has required fields and timestamps,
- chat can answer a basic request like “show me Jane’s latest summary and open tasks,”
- ambiguous requests trigger a clarification question,
- failed lookups are explicit rather than made-up.

### Exit gate

The provider can get a client summary and open tasks via chat and can turn approved summary content into an action plan.

---

## Phase 5: Scheduling and Daily Plan

### Objective

Create the mock scheduling loop and confirm the core product story around appointment booking and day planning.

### Work items

1. Availability rules
   - working hours
   - service duration
   - buffer time
   - blackout dates
   - timezone handling
   - existing appointments

2. Scheduling service
   - find free slots
   - reject overlaps and duplicates
   - return valid alternatives

3. Appointment model
   - client id
   - start/end
   - timezone
   - status
   - creation audit

4. Booking approval flow
   - propose options
   - present approval gate
   - execute approved booking
   - record audit event

5. Daily plan generation
   - read appointments + tasks
   - generate time-blocked plan
   - allow provider review and save if approved

6. Mock calendar MCP service
   - list events
   - find availability
   - create appointment
   - reject conflicts

### Acceptance criteria

- scheduling logic rejects overlapping or invalid slots,
- mock appointment is created only after approval,
- rejected or conflicting options show explicit reasons,
- daily plan can be generated from appointments and tasks,
- provider can review and approve the plan before saving.

### Exit gate

The core scheduling and daily-plan story works in demo mode without external integrations.

---

## Phase 6: Research + Demo Polish + Hardening

### Objective

Finish the demo experience and make the MVP look and behave like a believable internal product demo.

### Work items

1. Research workflow via MCP
   - approved source catalog
   - research request flow
   - source-linked output
   - distinguish retrieved facts vs recommendations

2. Message preview flow
   - draft appointment confirmation or follow-up message
   - preview-only in the MVP
   - no external sending

3. Observability and tracing
   - LangSmith traces
   - structured logs
   - correlation IDs
   - error visibility for run failures

4. Audit and governance
   - approval logs
   - write action history
   - provider-scoped resource access checks
   - final review of data protections

5. Demo data and seeded workflows
   - seeded provider
   - sample client
   - sample notes
   - ready-to-run summary and scheduling flows

6. Final UX polish
   - loading and empty states
   - accessible keyboard focus
   - visible status communication
   - consistent review panels

### Acceptance criteria

- research from approved sources works in mock mode,
- message previews are visible and do not send externally,
- the app demonstrates the end-to-end product narrative,
- errors are visible and recoverable,
- audit trail is present for all save and approval actions.

### Exit gate

The internal demo can be run end-to-end without external services.

## 6. Sequencing Notes

The build must follow this order to avoid rework:

1. runtime and auth,
2. provider and client data,
3. session summary generation,
4. action plans + retrieval chat,
5. scheduling + day plan,
6. research + demo polish.

This order prevents building scheduling or research workflows before the shared provider/client and summary primitives exist.

## 7. Definition of Done for MVP

The MVP is done when all of the following are true:

- the app starts locally for a developer,
- a provider can onboard and create a client,
- notes can be captured and turned into an approved summary,
- an action plan can be generated and approved,
- chat can retrieve a client’s latest summary and open tasks,
- scheduling returns valid slots and rejects conflicts,
- appointment creation requires explicit confirmation,
- the app uses provider-scoped access and audit logging,
- research and messaging flows are mock-only and preview-based,
- the demo can be run successfully end-to-end in one local environment.

## 8. Risks and Mitigations

### Risk: Overbuilding the first version

Mitigation: Keep the MVP limited to one provider, one local demo environment, and a single happy-path flow for each major use case.

### Risk: Model-driven writes without approval

Mitigation: All write and external actions require a LangGraph approval checkpoint and a backend validation gate.

### Risk: Scheduling logic becoming non-deterministic

Mitigation: Keep calendar conflict checks in deterministic service code, not in the LLM.

### Risk: UI drifting away from concept

Mitigation: Use one chat-first UX with clear review panels and approval actions instead of multiple divergent screens.

### Risk: Broken integration boundaries

Mitigation: Keep AG-UI, LangGraph, MCP, and repository boundaries explicit from the start.

## 9. Recommended Implementation Order

1. Build foundation and auth.
2. Build provider and client models and APIs.
3. Build session input + summary generation + approval.
4. Build action plan + chat retrieval.
5. Build scheduling + appointment approval + daily plan.
6. Add research + preview messaging + polish.

This is the correct path to an MVP that is both simple enough to build and strong enough to demonstrate the business value.
