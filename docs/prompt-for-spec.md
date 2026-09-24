Based on details for EPIC-01 | Phase 1 | Foundation and app shell in build-plan-document.md update phase1-spec.md under . This specification file that will have technical solution required to actual implement that phase. Consider the architecture.md file to consider the mvp tech stack


Create an architecture design document ADD for a minimal viable product based on the PRD

So keep in mind when creating ADD, that we want to use that to create a simple build plan and then actually build the simplest version of the product. The ADD and build plan  should be scalable later.
I had this tech stack in mind

- Frontend: Next.js App Router, React, TypeScript, Tailwind CSS, component library
- Conversational UI: CopilotKit-style chat experience
- Agent protocol: AG-UI for structured agent events and streaming
- Backend: Python FastAPI with Uvicorn
- Agent framework: LangGraph
- LLM provider: 
- Tool integrations: MCP services using streamable HTTP
- Streaming: Server-Sent Events for incremental assistant responses
- Observability: Langsmith


FastAPI: HTTP endpoints, authentication, authorization, request validation, SSE responses.
LangGraph: Agent orchestration, workflow state, nodes, edges, tool calls, retries, approvals, checkpoints.
AG-UI: Protocol for sending lifecycle events, text deltas, tool events, state updates, and errors to the frontend.
CopilotKit: Frontend chat state and rendering.

CopilotKit / React UI
        |
        | AG-UI events over HTTP/SSE
        v
FastAPI application
        |
        v
LangGraph orchestration graph
        |
        +--> Azure OpenAI
        +--> MCP tools
        +--> Healthcare data systems
        +--> Persistence/checkpointer

