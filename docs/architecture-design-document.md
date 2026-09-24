# Architecture Design Document

## Agentic AI Personal Assistant MVP

## Document Control

- Product: Agentic AI Personal Assistant (AI PA)
- Document type: Architecture Design Document (ADD)
- Release: Local MVP / internal demonstration
- Status: Draft
- Date: 2026-09-18
- Source requirements: `docs/product-requirements-document.md`

## 1. Purpose

This document defines the smallest architecture that can demonstrate the core AI PA workflow while preserving clear extension points for production integrations and higher scale later.

The MVP must allow a provider to:

1. configure a provider profile and availability,
2. create a client and attach rough session notes,
3. generate and review a structured session-summary draft,
4. approve the summary and generate an action plan,
5. retrieve client context through chat, and
6. find and approve a mock appointment without creating conflicts.
7. connect to internet using simple mcp to do research when user wants to research from approved sites
The architecture treats the assistant as a supervised operator. Reading may be automatic; generated drafts require review; writes and external actions require explicit approval.

## 2. Scope and Non-Goals

### 2.1 In scope

- One local provider account for the demo, with provider-scoped data access.
- Next.js App Router frontend with TypeScript, Tailwind CSS, and a component library.
- CopilotKit-style chat experience for message history, composer, and rendered assistant state.
- AG-UI-compatible structured events streamed over HTTP/SSE.
- FastAPI backend served by Uvicorn.
- LangGraph workflows for chat routing, summarization, action plans, retrieval, and scheduling.
- Azure OpenAI as the first LLM provider, behind a replaceable model adapter.
- SQLite persistence and local file storage.
- Mock calendar, messaging, CRM, spreadsheet, and research services exposed through MCP servers using streamable HTTP.
- Audit events, approval checkpoints, retries, and LangSmith tracing.

### 2.2 Out of scope

- Real external calendar, CRM, messaging, payment, or spreadsheet integrations.
- Production HIPAA, SOC, or other compliance certification.
- Multi-provider administration, organization billing, and enterprise tenancy.
- Autonomous clinical decisions, diagnosis, crisis response, or emergency communication.
- Audio transcription, unless represented by a pre-created mock transcript.
- Background job infrastructure, distributed workers, and high-concurrency deployment.

## 3. Architecture Drivers

The following requirements control the design:

| Driver | Architectural consequence |
| --- | --- |
| Provider approval for writes | LangGraph interrupt/checkpoint before persistence or external-action tools; backend revalidates approval. |
| Source-supported summaries | Session input is stored separately from generated content; generated fields carry source references and uncertainty labels. |
| Deterministic scheduling | Availability and conflict checks are ordinary domain logic, not an LLM decision. |
| Structured streaming | Agent progress is emitted as AG-UI events over an SSE response. |
| Local demo simplicity | SQLite, local files, one FastAPI process, and mock MCP services are sufficient. |
| Replaceable integrations | MCP clients and domain ports isolate the graph from calendar, CRM, messaging, and research implementations. |
| Recoverability | Checkpoints and explicit workflow states allow retry without repeating an approved write. |
| Privacy | Provider scope is applied in API, graph context, tool arguments, and repositories; raw session content is excluded from ordinary logs. |

## 4. Quality Attribute Targets

For the MVP:

- Retrieval requests should return an initial streamed event within the local demo target of three seconds, excluding model latency.
- Scheduling conflict checks must be deterministic and reject duplicate or overlapping appointments.
- No write or external-action tool may execute without a valid approval decision for the current workflow instance.
- A failed workflow must leave existing records unchanged unless the specific write was already approved and successfully committed.
- Primary workflows must be keyboard usable and must communicate state with text, not color alone.
If something is:

approved,
rejected,
pending,
failed,
unavailable,
or requires attention,
that status must be shown in text, labels, or icons with text, not only by changing color.

For example:

“Approved” text is required, not just green
“Rejected” text is required, not just red
“Needs review” should be visible as text
“Conflict detected” should be labeled in text, not only a red highlight

These are demo targets, not production availability or compliance commitments.

## 5. System Context

```text
Provider
   |
   v
Next.js App Router / React / CopilotKit-style UI
   |
   | HTTPS POST + AG-UI events over SSE
   v
FastAPI application
   |-- authentication, authorization, validation
   |-- AG-UI event adapter and SSE response
   |-- REST resources for screens and approval commands
   v
LangGraph assistant workflows
   |-- route request -> gather context -> plan -> draft -> approval -> execute
   |-- checkpoints and retries
   |
   |---- Azure OpenAI model adapter
   |---- MCP clients over streamable HTTP
   |         |-- mock calendar
   |         |-- mock messaging
   |         |-- mock CRM/spreadsheet
   |         |-- mock research sources
   |
   |---- domain services and repositories
             |-- SQLite
             |-- local session-input files
             |-- LangGraph checkpoint storage
             |-- LangSmith traces
```

The browser never calls the LLM, database, or MCP services directly. FastAPI is the trust boundary and the only backend entry point used by the frontend.

## 6. Container Architecture

### 6.1 Frontend container

**Technology:** Next.js App Router, React, TypeScript, Tailwind CSS, and the repository-selected component library.

**Responsibilities:**

- Render the provider shell, chat, client context, review panels, calendar, tasks, and onboarding forms.
- Maintain transient chat and UI state.
- Consume AG-UI lifecycle, text, tool, state, approval, and error events.
- Send approval decisions and ordinary resource mutations to FastAPI.
- Display source inputs, draft status, planned actions, and audit history.

The frontend does not decide whether an action is permitted. Disabled controls improve UX, but FastAPI and the graph enforce the rule.

### 6.2 FastAPI application container

**Technology:** Python, FastAPI, Pydantic, and Uvicorn.

**Responsibilities:**

- Local authentication and provider identity resolution.
- Provider-scoped authorization and request validation.
- REST endpoints for resource screens and workflow commands.
- POST endpoint that starts or resumes an assistant run.
- Translation of LangGraph events into AG-UI events and SSE frames.
- Approval validation, idempotency checks, and transaction boundaries.
- Safe error responses without exposing prompts, secrets, or raw sensitive content.

FastAPI owns transport and policy. It does not contain prompt-specific orchestration logic.

### 6.3 LangGraph orchestration container

LangGraph owns stateful workflow execution. The graph receives a normalized request and a provider identity, then produces assistant events and a final workflow state.

The graph may call the model for interpretation and drafting, but deterministic domain services own authorization, scheduling, persistence, and state transitions.

### 6.4 MCP integration containers

MCP services expose stable tool contracts over streamable HTTP. The MVP uses local mock implementations with seeded data.

Initial MCP service boundaries:

- `calendar`: list events, find available slots, create/reschedule/cancel appointment.
- `messaging`: render a provider-branded message preview; never sends externally.
- `records`: read and update mock CRM/spreadsheet records after approval.
- `research`: read curated mock sources and return source metadata.

MCP tools are not granted unrestricted database access. Each tool receives a provider-scoped context and validates its own input.

### 6.5 Persistence containers

- **SQLite:** providers, preferences, clients, session inputs, summaries, action plans, tasks, appointments, message drafts, and audit events.
- **Local file storage:** original text or transcript files, referenced by a stored relative path and checksum. Files are outside the SQLite row payload.
- **LangGraph checkpoint store:** SQLite-backed checkpoint tables in the MVP, using the same local database only if the selected checkpointer supports safe table separation.
- **Vector retrieval:** not required for the first vertical slice. Add a provider-scoped vector index only when templates or approved history cannot be handled by ordinary SQLite queries.

## 7. Request and Streaming Model

### 7.1 Assistant request

The frontend sends a request containing:

```json
{
  "thread_id": "thread-123",
  "message": "Show me Maya's latest summary and open tasks",
  "client_id": null,
  "approval": null
}
```

FastAPI adds the authenticated `provider_id`, validates the request, creates an execution context, and invokes the graph.

### 7.2 SSE and AG-UI events

The response is `text/event-stream`. Each frame contains a serialized AG-UI event appropriate to the selected AG-UI version. The adapter must preserve event ordering and include the workflow/thread identifier.

The minimum event vocabulary is:

- run started and run finished,
- assistant text delta,
- state or structured-result update,
- tool call started, tool result, and tool error,
- approval requested,
- workflow error.

The UI renders text incrementally but uses structured state events for review panels, tool activity, approval controls, and final records. It must not infer approval state from assistant prose.

### 7.3 Resume after approval

When the graph reaches an approval checkpoint, it emits `approval_requested` and persists the checkpoint. The frontend submits an approval command containing the thread/run identifier, requested action identifier, decision, and an idempotency key. FastAPI verifies:

1. the signed-in provider owns the workflow,
2. the requested action is still pending,
3. the approval has not expired or already been consumed, and
4. the idempotency key has not been used for a different action.

The graph then resumes from the checkpoint. Rejecting an action ends or returns the workflow to an editable draft state without executing the write.

## 8. LangGraph Design

### 8.1 Shared state

The graph state is intentionally small and serializable:

```text
AssistantState
  provider_id
  thread_id
  request
  intent
  entities                 # client/date/service/action references
  retrieved_context        # provider-scoped records and source ids
  draft                    # summary, plan, message, or slot proposal
  pending_action           # action type, payload hash, approval status
  tool_events
  errors
  response_status
```

Raw session content should be referenced by record or file identifier where possible rather than copied into every checkpoint.

### 8.2 Graph nodes

```text
START
  -> normalize_request
  -> classify_intent
  -> gather_context
  -> route_workflow

route_workflow
  -> retrieve_context
  -> create_summary_draft
  -> create_action_plan_draft
  -> find_slots
  -> create_daily_plan_draft
  -> unsupported_or_clarify

draft_or_result
  -> validate_draft
  -> approval_gate (for draft/write/external actions)
  -> execute_approved_action
  -> persist_result
  -> respond
  -> END
```

The actual implementation may use subgraphs for summary, action-plan, and scheduling workflows. The first build should keep one assistant graph with typed routing and extract subgraphs only when a workflow has independent tests or checkpoint needs.

### 8.3 Deterministic boundaries

- `classify_intent` may use the model, but unsupported intents are rejected by an allowlist.
- `retrieve_context` applies provider and client authorization through repositories.
- `find_slots` calls deterministic availability logic; the model may explain options but cannot invent them.
- `approval_gate` is mandatory for saving summaries, saving action plans, booking appointments, changing statuses, and external-action previews.
- `execute_approved_action` verifies the action payload hash before writing.
- `persist_result` uses a transaction and records an audit event in the same transaction where practical.

### 8.4 Initial workflow behavior

#### Retrieve client context

Resolve the client, clarify ambiguous names, query the latest approved summary and open tasks, and return source-linked results. Retrieval does not require approval.

#### Create session summary

Load the original session input and provider template, generate a draft with supported facts, inferences, missing fields, and source references, then pause for review. Only an approval command can persist the summary as approved.

#### Create action plan

Use an approved summary or explicit provider instructions, produce editable action items, validate dates and owners, then pause before saving or sharing.

#### Find or book appointment

Use provider availability, buffers, blackout dates, time zones, existing events, and service duration to compute slots. Present options without writing. A selected slot enters an approval checkpoint; booking rechecks conflicts inside the write transaction.

#### Daily plan

Read appointments and tasks, produce a draft time-blocked plan, identify conflicts, and require approval before saving it as the provider's plan.

## 9. Domain Model

The MVP stores the following core entities. All records include `provider_id`, timestamps, and a stable identifier unless noted otherwise.

| Entity | Important fields | State / constraint |
| --- | --- | --- |
| Provider | name, business name, time zone | local authenticated owner |
| ProviderPreference | tone, service type, template, boundaries, availability rules | one active preference set for MVP |
| Client | name, contact, time zone, service type, goals, status | provider-scoped |
| SessionInput | client id, kind, file path or text, checksum, processing status | original input is immutable |
| SessionSummary | session input id, structured content, sources, uncertainties | draft/approved/rejected/superseded |
| ActionPlan | client id, summary id, content | draft/approved/rejected |
| ActionItem | plan id, title, owner, due date, follow-up date, status | task status changes are audited |
| Appointment | client id, start/end, time zone, status, external ref | overlap check required |
| MessageDraft | client id, channel, body, source refs | preview only in MVP |
| AuditEvent | actor, action, entity, decision, payload hash, timestamp | no raw session content |

Use explicit status fields and optimistic version columns for mutable records. Do not represent approval only as a boolean; retain who, when, decision, and the version approved.

## 10. API Surface

The exact route names may evolve, but the first implementation should provide these boundaries:

| Route | Purpose |
| --- | --- |
| `GET /health` | process and dependency health |
| `GET/PUT /api/provider` | provider profile and preferences |
| `GET/POST/PUT /api/clients` | client records |
| `POST /api/clients/{id}/session-inputs` | create text or transcript input |
| `GET /api/clients/{id}/context` | summary, tasks, and appointments |
| `POST /api/assistant/runs` | start a chat/workflow run and stream AG-UI SSE |
| `POST /api/assistant/runs/{run_id}/approval` | approve or reject a pending action and resume |
| `GET /api/appointments/availability` | deterministic slot lookup |
| `GET/POST /api/audit-events` | read audit history; writes are internal |

Resource routes support screens and direct manipulation. Assistant runs are the primary conversational entry point. Both paths use the same domain services and authorization rules.

## 11. Security and Privacy

### MVP controls

- Use a local demo login/session and resolve one provider identity per request.
- Require `provider_id` in repository queries; never trust a client-supplied provider identifier.
- Validate client ownership before reading session inputs, summaries, tasks, or appointments.
- Keep secrets in environment variables and never send them to the browser or MCP tools.
- Redact or omit raw notes, transcripts, and prompt contents from ordinary application logs.
- Store local input files in an application-controlled directory with generated names.
- Treat uploaded filenames and text as untrusted input.
- Log tool name, record identifiers, result status, and payload hash, not sensitive bodies.
- Return generic internal errors to the frontend while retaining correlation IDs for diagnosis.

### Explicit MVP limitation

This local system is demonstration software. It must not be used for real regulated client data. Production deployment requires a dedicated threat model, stronger identity, encryption and key management, tenant isolation, retention/deletion controls, vendor review, and compliance work.

## 12. Observability and Operations

LangSmith traces each assistant run, graph node, model call, tool call, latency, token usage, and error using a correlation ID. Sensitive content must be filtered or disabled in traces according to the local privacy configuration.

Application logs use structured fields:

- request ID, thread ID, run ID, provider ID,
- route and graph node,
- event type and duration,
- tool name and outcome,
- error category.

The MVP health check verifies the FastAPI process and SQLite connectivity. MCP and Azure OpenAI connectivity are reported separately so a degraded integration is visible rather than mistaken for a database failure.

## 13. Failure Handling

| Failure | Behavior |
| --- | --- |
| Ambiguous client | Ask one concise clarification; do not query or write against a guessed client. |
| Missing source data | Return an explicit missing-data result; do not fabricate a summary. |
| Model timeout or invalid structured output | Emit an error event, keep existing records unchanged, and allow retry. |
| MCP unavailable | Show the integration as unavailable; read local data where possible; do not claim success. |
| Approval rejected | Persist the decision/audit event, leave the target record unchanged, and return to review or end. |
| Conflict detected during booking | Reject the write and return fresh alternatives; never silently move the appointment. |
| Client disconnects during stream | Keep the checkpoint for resumable work; do not execute a pending write solely because the stream ended. |
| Duplicate approval request | Return the existing result for the same idempotency key; do not repeat the write. |

## 14. Deployment and Local Runtime

The first runtime uses separate local processes:

```text
Next.js dev server       localhost:3000
FastAPI/Uvicorn          localhost:8000
Mock MCP services        localhost:8100+ (one port per service or one gateway)
SQLite + files           local application data directory
Azure OpenAI             configured remote endpoint
LangSmith                optional remote observability endpoint
```

Use a checked-in environment example with placeholders for Azure OpenAI and LangSmith settings. The application must start with mock/local modes when those remote credentials are absent, so UI and deterministic workflow tests do not require a live model.

## 15. Testing Strategy

### Unit tests

- provider-scoped repository queries,
- availability, buffers, time zones, blackout dates, and overlap detection,
- approval state transitions and idempotency,
- Pydantic request/event schemas,
- prompt-output parsing and uncertainty labeling.

### Graph tests

- one test per supported intent,
- clarification for ambiguous clients,
- checkpoint and resume after approval,
- rejection and retry behavior,
- no tool call for unsupported or prohibited requests.

### API tests

- auth and provider isolation,
- SSE event ordering and terminal events,
- approval endpoint authorization,
- transaction rollback on failed writes.

### Frontend tests

- chat renders streamed text and structured state,
- approval controls are available only for pending actions,
- review panels display draft versus approved state,
- keyboard navigation and error/loading states.

### Acceptance scenarios

Run the PRD demo path end to end: onboard provider, create client, attach notes, generate and approve summary, generate action plan, retrieve context, find slots, reject a conflict, and approve one appointment. Include a test that proves an unapproved appointment is not created.

## 16. Scalability Path

The MVP should not introduce infrastructure before it is needed, but the boundaries must support these later changes:

| MVP choice | Later evolution |
| --- | --- |
| SQLite repositories | PostgreSQL with migrations and row-level tenant controls |
| Local files | Object storage with signed URLs and retention policies |
| In-process FastAPI graph run | Queue-backed workers and run resumption service |
| SQLite checkpointer | Durable checkpoint database with cleanup and retention |
| Mock MCP services | Real MCP services with OAuth, rate limits, and circuit breakers |
| One provider demo auth | OIDC/session service and organization membership |
| SSE | SSE remains valid for one-way streaming; add WebSocket only for a proven bidirectional need |
| Optional simple retrieval | Provider-scoped vector/search service with evaluation and re-indexing |
| Single app deployment | Independently deployable frontend, API, graph worker, and MCP services |

The frontend should depend on event contracts and resource schemas rather than LangGraph internals. The graph should depend on domain ports rather than SQLite or a specific MCP implementation. Those two seams provide the main scale-out leverage.

## 17. Decisions and Open Questions

### Decisions for the MVP

- Azure OpenAI is the initial model provider; model access is wrapped behind a small adapter.
- SQLite is the initial structured store; PostgreSQL is the intended later migration target.
- SSE is the transport for AG-UI events.
- LangGraph checkpoints are required before approval-bound writes.
- Calendar conflict detection is deterministic domain code.
- MCP mock services use streamable HTTP to exercise the future integration boundary.
- The first vertical slice does not require vector search, audio transcription, or real external integrations.

### Open questions to resolve during implementation

- Which component library is already approved by the frontend repository?
- Which AG-UI package/version and event schema will be adopted?
- Should the local demo use a single MCP gateway process or one process per mock service?
- Which LangGraph checkpointer is compatible with the chosen SQLite migration setup?
- Which Azure OpenAI deployment and structured-output model should be used?
- How much content may be retained in LangSmith traces during local testing?

## 18. Build-Plan Implications

The ADD should translate into the following smallest implementation sequence:

1. Establish the monorepo/runtime shape, environment configuration, FastAPI health route, Next.js shell, SQLite migrations, and local auth.
2. Implement provider, preference, client, session-input, summary, task, appointment, and audit repositories with provider scoping.
3. Build the deterministic scheduling service and mock calendar MCP service before connecting model-driven booking.
4. Build the LangGraph state, intent allowlist, retrieval workflow, summary draft workflow, and approval checkpoint.
5. Add the AG-UI event adapter and SSE endpoint, then connect the CopilotKit-style chat and review panels.
6. Add action-plan generation, appointment approval/resume, and audit display.
7. Add LangSmith tracing, failure/retry tests, seeded demo data, and the complete acceptance scenario.

Each step should leave the application runnable. Real integrations, vector retrieval, background workers, and production authentication remain follow-on work rather than prerequisites for proving the MVP.