# Architecture Design Document

## Document Control

- Product: Agentic AI Personal Assistant (AI PA)
- Release: MVP / internal demo
- Status: Draft
- Date: 2026-09-14

## 1. Purpose

This document describes the architecture for the MVP of the AI PA based on the Product Requirements Document. The architecture is designed to validate the core user workflows in a local environment while preserving a clear path to real integrations and production readiness.

The core architectural goal is to enable a provider-facing assistant that can:

- ingest session notes and transcripts,
- generate structured summaries and action plans,
- answer natural-language questions about client context,
- suggest and confirm calendar bookings,
- execute provider-approved actions with complete auditability.

The MVP is intentionally scoped to a local demo, with mock adapters for calendar, messaging, CRM, and spreadsheet operations.

## 2. Scope

### In Scope

- Profile onboarding for providers
- Client record management
- Session summary generation
- Action plan drafting
- Retrieval-based chat assistant
- Local calendar scheduling and conflict detection
- Local storage of provider, client, and session data
- Approval requirement for write actions
- Mock integrations for external systems
- Admin and audit logging

### Out of Scope for MVP

- Production HIPAA or privacy certification
- Real external app integrations
- Multi-tenant enterprise deployment
- Crisis or emergency workflows
- Payment processing and billing systems
- Large-scale multi-user operations

## 3. Architectural Principles

1. Provider-controlled autonomy
   - The system should act as a supervised assistant, not an autonomous decision-maker.
   - Sensitive actions require provider approval.

2. Human-in-the-loop review
   - Draft summaries, task lists, scheduling options, and messages are editable before saving or sending.

3. Local-first MVP
   - All functionality must run locally for demo usage and faster iteration.

4. Modular but simple
   - Keep a clear separation between UI, API, orchestrator, domain services, adapters, and storage.

5. Explainability and traceability
   - Every AI-generated artifact must show provenance, source inputs, and approval state.

6. Extensibility
   - The system should support later connection to Google Calendar, CRM tools, messaging APIs, and spreadsheets with minimal structural changes.

## 4. System Overview

The application is organized as a layered, modular system:

- Frontend UI for provider interaction and chat
- API layer for business operations
- Agent/orchestration layer that coordinates AI workflows
- Domain services for summaries, plans, reminders, and scheduling
- Data access layer for local persistence
- Integration adapters for mock external systems
- Audit and security layer for authorization and action history

The general model is:

User -> Frontend -> Backend API -> Agent Orchestrator -> Domain Services -> Persistence / External Adapters

### 4.1 System Context Diagram

```text
Provider / User
      |
      v
[Next.js + React + Tailwind UI]
      |
      | HTTPS / SSE / AG-UI events
      v
[FastAPI API / Auth / Policy Layer]
      |
      +--> [LangGraph Agent Workflows]
      |        |--> Summary generation
      |        |--> Action plans
      |        |--> Scheduling
      |        |--> Retrieval + daily planning
      |
      +--> [MCP Tool Gateway]
                 |--> Calendar
                 |--> CRM
                 |--> Messaging
                 |--> Spreadsheets
                 |--> Research / knowledge sources

      +--> [Azure OpenAI]
      +--> [SQLite / Postgres + Vector DB + Object Storage]
```

## 5. High-Level Architecture

```text
┌──────────────────────────────────────────────────────────────┐
│                         Frontend Layer                        │
│  Chat UI  | Provider Onboarding | Client Dashboard           │
│  Summary Review Panel | Calendar View | Daily Plan View      │
└───────────────────────────────┬──────────────────────────────┘
                                │ HTTP / WebSocket
                                ▼
┌──────────────────────────────────────────────────────────────┐
│                         API Layer                             │
│  FastAPI endpoints for auth, clients, sessions, tasks,       │
│  scheduling, research, audit                                   │
└───────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────┐
│                    Agent Orchestration Layer                   │
│  LangGraph / workflow orchestration                            │
│  Request routing, state management, tool execution            │
└───────────────┬───────────────────────────────────────────────┘
                │
      ┌─────────┼─────────┬──────────────┐
      ▼         ▼         ▼              ▼
┌──────────┐ ┌──────────┐ ┌────────────┐ ┌──────────────┐
│ Summary  │ │ Action   │ │ Scheduling│ │ Research    │
│ Service  │ │ Plan     │ │ Service    │ │ Service     │
└────┬─────┘ └────┬─────┘ └────┬──────┘ └────┬────────┘
     │          │            │               │
     └──────────┴────────────┴───────────────┴──────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────┐
│                    Persistence Layer                           │
│  SQLite DB + File Storage + Vector Index (optional)          │
└───────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────┐
│                  Integration Adapters / Mock Systems           │
│  Calendar Adapter | Messaging Adapter | CRM Adapter          │
│  Spreadsheet Adapter | Research Source Adapter               │
└──────────────────────────────────────────────────────────────┘
```

## 6. Components

### 6.0 Component Responsibilities

- Frontend: user experience, chat, dashboards, review flows, and approvals.
- API layer: auth, validation, provider access, workflow entrypoints, and backend policy enforcement.
- Agent orchestration: stateful workflow control, tool routing, summarization, retrieval, and approval checkpoints.
- Domain services: business logic for scheduling, summarization, action plans, reminders, research, and daily planning.
- MCP tool gateway: stable integration boundary for external systems and provider tools.
- Persistence layer: structured records, approvals, audit history, and vector retrieval data.
- External services: Azure OpenAI and real external integrations such as calendar, CRM, messaging, and research systems.

### 6.1 Frontend Layer

The frontend provides a chat-first interface for providers and a review workflow for generated outputs.

Responsibilities:

- Provider onboarding and configuration
- Client list and detail screens
- Session input upload or note capture
- Summary and action plan review pages
- Chat-based assistant interactions
- Daily plan and calendar views
- Approval and audit panels

Suggested stack:

- A2UI or equivalent modern UI framework for dynamic AI-assisted screens
- Local client-side state with API integration
- Role-based UI states for draft, approved, rejected, and processing

Key UX patterns:

- Show generated content in a side-by-side review panel
- Require explicit approval for writes and sends
- Show source evidence behind every summary or recommendation

### 6.2 API Layer

The backend exposes REST endpoints for provider and assistant operations. This layer is the system's integration boundary between the UI and the orchestration logic.

Responsibilities:

- Authentication and session management
- Validation of provider and client access
- Routing of requests to orchestration workflows
- Enforcement of write approval rules
- Returning structured JSON and status metadata

Core resources:

- Providers
- Clients
- Sessions / notes
- Summaries
- Action plans
- Appointments
- Tasks
- Messages
- Research sources
- Audit logs

### 6.3 Agent Orchestration Layer

This layer coordinates AI workflows using a graph-based or stateful orchestration model. The main responsibilities include:

- collecting necessary context,
- calling task-specific services,
- validating data before writes,
- capturing user approval state,
- returning output in a structured format.

Suggested technology:

- LangGraph for orchestration and state management
- LangChain or equivalent prompt and retrieval utilities
- LLM connector for provider-specific synthesis and reasoning

Primary flows:

1. Summary-generation workflow
2. Action-plan workflow
3. Client-context retrieval workflow
4. Scheduling workflow
5. Daily planning workflow

### 6.4 Domain Services

These are the business logic services that encapsulate specific use cases.

#### Summary Service

- Accepts transcript, audio metadata, or notes
- Applies provider template rules
- Identifies themes, actions, and unresolved items
- Returns a draft summary with evidence and confidence markers

#### Action Plan Service

- Converts approved summary into tasks
- Applies service-specific structures
- Produces due dates, owners, follow-up actions, and statuses

#### Scheduling Service

- Evaluates availability against provider slots and client timezone
- Detects conflicts and suggests alternatives
- Validates booking preconditions before creating an appointment

#### Research Service

- Pulls from curated sources
- Generates a brief with attribution
- Flags unsupported or uncertain claims

#### Reminder Service

- Detects upcoming events and missing follow-ups
- Creates reminder drafts and checklists

#### Daily Planning Service

- Builds a schedule from meetings, tasks, and provider preferences
- Balances workload and personal time blocks

### 6.5 Data Layer

#### Relational data store

Use SQLite in the MVP for speed and simplicity.

Core tables include:

- providers
- provider_preferences
- clients
- service_types
- sessions
- session_inputs
- session_summaries
- action_plans
- action_items
- appointments
- tasks
- message_drafts
- research_sources
- audit_events

#### File storage

Store raw inputs separately from generated artifacts:

- audio files
- transcripts
- notes and uploaded documents
- generated drafts and exported artifacts

#### Vector store (optional)

Use a local vector database such as Chroma or FAISS for:

- prior session summaries
- provider style samples
- research source documents
- templates and historical examples

This supports better retrieval but is optional for the first pass.

## 7. Workflow Design

### 7.1 Provider Onboarding Workflow

1. Provider registers or signs in.
2. Provider enters profile, modality, preferred tone, and working rules.
3. Provider defines templates, working hours, and message boundaries.
4. The system saves profile and configuration.
5. System displays enabled actions and approval requirements.

### 7.2 Session Summary Workflow

1. Provider selects a client and a session.
2. System accepts transcript or note input.
3. Orchestrator gathers client context and provider profile.
4. Summary service generates a draft.
5. System labels assumptions, missing data, and unresolved ambiguity.
6. Provider reviews and approves or edits.
7. System stores approved content and audit record.

### 7.3 Action Plan Workflow

1. Approved summary is passed to action-plan service.
2. Service generates tasks and due dates.
3. Provider reviews and approves.
4. Action plan is saved to the client record and surfaced in the dashboard.

### 7.4 Chat Retrieval Workflow

1. User asks a natural-language question.
2. Router identifies intent and required data.
3. Retrieval layer queries provider-allowed record sets.
4. Model prepares summary with source references.
5. System returns brief, contextual answer.

### 7.5 Scheduling Workflow

1. User asks for available slots.
2. Scheduling service checks provider calendar and service duration.
3. It rejects conflict and returns valid options.
4. Provider selects a slot.
5. System creates an appointment record and drafts confirmation text.
6. Confirmation is sent only after approval.

## 8. Security and Trust Architecture

### Core principles

- Identity and authorization are provider-scoped.
- AI execution is supervised and observable.
- No write action happens without explicit provider confirmation.

### Security controls

- Local authentication for MVP
- Authorization checks on every client read and update
- Audit log for every summary generation, save, approval, booking, and message preview
- Redaction rules for sensitive data in debug logs
- Explicit denials for unsupported actions such as emergency guidance or unapproved external sends

### Trust layers

- Source-backed answer generation
- Uncertainty labeling in summaries
- Human review before write operations
- Optional action preview before external communication

## 9. Data Model

### Entities

#### Provider

- id
- name
- business_name
- timezone
- tone
- service_type
- created_at

#### ProviderPreference

- provider_id
- working_hours
- buffers
- blackout_dates
- default_template
- message_boundaries
- allowed_actions
- prohibited_actions

#### Client

- id
- provider_id
- name
- contact_info
- timezone
- status
- goals
- created_at

#### SessionInput

- id
- client_id
- source_type
- raw_file_path
- transcript_text
- created_at
- status

#### SessionSummary

- id
- client_id
- provider_id
- source_input_id
- content
- template_type
- version
- status
- approved_by
- approved_at

#### ActionPlan

- id
- client_id
- provider_id
- summary_id
- status
- created_at
- approved_by
- approved_at

#### ActionItem

- id
- action_plan_id
- title
- description
- owner
- due_date
- status

#### Appointment

- id
- client_id
- provider_id
- start_time
- end_time
- status
- timezone
- source

#### AuditEvent

- id
- provider_id
- entity_type
- entity_id
- action
- actor
- timestamp
- metadata

## 10. API Design

### Authentication

- POST /api/auth/login
- POST /api/auth/logout

### Providers

- GET /api/providers/me
- PUT /api/providers/me/preferences

### Clients

- GET /api/clients
- GET /api/clients/{id}
- POST /api/clients
- PUT /api/clients/{id}

### Sessions

- POST /api/clients/{id}/sessions
- GET /api/clients/{id}/sessions
- POST /api/sessions/{id}/summarize
- POST /api/summaries/{id}/approve

### Action Plans

- POST /api/clients/{id}/action-plans
- GET /api/clients/{id}/action-plans
- POST /api/action-plans/{id}/approve

### Scheduling

- GET /api/calendar/availability
- POST /api/appointments/suggest
- POST /api/appointments
- POST /api/appointments/{id}/confirm

### Chat

- POST /api/chat/message
- GET /api/chat/history

### Audit

- GET /api/audit

## 11. Technology Stack

### Frontend

- Next.js App Router
- React + TypeScript
- Tailwind CSS
- Component library for forms, chat, table, modal, and review states
- CopilotKit-style conversational experience for assistant workflows

### Conversational UI / Agent Protocol

- AG-UI for structured agent events and streaming state updates
- Server-Sent Events for incremental visible assistant responses
- Event-driven UI states for tool execution, approval, and results

### Backend

- Python
- FastAPI with Uvicorn
- Pydantic for request/response schemas
- Async endpoints for chat, orchestration, and workflow execution

### Agent / AI Layer

- LangGraph for stateful workflows and task orchestration
- LangChain or equivalent retrieval/prompt utilities
- Azure OpenAI as the model provider for summarization, planning, and retrieval-grounded answers

### Tool / Integration Layer

- MCP services using streamable HTTP for structured external capabilities
- Adapters for calendar, messaging, spreadsheet, research, and CRM tools
- Standardized tool contracts to prevent direct ad hoc integrations in the UI or agent logic

### Database

- SQLite for the MVP and local development
- Target production database: PostgreSQL for transactional data and audit history

### Vector / Retrieval

- Local vector DB for MVP (for example Chroma or FAISS)
- Target production vector store: managed vector database or Postgres with pgvector depending on scale and controls

### Storage

- Local file system for MVP uploads and generated artifacts
- Production target: object storage for transcripts, notes, and generated files

### Streaming / Async

- SSE for incremental responses and workflow progress
- Background task processing for summary generation, reminder pipelines, and scheduled jobs

### Integration Adapters

- Calendar adapter: Microsoft / Google calendar integration through MCP
- Messaging adapter: outbound message drafts and send workflows
- Spreadsheet adapter: CSV/Sheets sync or structured data export
- CRM adapter: structured client and session sync
- Research adapter: curated sources and citation-aware content retrieval

## 12. Deployment Architecture

### Local MVP deployment

All components run on a single developer machine or local environment.

Components:

- Frontend served on localhost
- Backend served on localhost:8000
- SQLite database on local disk
- Local file storage for uploads
- Optional vector store stored locally

### Deployment topology

```text
Developer Laptop
├─ Frontend App
├─ FastAPI Backend
├─ SQLite DB
├─ Local File Storage
├─ Vector Store (optional)
└─ LLM API Connection (if external provider is used)
```

This architecture is designed for demonstration and iteration, not production-grade hosting.

## 13. MVP to Production

This section defines the migration path from the local MVP to a production-grade product while preserving the same user-centered principles. The goal is to keep the core workflow intact while replacing mock systems with real capabilities and adding operational controls.

### 13.1 Key Guardrails and Guidelines

1. Keep the UI and tool execution separate
   - The frontend should render state and user intent; it should not directly call external tools or enforce business logic.
   - Tool execution, approvals, and external writes must be routed through backend services and policy checks.

2. Enforce write approval at the backend
   - A UI-level confirm is not enough.
   - All create, update, send, or booking actions should be validated by backend permission checks, provider-scoped authorization, and audit logging.

3. Treat agent actions as supervised workflows
   - Summary generation, message drafts, scheduling suggestions, and task generation should all operate in reviewable states.
   - Final writes require provider confirmation and should leave a clear change history.

4. Design tool integrations behind an MCP gateway
   - External systems should not be embedded directly into the LangGraph node logic.
   - Wrap them in standard tool adapters with explicit contracts, retries, and permission scopes.

5. Keep the model output evidence-backed
   - Summaries and guidance should cite or reference source inputs when possible.
   - The UI should show uncertainty, missing data, and approved vs draft states.

6. Use SQLite only for MVP
   - SQLite is fine for local development and demo workloads.
   - Production data should move to PostgreSQL for concurrency, backups, migrations, auditability, and operational reliability.

7. Use SSE and AG-UI for streaming, but keep workflow state authoritative server-side
   - UI streaming should be for experience and progress, not as the system of record.
   - The server should remain the source of truth for workflow state.

8. Add privacy and data controls before exposing real client data
   - Provider-scoped access controls, encryption at rest, audit trails, retention policies, and sensitive logging safeguards are required before production data use.

9. Separate orchestration from business logic
   - LangGraph orchestrates tasks and state transitions.
   - Domain services implement schedule validation, summary generation, action-plan logic, and client rules.

10. Plan for operations and cost monitoring early
    - Instrument the app for latency, token usage, retries, tool failures, and approval rates.
    - This is especially important when Azure OpenAI and external integrations are added.

### 13.2 Recommended Production Target Architecture

The production target should preserve the same application concepts while replacing local mocks with secure service boundaries and operational infrastructure.

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                              Frontend (Next.js)                              │
│  App Router | React | TypeScript | Tailwind | Component Library             │
│  Chat UI + Dashboard + Client Detail + Calendar + Review Panels             │
│  AG-UI event stream + SSE for streaming responses                           │
└───────────────────────────────┬──────────────────────────────────────────────┘
                                │ HTTPS / WebSocket / SSE
                                ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                            API / Application Layer                           │
│  FastAPI + Uvicorn                                                          │
│  Auth, provider RBAC, client records, audit API, workflow endpoints          │
│  Approval enforcement, validation, policy checks                             │
└───────────────────────────────┬──────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                        Agent Orchestration Layer (LangGraph)                 │
│  Summary workflow | Action plan workflow | Scheduling workflow               │
│  Retrieval workflow | Daily plan workflow | approval checkpoints             │
│  Workflow state, retries, tool orchestration                                 │
└───────────────┬──────────────────────────────────────────────┬────────────────┘
                │                                              │
                ▼                                              ▼
┌───────────────────────────────┐               ┌───────────────────────────────┐
│      Domain Services          │               │       MCP Tool Gateway        │
│  - Summary Service            │               │  - Calendar MCP               │
│  - Scheduling Service        │               │  - CRM MCP                    │
│  - Action Plan Service       │               │  - Messaging MCP              │
│  - Research Service          │               │  - Spreadsheet MCP            │
│  - Reminder / Daily Plan     │               │  - Search / Knowledge MCP    │
└───────────────┬───────────────┘               └───────────────┬───────────────┘
                │                                               │
                ▼                                               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                      Persistence and Retrieval Layer                          │
│  PostgreSQL (transactional data + audit + approvals)                         │
│  Vector DB (knowledge, provider examples, historical summaries)             │
│  Object Storage for documents, session files, transcripts                    │
│  Cache/Queue (optional for async follow-up jobs)                             │
└───────────────────────────────┬──────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                            External AI & Services                             │
│  Azure OpenAI for reasoning and generation                                   │
│  Calendar / CRM / Messaging / Research providers via MCP                     │
│  Security and observability layers (logs, tracing, metrics, alerts)          │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 13.3 Production Migration Path

1. Replace local mocks with MCP-backed tool adapters
   - Keep the tool interface stable while swapping providers behind the adapter.

2. Move from SQLite to PostgreSQL
   - Keep schema migrations explicit and versioned.
   - Add provider auth, approvals, and audit history as first-class operational tables.

3. Add production-grade auth and RBAC
   - Provider-specific roles and permission scopes for reading and writing client data.

4. Add operational observability
   - Trace every workflow step from user intent to tool call and save.
   - Monitor latency, token consumption, approval rates, and tool failures.

5. Add event-driven background jobs
   - Follow-ups, reminders, daily plan generation, and scheduled automation should run through job workers instead of blocking user requests.

6. Add environment-specific deployment patterns
   - local dev, staging, and production environments with isolated configs and secrets management.

7. Expand privacy and retention controls
   - provider-specific retention windows, deletion workflows, anonymization options, and audit review processes.

### 13.4 MVP to Production Migration Checklist

- [ ] Replace mock calendar, CRM, messaging, and spreadsheet adapters with MCP-backed adapters.
- [ ] Move from SQLite to PostgreSQL for transactional business data and audit tables.
- [ ] Add provider RBAC and permission scopes for every client and workflow action.
- [ ] Enforce backend-level write approvals for appointment creation, messages, and record updates.
- [ ] Add structured tracing for user actions, tool calls, workflow state, and LLM calls.
- [ ] Introduce async job workers for reminders, summaries, and daily planning tasks.
- [ ] Add environment configuration for local, staging, and production deployments.
- [ ] Introduce encryption at rest, secret management, and sensitive log redaction.
- [ ] Add data retention, deletion, and privacy controls for client records.
- [ ] Add evaluation tests for summary quality, schedule conflict detection, and retrieval accuracy.
- [ ] Add cost monitoring and rate limits for Azure OpenAI usage.
- [ ] Define a provider onboarding and data consent workflow before real client data is used.

### 13.5 Why this production target is a good fit

This production architecture preserves the strengths of the MVP:

- a chat-first workflow that feels natural,
- structured AI-generated output with human approval,
- a modular backend that can absorb more integrations,
- a clean separation between product experience and tool execution,
- a practical path from internal demo to real business workflows.

The critical point is that the architecture stays consistent: the UI remains a thin product layer, the agent remains orchestrated, and external systems remain behind stable, policy-aware adapters.

## 14. Non-Functional Requirements Mapping

### Performance

- Chat retrieval responses should be fast and lightweight.
- Summarization should show immediate processing state while running.
- Use background task execution for long-running operations.

### Reliability

- Avoid write operations without explicit approval.
- Validate all scheduling conflicts before booking.
- Use transactional database writes for core state changes.

### Maintainability

- Separate domain services from API endpoints.
- Use clear request/response schemas.
- Keep integration adapters behind interface boundaries.

### Observability

- Log request IDs and workflow execution steps.
- Record summary generation, approval, booking, and messaging actions in the audit log.
- Surface error states to the UI without exposing raw sensitive content.

## 15. Risks and Mitigations

| Risk | Architectural Response |
| --- | --- |
| AI hallucination in summaries | Use source-aware generation, uncertainty labels, and provider approval |
| Unsafe autonomous actions | Enforce write approval gate and tool permission checks |
| Data leakage across providers | Add provider-scoped access checks and local data isolation |
| Poor agent orchestration quality | Use explicit workflow states and modular service boundaries |
| Excessive complexity in MVP | Keep integrations mocked and local-first, reduce scope |
| Hard-to-debug workflows | Add audit logs, trace IDs, and visible processing states |

## 16. Sequence Example: Session Summary Generation

```text
Provider -> Frontend: Upload transcript / notes
Frontend -> API: POST /sessions/{id}/summarize
API -> Orchestrator: Start summary workflow
Orchestrator -> Summary Service: Build draft summary
Summary Service -> Data Layer: Fetch client context + provider settings
Summary Service -> LLM: Generate structured draft
LLM -> Summary Service: Draft output + uncertainties
Summary Service -> API: Draft summary response
API -> Frontend: Display review panel
Provider -> Frontend: Review and approve
Frontend -> API: POST /summaries/{id}/approve
API -> Data Layer: Save approved summary + audit event
```

## 17. Sequence Example: Booking Appointment

```text
Provider -> Frontend: Ask for available time slots
Frontend -> API: GET /calendar/availability
API -> Scheduling Service: Evaluate conflicts
Scheduling Service -> Data Layer: Read provider calendar + sessions
Scheduling Service -> API: Valid slots list
API -> Frontend: Show options
Provider -> Frontend: Select slot and confirm
Frontend -> API: POST /appointments
API -> Scheduling Service: Validate final booking
API -> Data Layer: Save appointment record
API -> Frontend: Show booking confirmation
```

## 18. Architecture Decisions Summary

1. Local-first monolith with modular services
   - Keeps MVP easy to run and debug.

2. Approval-based execution model
   - Protects trust and reduces risk.

3. SQLite + local file storage
   - Fits the demo scope and reduces setup noise.

4. Mock integrations as a first step
   - Allows validation of interaction patterns without external dependencies.

5. LangGraph-centered orchestration
   - Keeps workflows explicit and understandable.

6. Clear audit trail for all writes
   - Required for trust, safety, and product readiness.

## 19. Open Technical Decisions

- Should the frontend be A2UI-native or a standard web app shell with a chat panel?
- Should the orchestration layer be graph-based for all flows or only for the LLM-heavy ones?
- Is a lightweight vector store necessary for the first internal demo?
- Should app-level approval be enforced in the API or UI only?
- What level of encryption is acceptable for local demo data before moving to regulated environments?

## 20. Recommended MVP Build Order

### Milestone 1: Foundation

- Project scaffolding
- Provider sign-in
- Provider profile and preferences
- SQLite schema
- Local file storage

### Milestone 2: Core assistant workflows

- Client creation and session upload
- Summary generation and approval
- Action plan generation and review
- Basic chat retrieval

### Milestone 3: Scheduling and daily ops

- Local calendar logic
- Appointment suggestions and approval
- Daily plan generation
- Message preview flows

### Milestone 4: Demo polish

- Audit dashboard
- Review/edit states
- Error handling and recovery
- UX refinements for demo quality

## 21. Conclusion

This architecture delivers the MVP in the simplest reliable form: a local, provider-centered, agentic assistant with explicit approval gates, modular workflows, and mock integrations. It gives product and engineering a solid path from a working demo to more realistic external integrations without redesigning the system.

The architecture is intentionally constrained so the team can validate the most important user outcomes first: reduce admin load, improve follow-through, and make provider control explicit and trustworthy.
