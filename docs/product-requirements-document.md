# Product Requirements Document

## Product

**Working name:** Agentic AI Personal Assistant (AI PA)

**Document status:** Draft for product and engineering alignment

**Date:** 2026-09-14

**Primary release:** Local MVP / internal demonstration

## 1. Executive Summary

The AI PA is a chat-first operational assistant for independent 1:1 service providers. It brings together client context, session documentation, scheduling, follow-up tasks, research, and day planning so providers can spend more time with clients and less time moving information between tools.

The assistant learns a provider's service modality, personal brand, preferred templates, availability rules, and communication boundaries. It can retrieve information and prepare changes across connected systems, but the MVP requires provider approval before saving sensitive summaries, sending client-facing messages, or making bookings.

The initial product serves two representative users:

- **Jane:** a tech-comfortable therapist or coach who needs faster session documentation and consistent follow-up.
- **Meera:** a less tech-savvy independent service provider who needs simple scheduling, messaging, and spreadsheet tracking.

## 2. Problem Statement

Independent providers lose time and attention to fragmented administrative work:

- Session notes and action plans are created manually after client conversations.
- Calendars, client records, messages, and spreadsheets do not share context.
- Scheduling requires repeated back-and-forth and creates double-booking risk.
- Generic automation tools do not reflect the provider's tone, modality, templates, or boundaries.
- Providers need a simple way to ask for information, such as "show me Client X's last session summary," without navigating multiple screens.

This administrative burden reduces client-facing capacity, consistency, and follow-through.

## 3. Product Vision

Make the provider's existing tools feel like one calm, context-aware command center: the provider can ask for information or delegate a task in natural language, review the assistant's work, and approve changes with confidence.

## 4. Goals and Non-Goals

### Goals

1. Reduce the time required to turn rough notes or transcripts into a usable session summary.
2. Generate clear, provider-specific action plans and follow-up tasks.
3. Give providers a conversational way to retrieve client and appointment information from other integrated systems, for MVP we will mock up these systems.
4. Prevent scheduling conflicts through centralized availability and explicit confirmation.
5. Preserve provider control through review, approval, audit history, and configurable boundaries.
6. Demonstrate the end-to-end workflow locally with mock integrations and persistent data.

### Non-goals for the MVP

- Diagnosing clients, providing medical advice, or making clinical decisions.
- Fully autonomous crisis response or emergency communication.
- Production HIPAA compliance certification or deployment to a regulated environment.
- Real WhatsApp, Instagram, Facebook, payment, CRM, or calendar integrations.
- Multi-provider team administration and complex billing.
- Training a custom foundation model.

## 5. Target Users

### Primary: Independent provider

A therapist, coach, nutritionist, astrologer, or other 1:1 service professional who manages client relationships and operations personally.

**Needs:** less documentation, reliable follow-up, fast access to context, consistent communication, and control over automation.

### Secondary: Low-technology independent service provider

A solo provider who primarily uses messaging applications, a calendar, and a spreadsheet.

**Needs:** simple language-based workflows, minimal navigation, clear confirmations, and low setup effort.

### Indirect: Client

The client receives clearer summaries, action plans, reminders, and appointment communication. The client does not directly operate the MVP.

## 6. Core User Journeys

### Journey A: Onboard provider

1. Provider enters business profile, service type, tone, preferred language, and communication boundaries.
2. Provider selects a service workflow and summary format.
3. Provider configures working hours, buffers, blackout dates, and maximum daily sessions.
4. Provider adds example templates or approved messages.
5. Assistant confirms the saved profile and explains which actions require approval.

**Outcome:** The assistant has enough context to generate provider-specific drafts and scheduling suggestions.

### Journey B: Create and approve a session summary

1. Provider opens a client record or tells the assistant to process a session.
2. Provider uploads a transcript, audio file, scanned note, or typed rough notes.
3. Assistant identifies the client and creates a structured draft using the provider's template.
4. Assistant displays source inputs, summary, uncertainties, and suggested action items.
5. Provider edits, approves, or rejects the draft.
6. On approval, the system stores the summary and records the approval event.

**Outcome:** A reviewable summary is available without manual reformatting.

### Journey C: Retrieve client context by chat

1. Provider asks a natural-language question, such as "Show me Client X's last session summary and open tasks."
2. Assistant identifies the client, retrieves authorized records, and presents a concise answer.
3. Assistant links the result to the full client context and states when data is unavailable or ambiguous.

**Outcome:** The provider gets the requested information without navigating multiple screens.

### Journey D: Suggest and confirm an appointment

1. Provider asks for available slots or forwards a client scheduling request.
2. Assistant checks mock calendar events, working hours, buffers, time zones, and service duration.
3. Assistant presents one or more valid options and identifies conflicts or missing information.
4. Provider approves a slot.
5. Assistant creates the appointment, updates the local client record, and drafts a confirmation.
6. Provider approves sending the confirmation in the MVP.

**Outcome:** Scheduling is faster while double-booking and accidental messages are prevented.

### Journey E: Generate a daily plan

1. Assistant reads the provider's appointments, tasks, deadlines, routines, and preparation needs.
2. Assistant creates a time-blocked plan with priorities and unscheduled work.
3. Provider edits or accepts the plan.
4. Assistant highlights conflicts and incomplete high-priority work.

**Outcome:** The provider has one practical plan for the day.

## 7. MVP Scope and Requirements

### 7.1 Provider profile and preferences

**FR-1** The system shall create and edit a provider profile containing name, practice or business name, service type, time zone, and preferred communication tone.

**FR-2** The system shall store provider modalities, service types, summary formats, approved phrases, and prohibited actions.

**FR-3** The system shall support configurable availability rules: working hours, session duration, buffer time, blackout dates, and maximum sessions per day.

**FR-4** The system shall show the provider which capabilities are enabled and which actions require approval.

### 7.2 Client and session records

**FR-5** The system shall create and edit client records with name, contact information, time zone, service type, goals, and status.

**FR-6** The system shall associate transcripts, notes, summaries, action plans, appointments, and tasks with a client.

**FR-7** The system shall accept text notes and transcript files in the MVP. Audio ingestion may be represented by a mock or deferred adapter.

**FR-8** The system shall retain the original input separately from generated content and show its processing status.

### 7.3 Session summarization

**FR-9** The system shall generate a draft summary using the provider's selected template, such as SOAP, DAP, coaching recap, or a custom format.

**FR-10** The summary shall distinguish source-supported information from inference, missing information, and unresolved ambiguity.

**FR-11** The provider shall be able to edit, regenerate, save as draft, approve, or reject a summary.

**FR-12** The system shall record who approved a summary and when.

**FR-13** The system shall not present a generated summary as a confirmed clinical record before provider approval.

### 7.4 Action plans and follow-up

**FR-14** The system shall generate a draft action plan from an approved summary or provider instructions.

**FR-15** Each action item shall support title, description, owner, due date, status, and follow-up date.

**FR-16** The provider shall be able to edit and approve action plans before sharing them with a client.

**FR-17** The system shall surface overdue tasks, missing post-session documentation, and upcoming preparation work.

### 7.5 Conversational assistant

**FR-18** The assistant shall accept natural-language requests through a chat interface.

**FR-19** The assistant shall support at least these intents in the MVP:

- Retrieve a client's latest summary, open tasks, or upcoming appointment.
- Create a session summary from supplied notes.
- Generate or update an action plan.
- Find available appointment slots.
- Create a draft appointment after confirmation.
- Generate a daily plan.

**FR-20** The assistant shall ask a concise clarification question when the client, date, service, or requested action is ambiguous.

**FR-21** The assistant shall show the records and planned tool actions used to answer or fulfill a request when practical.

**FR-22** The assistant shall report failure, missing permissions, and unavailable data explicitly rather than inventing an answer.

### 7.6 Scheduling

**FR-23** The system shall maintain a local mock calendar with events, time zones, and appointment status.

**FR-24** The scheduling logic shall respect provider availability, service duration, buffers, blackout dates, existing events, and client time zone.

**FR-25** The system shall never create an appointment without explicit provider approval.

**FR-26** The system shall support appointment creation, rescheduling, cancellation, and alternative slot suggestions in the local MVP.

### 7.7 Communication and research

**FR-27** The system shall generate provider-branded drafts for appointment confirmations, reminders, and session follow-ups.

**FR-28** The MVP shall use a mock messaging adapter and shall not send external messages.

**FR-29** The provider shall be able to maintain a curated list of research sources and request a source-grounded research brief.

**FR-30** Research results shall identify their sources and distinguish retrieved information from assistant-generated recommendations.

## 8. Agent Behavior and Trust Model

The assistant should behave as a supervised operator:

- **Read actions:** retrieval of authorized records may be automatic.
- **Draft actions:** summaries, action plans, messages, and research briefs require review.
- **Write actions:** saving approved records, booking appointments, and changing status require confirmation.
- **External actions:** sending messages or changing external systems require explicit confirmation and a visible preview.

Every tool call shall be scoped to the signed-in provider and recorded in an audit log. The assistant shall follow provider-defined boundaries and refuse or redirect requests for diagnosis, emergency intervention, or unsupported clinical advice.

## 9. Data Requirements

### Core entities

- Provider
- ProviderPreference
- Client
- ServiceType
- SessionInput
- SessionSummary
- ActionPlan
- ActionItem
- Appointment
- Task
- MessageDraft
- ResearchSource
- AuditEvent

### Data handling

- Store generated content with its source and version.
- Preserve draft, approved, rejected, and superseded states.
- Apply provider-level authorization to every client record lookup.
- Keep client data isolated between providers.
- Avoid logging raw session content in application logs.
- Make deletion of client records and associated local files possible.
- Treat the local MVP as demonstration software, not a production system for regulated data.

## 10. MVP Technical Constraints

- Frontend: existing local A2UI or frontend application with chat, forms, review panels, calendar, and client context views.
- Backend: FastAPI service.
- Agent orchestration: LangGraph/LangChain or the repository's established equivalent.
- Persistence: SQLite for structured data and local file storage for inputs.
- Retrieval: local vector store may be used for provider templates and approved history.
- Integrations: mock calendar, messaging, CRM, and spreadsheet adapters.
- Authentication: simple local authentication suitable for a demo environment.

## 11. Non-Functional Requirements

**NFR-1 Usability:** A provider shall be able to retrieve a client's latest summary in three or fewer conversational turns.

**NFR-2 Responsiveness:** Standard retrieval requests should return an initial response within 3 seconds in the local demo, excluding model latency; generation requests should show progress state.

**NFR-3 Reliability:** Scheduling must reject conflicts deterministically and must not silently create duplicate appointments.

**NFR-4 Explainability:** Generated records shall show status, source inputs, and approval state.

**NFR-5 Accessibility:** Primary workflows shall be keyboard usable, readable at common desktop sizes, and usable without relying on color alone.

**NFR-6 Privacy:** Sensitive content shall not be exposed across providers or written to ordinary debug logs.

**NFR-7 Recoverability:** Failed agent actions shall leave existing records unchanged and provide a retryable error state.

## 12. Success Metrics

### MVP success metrics

- At least 80% of test retrieval prompts return the correct client record and requested field.
- At least 90% of scheduling test cases reject double-bookings and invalid slots.
- At least 80% of generated summaries require only minor provider edits in a representative evaluation set.
- A provider can complete onboarding, generate a summary, approve an action plan, and schedule a mock appointment in under 15 minutes.
- At least 90% of write or external-action test cases require and capture explicit approval.

### Longer-term product metrics

- Reduction in average post-session documentation time.
- Percentage of sessions with an approved summary and action plan.
- Appointment scheduling completion rate and rescheduling time.
- Provider weekly active usage and retention.
- Provider-reported trust, usefulness, and perceived administrative workload.

## 13. Acceptance Criteria for MVP Demo

The MVP is ready for internal demonstration when:

1. A new provider can configure a service type, tone, template, boundaries, and availability.
2. A provider can create a client and attach rough notes or a transcript.
3. The assistant can generate a structured, editable summary tied to that client.
4. The provider can approve the summary and see its audit event.
5. The assistant can generate an action plan with due dates and follow-up tasks.
6. A chat request can retrieve the client's latest summary and open tasks.
7. The local calendar returns valid slots and rejects conflicting slots.
8. An appointment is created only after provider confirmation.
9. The assistant can generate a daily plan from mock events and tasks.
10. Mock message and integration actions show previews and status without contacting external systems.
11. Error states are visible for ambiguous client names, missing data, failed generation, and unavailable integrations.

## 14. Release Plan

### Phase 1: Foundation

- Local authentication and provider profile
- SQLite schema and local file storage
- Client, session, appointment, and task records
- Basic chat request/response surface

### Phase 2: Core assistant workflows

- Summary generation and review
- Action plan generation and review
- Client context retrieval
- Mock calendar and approval-based booking

### Phase 3: Daily operations

- Daily plan generation
- Follow-up reminders
- Mock message previews
- Curated research workflow

### Phase 4: Pilot readiness

- Usability testing with representative providers
- Stronger authorization and deletion controls
- Evaluation dataset for summaries and retrieval
- Integration design for Google Calendar, CRM, spreadsheets, and messaging channels

## 15. Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Hallucinated or incorrect session details | High | Source-linked drafts, uncertainty labels, provider approval, evaluation tests |
| Accidental client communication or booking | High | Explicit confirmation, preview, audit log, mock adapters in MVP |
| Sensitive data leakage | High | Provider-scoped authorization, minimal logs, local-only demo, deletion flow |
| Overly complex onboarding | Medium | Progressive setup, sensible defaults, editable templates |
| Generic tone or poor modality fit | Medium | Provider examples, configurable templates, correction feedback |
| Scheduling time-zone errors | Medium | Store time zones explicitly and show local time in confirmations |
| Over-automation reduces trust | Medium | Make agent actions visible, reversible, and approval-based |

## 16. Open Product Decisions

- Which first market should be prioritized: therapists/coaches or broader service providers?
- Should the first production version focus on one regulated modality or remain modality-neutral?
- Which calendar, CRM, spreadsheet, and messaging integrations provide the highest early value?
- What minimum consent and retention controls are required before handling real client data?
- Should clients receive a portal, email artifacts, or both?
- Which local or hosted model is acceptable for sensitive session content?
- How should provider corrections influence future drafts without silently changing established templates?
