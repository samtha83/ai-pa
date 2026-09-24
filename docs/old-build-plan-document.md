# MVP Build and Delivery Plan

## Document Control

- Product: Agentic AI Personal Assistant (AI PA)
- Release: MVP / internal demo
- Status: Draft
- Date: 2026-09-14

## 1. Purpose

This document translates the Product Requirements Document and Architecture Design Document into a phased delivery plan for the MVP. It is structured in Jira-friendly epic format so the team can plan implementation, validation, testing, deployment, and acceptance in clear stages.

This plan is intentionally scoped to the MVP and is designed to support early demo readiness, stakeholder validation, and a clean path to production later.

## 2. Assumptions and Non-Goals

### 2.1 Assumptions

| Area | Assumption |
| --- | --- |
| User type | Primary users are solo service providers with 1:1 client workflows. |
| Business model | MVP is for internal demo and validation, not full production billing or compliance rollout. |
| Data model | Provider and client records are stored locally in the MVP, with a clear path to PostgreSQL later. |
| LLM usage | Azure OpenAI is the production-target model provider, with local/mock AI allowed for early testing. |
| Integrations | Real calendar, CRM, messaging, and spreadsheet integrations are mocked in MVP. |
| Approval model | All write actions require provider review and confirmation. |
| Deployment | MVP runs locally and is intended for rapid iteration and demo usage. |
| Security | Local auth and basic provider scoping are adequate for MVP, not production-grade security. |

### 2.2 Non-Goals

| Area | Non-goal |
| --- | --- |
| Compliance | Full HIPAA, SOC, or enterprise compliance certification is not in scope for MVP. |
| External integrations | Real WhatsApp, Google Calendar, payment providers, and external CRM integrations are not required for MVP. |
| Multi-tenancy | Multi-provider enterprise deployment and complex tenant isolation are out of scope. |
| Autonomous actions | The assistant may not make final actions without provider approval. |
| Billing | Payment processing, subscriptions, and billing workflows are not included. |
| Crisis handling | Emergency escalation or crisis interventions are excluded from the MVP. |
| Scale | Large-volume concurrent usage and enterprise-scale operational requirements are not required. |

## 3. Delivery Principles

- Build the smallest valuable workflow loop first.
- Keep every write action approval-bound.
- Prefer clean architecture over quick hacks.
- Validate each phase with demo-ready acceptance criteria.
- Treat the MVP as a production-like proving ground for workflows, not a final operational system.

## 4. Epic Overview

| Epic | Phase | Goal |
| --- | --- | --- |
| EPIC-01 | Phase 1 | Foundation and app shell |
| EPIC-02 | Phase 2 | Provider onboarding and client setup |
| EPIC-03 | Phase 3 | Session ingestion and summary generation |
| EPIC-04 | Phase 4 | Action plans and task tracking |
| EPIC-05 | Phase 5 | Chat-based retrieval and assistant UX |
| EPIC-06 | Phase 6 | Scheduling, appointments, and daily plans |
| EPIC-07 | Phase 7 | Integration adapters, observability, and demo polish |

## 5. Phase-by-Phase Plan

## Phase 1 — EPIC-01: Foundation and App Shell

### Objective
Establish a runnable local environment and the core app shell for onboarding, navigation, and backend integration.

### Scope
- Frontend skeleton in Next.js + React + TypeScript + Tailwind
- Basic app layout and navigation
- Backend API skeleton in FastAPI
- Database foundation with SQLite
- Basic local auth or mocked session flow
- Health checks and environment configuration

### Jira-style Epic
- Epic: EPIC-01 Foundation and App Shell
- Story grouping:
  - setup app scaffolding
  - create database schema
  - build health endpoints
  - create provider login shell
  - create base UI layout

### Build tasks
- Initialize frontend app and project structure
- Initialize backend API and route scaffolding
- Configure local environment variables and secrets placeholders
- Create SQLite schema and migrations base
- Build initial dashboard shell
- Add error boundary and loading states

### Test tasks
- Smoke test for frontend app boot
- Smoke test for backend health endpoint
- DB connectivity check
- Basic login flow validation

### Deploy tasks
- Local dev deployment to localhost
- Environment configuration for local development

### Validation / Acceptance Criteria
- Frontend loads without crashing
- Backend responds on the health endpoint
- Database is reachable and schema is created
- User can access the base app shell and navigate to core screens

## Phase 2 — EPIC-02: Provider Onboarding and Client Setup

### Objective
Allow a provider to configure preferences, define service rules, and create client records.

### Scope
- Provider profile creation
- Preference setup such as tone, availability, templates, and boundaries
- Client creation and profile editing
- Service type definitions
- Basic provider-specific configuration storage

### Jira-style Epic
- Epic: EPIC-02 Provider Onboarding and Client Setup
- Story grouping:
  - create provider profile
  - save working hours and boundaries
  - create client record flow
  - attach client metadata and goals

### Build tasks
- Build provider onboarding form
- Persist provider preferences to DB
- Build client create/edit pages
- Add time zone, service type, and status fields
- Add validation for required provider profile fields

### Test tasks
- Validate onboarding form completeness
- Validate provider preference persistence
- Validate client create/edit logic
- Validate required field rules

### Deploy tasks
- Local deployment with seeded sample provider data

### Validation / Acceptance Criteria
- A provider can create a profile and save preferences
- A client can be created with required details
- Provider settings can be updated without breaking the app
- The saved provider and client data is retrievable from the backend

## Phase 3 — EPIC-03: Session Ingestion and Summary Generation

### Objective
Allow a provider to upload notes or transcript input and generate a structured summary draft.

### Scope
- Session input creation
- Transcript or text upload flow
- Summary generation workflow
- Review, edit, reject, or approve states
- Audit record of summary approval

### Jira-style Epic
- Epic: EPIC-03 Session Ingestion and Summary Generation
- Story grouping:
  - add session input capture
  - build summary generation workflow
  - add draft review experience
  - create approval actions

### Build tasks
- Create session intake UI and backend route
- Add transcript and notes storage
- Add summary generation service with template selection
- Add evidence markers and uncertainty labels
- Add summary review panel with edit and approve states
- Add audit event logging for summary saves and approvals

### Test tasks
- Test summary generation from sample notes
- Test provider approval and rejection flows
- Test re-generation after edits
- Test audit trail persistence

### Deploy tasks
- Local demo with sample notes and transcript data

### Validation / Acceptance Criteria
- Provider can upload a transcript or note
- System generates a structured summary draft
- Provider can edit and approve the summary
- Approved summary is persisted and traceable in audit records

## Phase 4 — EPIC-04: Action Plans and Task Tracking

### Objective
Turn approved session content into actionable tasks and follow-up plans.

### Scope
- Generate action plans from approved summaries
- Create action items with dates, status, and owners
- Surface overdue or upcoming tasks
- Review and approve action plan before saving

### Jira-style Epic
- Epic: EPIC-04 Action Plans and Task Tracking
- Story grouping:
  - generate action plan draft
  - create action item model
  - create due date and ownership logic
  - surface task status and progress

### Build tasks
- Build action plan service
- Add task schema and status model
- Add action plan review UI
- Add approval button and audit trail
- Surface upcoming and overdue tasks in dashboard

### Test tasks
- Validate action-plan generation from approved summary
- Validate due dates and task states
- Validate provider edits and approvals
- Validate audit logging for task updates

### Deploy tasks
- Demo environment with one sample client and sample task lifecycle

### Validation / Acceptance Criteria
- Action plan can be generated from summary data
- Provider can approve or revise tasks
- Tasks are visible in the client dashboard and dashboard views
- Due dates and statuses are correctly stored

## Phase 5 — EPIC-05: Chat-Based Retrieval and Assistant UX

### Objective
Enable conversational access to key client data and workflow actions using a chat interface.

### Scope
- Chat UI and streaming responses
- Retrieval from provider scope data
- Client summary and task lookup
- Scheduling and daily plan requests through natural language
- Clarification for ambiguous requests

### Jira-style Epic
- Epic: EPIC-05 Chat-Based Retrieval and Assistant UX
- Story grouping:
  - create chat interface
  - wire AG-UI or equivalent event stream
  - implement retrieval intents
  - handle clarification and error states

### Build tasks
- Create chat shell and message history UI
- Connect chat to backend API endpoints
- Add intent routing for retrieve, summarize, plan, and schedule
- Implement retrieval of recent summary and open tasks
- Add ambiguity handling and suggested follow-up prompts
- Add SSE-based incremental responses

### Test tasks
- Validate retrieval for known client records
- Validate missing-data and ambiguity responses
- Validate assistant returns data without exposing unrelated records
- Validate streaming UX behavior

### Deploy tasks
- Local demo with mock data used to validate a few representative prompts

### Validation / Acceptance Criteria
- Provider can ask for a client's latest summary
- Provider can ask for open tasks and upcoming appointments
- System asks clarifying questions when intent is ambiguous
- Chat response is shown incrementally and remains readable

## Phase 6 — EPIC-06: Scheduling, Appointments, and Daily Plans

### Objective
Support scheduling flows, conflict detection, and a personal daily plan.

### Scope
- Local calendar availability logic
- Appointment suggestion and approval flow
- Reschedule/cancel logic
- Daily-plan generation
- Follow-up reminders and prep tasks

### Jira-style Epic
- Epic: EPIC-06 Scheduling, Appointments, and Daily Plans
- Story grouping:
  - build scheduling engine
  - add appointment workflows
  - create daily plan generation
  - create reminder logic

### Build tasks
- Implement availability calculation against working hours and buffers
- Add conflict detection and invalid-slot rejection
- Build appointment suggestion UI and approval flow
- Add daily plan generation based on tasks and appointments
- Add reminder drafts and task preparation prompts

### Test tasks
- Validate no double booking
- Validate timezone handling and slot selection
- Validate booking approval behavior
- Validate daily plan generation against real scheduled data

### Deploy tasks
- Local scheduling demo environment with seeded events and constraints

### Validation / Acceptance Criteria
- Provider can request valid appointment slots
- No conflicting booking is created without approval
- Approved booking is stored and visible in client records
- Daily plan is generated from tasks and calendar content

## Phase 7 — EPIC-07: Integration Adapters, Observability, and Demo Polish

### Objective
Prepare the MVP for stakeholder demos and establish the foundation for production integration without destabilizing the core product.

### Scope
- MCP-backed adapters for external systems
- Observability and logging
- Error and retry handling
- Demo polish and UX finishing
- Security and approval review hardening

### Jira-style Epic
- Epic: EPIC-07 Integration Adapters, Observability, and Demo Polish
- Story grouping:
  - connect MCP tool layer
  - instrument workflows
  - add production-like error handling
  - prepare demo experience

### Build tasks
- Implement mock or MCP adapters for calendar, CRM, messaging, and spreadsheet services
- Add workflow tracing and audit logs
- Add progress states and error banners to the UI
- Add provider approval review screens for sensitive actions
- Improve usability for demo flow and signage

### Test tasks
- Validate tool contract reliability
- Validate logging and trace quality
- Validate approval flow under failure conditions
- Validate end-to-end demo scenario against PRD acceptance criteria

### Deploy tasks
- Local demo deployment with final validation run
- Release checklist and stakeholder demo guide

### Validation / Acceptance Criteria
- Complete end-to-end demo path works without manual backend fixes
- All approval gates work consistently
- Sensitive actions are clearly previewed and logged
- Demonstration flow is stable enough for stakeholder review

## 6. Release Gates

Each phase should have a release gate before moving to the next phase.

### Suggested release gate checklist
- All build tasks completed and merged
- Unit tests and relevant integration tests pass
- Smoke tests pass on local environment
- No critical issues in workflow approval flow
- Demo scenario validated by product or engineering owner
- Risk log reviewed
- Deployment notes written for the next environment

## 7. Definition of Done for Phase Completion

A phase is considered complete only when:

- all planned stories are built and tests pass
- the user journey works end-to-end in the local environment
- the approval model is respected for every sensitive action
- the relevant acceptance criteria are met
- the phase is reviewed by product + engineering
- deployment notes are documented

## 8. Suggested Jira Story Breakdown

Each phase should later be broken into Jira stories with the following structure:

- User story
- Acceptance criteria
- Build notes
- Dev validation checklist
- QA validation checklist
- Deployment notes
- Risks / blockers

Example story template:

- Title: As a provider, I want to approve a summary draft before saving it.
- Acceptance criteria:
  - Summary draft is visible in a review panel
  - Provider can edit and approve the draft
  - Approval records an audit event
  - Unapproved drafts remain in draft state

## 9. MVP Demo Scenario

The following end-to-end scenario should be used as the final MVP validation flow:

1. Provider signs in and configures preferences.
2. Provider creates a client.
3. Provider uploads notes or transcript.
4. Assistant generates a summary draft.
5. Provider reviews and approves the summary.
6. Assistant generates an action plan from the summary.
7. Provider reviews and approves the plan.
8. Provider asks the assistant for open tasks or latest summary.
9. Provider asks for available appointment slots.
10. Provider confirms a slot and creates the appointment.
11. A daily plan is generated from appointments and tasks.
12. All steps are logged and approvals are visible in the audit trail.

## 10. Exit Criteria for MVP

The MVP is ready for internal release when:

- all seven epics are complete or effectively validated
- the end-to-end scenario above works reliably
- sensitive actions require approval and audit logging
- the product is stable for stakeholder demos
- key risks are documented and accepted by the team

## 11. Recommended Next Step

Break this document into Jira epics and stories in the project management tool, starting with:

1. EPIC-01: Foundation and app shell
2. EPIC-02: Provider onboarding and client setup
3. EPIC-03: Session ingestion and summary generation

Once these are built and validated, proceed to scheduling, chat, and integration hardening.
