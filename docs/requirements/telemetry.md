# Telemetry Requirement

Scope: agent-facing telemetry infrastructure for capturing AI workflow friction, improvement suggestions, and session diagnostics — enabling rqmd's own AI agents to report how rqmd can be improved.

<!-- acceptance-status-summary:start -->
Summary: 0💡 8🔧 0✅ 0⚠️ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->

### RQMD-TELEMETRY-001: Local telemetry development stack
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- As a developer working on rqmd telemetry features locally
- I want a Docker Compose stack with Postgres, MinIO, a telemetry gateway, and admin tooling
- So that the full telemetry pipeline can run on a single machine without external service dependencies.
- Given a developer runs `docker compose -f docker-compose.telemetry.yml up`
- When all services reach healthy status
- Then a Postgres database is available for structured telemetry events, a MinIO bucket exists for larger artifacts such as session logs and prompt snapshots, and a gateway accepts HTTP posts on a non-standard dev port
- And default credentials are dev-only, clearly marked, and never used for production.

### RQMD-TELEMETRY-002: Telemetry event schema
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- As a developer querying telemetry data to understand agent behavior
- I want a structured event schema that captures session identity, event type, severity, agent context, and freeform detail
- So that telemetry data is queryable, filterable, and useful for diagnosing patterns across many agent sessions.
- Given an AI agent submits a telemetry event
- When the event is stored
- Then it includes at minimum: event_id, session_id, timestamp, agent_name, event_type (struggle | suggestion | error | success | workflow_step), severity, summary text, and optional structured detail JSON
- And event_type is extensible so new categories can be added without schema migration.

### RQMD-TELEMETRY-003: Telemetry HTTP gateway
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- As an AI agent running inside a chat session that encounters friction with rqmd
- I want a simple HTTP endpoint I can POST structured telemetry events to
- So that telemetry capture does not require database drivers, SDK dependencies, or complex client setup inside the agent environment.
- Given an agent has a telemetry endpoint URL configured
- When it POSTs a JSON event body to the gateway
- Then the gateway validates the payload against the event schema, stores the structured event in Postgres, and optionally stores referenced artifacts in MinIO
- And the gateway responds with a confirmation or structured error so the agent knows whether the report succeeded.

### RQMD-TELEMETRY-004: rqmd-telemetry bundle skill
- **Status:** 🔧 Implemented
- **Priority:** 🔴 P0 - Critical
- As a maintainer who installs the rqmd AI bundle into a repository
- I want an `/rqmd-telemetry` skill that teaches AI agents how and when to submit telemetry
- So that agents have clear instructions for reporting friction, errors, and improvement ideas without needing ad hoc prompting.
- Given an AI agent encounters a problem while running rqmd workflows
- When the agent has the rqmd-telemetry skill loaded
- Then it knows the telemetry endpoint, the event schema, and the expected submission protocol
- And it can decide autonomously whether to submit a struggle report, an improvement suggestion, or both based on what it observed
- And the skill guidance makes clear that telemetry is opt-in, local-first, and never silently phones home.

### RQMD-TELEMETRY-005: Agent struggle reporting
- **Status:** 🔧 Implemented
- **Priority:** 🔴 P0 - Critical
- As a developer reviewing telemetry to understand where rqmd agents fail
- I want agents to report structured "I struggled because..." events when they encounter friction with rqmd workflows
- So that recurring failure patterns surface as queryable data instead of disappearing into chat transcripts.
- Given an AI agent tries to run an rqmd command, parse rqmd output, or follow rqmd workflow guidance and encounters unexpected behavior
- When it recognizes that something went wrong or took significantly more effort than expected
- Then it submits a telemetry event with event_type "struggle", a concise summary of what it was trying to do, what went wrong, any error output or unexpected state it observed, and which rqmd command or skill was involved
- And the event captures enough context for a developer to reproduce or understand the failure without needing the full chat transcript.

### RQMD-TELEMETRY-006: Agent improvement suggestions
- **Status:** 🔧 Implemented
- **Priority:** 🔴 P0 - Critical
- As a developer who wants rqmd to get better informed by AI agent experience
- I want agents to proactively submit "rqmd could be improved if..." suggestions based on their direct experience using rqmd
- So that product improvement ideas come from the agents that actually use the tool day to day, not just from manually observed failures.
- Given an AI agent completes or partially completes an rqmd workflow
- When it identifies friction that was not a hard failure but made the workflow harder, slower, or more confusing than it should have been
- Then it submits a telemetry event with event_type "suggestion", a concise description of the observed friction, a proposed improvement or change, and an optional confidence level
- And the suggestion captures enough detail for a developer to evaluate whether the idea is actionable without needing the full session context.

### RQMD-TELEMETRY-007: Telemetry opt-in and privacy controls
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- As a user who values privacy and does not want silent data collection
- I want telemetry to be explicitly opt-in, default to local-only storage, and never transmit data without clear configuration
- So that rqmd telemetry cannot become a trust liability.
- Given a repository has the rqmd AI bundle installed with the telemetry skill
- When no telemetry endpoint has been explicitly configured
- Then agents must not attempt to send telemetry events anywhere
- And when a local telemetry endpoint is configured, events stay on the local machine unless a remote endpoint is separately and explicitly opted into
- And the skill guidance makes the opt-in contract visible to both agents and humans reviewing the installed bundle.

### RQMD-TELEMETRY-008: Agent telemetry configuration discovery
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- As an AI agent that needs to submit telemetry events to a remote gateway
- I want a single discovery mechanism that resolves both the telemetry endpoint URL and the API key from well-known configuration sources
- So that I can authenticate with the gateway without ad-hoc credential handling or hard-coded secrets.
- Given an agent invokes the telemetry config discovery
- When the `RQMD_TELEMETRY_ENDPOINT` environment variable is set
- Then the endpoint URL is taken from that variable
- And when the `RQMD_TELEMETRY_API_KEY` environment variable is set
- Then the API key is taken from that variable
- And when the environment variables are not set but a `.rqmd.yml` / `.rqmd.yaml` / `.rqmd.json` config file contains `telemetry.endpoint` and/or `telemetry.api_key`
- Then those config-file values are used as fallbacks
- And when neither source provides an endpoint, telemetry is silently disabled
- And the `submit_event` client includes the resolved API key as a `Bearer` token in the `Authorization` header on every request
- And the `rqmd-ai telemetry` status command reports whether an API key is configured (without revealing the key value).
