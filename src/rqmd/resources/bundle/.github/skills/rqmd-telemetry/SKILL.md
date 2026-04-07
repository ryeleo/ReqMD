---
name: rqmd-telemetry
description: Report AI workflow friction, improvement suggestions, and session diagnostics to the rqmd telemetry service. Use when an rqmd command fails unexpectedly, when workflow guidance is confusing, or when you notice something that could be improved.
argument-hint: Describe the friction, failure, or improvement idea you want to report.
user-invocable: true
metadata:
  guide:
    summary: Submit structured telemetry events so rqmd developers can see where AI agents struggle and what they think could be better.
    workflow:
      - Check whether telemetry is configured before attempting to send events.
      - Submit struggle reports when rqmd commands fail or produce unexpected output.
      - Submit improvement suggestions when you notice friction that was not a hard failure.
      - Include enough context for a developer to understand the issue without the full chat transcript.
    examples:
      - Report a struggle when rqmd --verify-summaries fails unexpectedly.
      - Suggest an improvement when rqmd-ai JSON output is hard to parse.
      - Report an error when a bundle install command exits non-zero.
---

Use this skill when you encounter friction, errors, or improvement opportunities while using rqmd workflows.

## Telemetry is opt-in and local-first

Telemetry is **never** sent unless a telemetry endpoint has been explicitly configured. Check for a configured endpoint before attempting to send events:

1. Look for `telemetry.endpoint` in the project `.rqmd.yml` / `.rqmd.yaml` / `.rqmd.json` config file.
2. Check the `RQMD_TELEMETRY_ENDPOINT` environment variable.
3. If neither is set, **do not attempt to send telemetry**. You may still log the event to stderr for the user's awareness.

## Authentication

All gateway endpoints except `/health` require an API key. The key is resolved the same way as the endpoint:

1. `RQMD_TELEMETRY_API_KEY` environment variable.
2. `telemetry.api_key` in the project `.rqmd.yml` / `.rqmd.yaml` / `.rqmd.json` config file.

Include the key as a Bearer token on every request:

```
Authorization: Bearer <api-key>
```

If no API key is configured but an endpoint is, requests will likely receive a `403 Forbidden` response from the gateway.

## When to report

Report a **struggle** event when:
- An rqmd or rqmd-ai command exits non-zero or produces unexpected output.
- You had to retry a command multiple times to get it working.
- Workflow guidance was confusing or led you down a wrong path.
- You could not find the right command, flag, or skill for what you needed.
- JSON output was malformed, missing expected fields, or hard to parse.

Report a **suggestion** event when:
- You notice friction that was not a hard failure but made the workflow harder than it should be.
- You think a command, flag, or workflow could be designed differently to be more intuitive.
- You see a pattern where rqmd guidance could teach something better or earlier.
- You think a new skill, prompt, or workflow would fill a gap you observed.

Report an **error** event when:
- A Python traceback or unhandled exception occurs during an rqmd command.
- A command hangs or times out unexpectedly.

## How to report

POST a JSON event to the configured telemetry endpoint:

```
POST {endpoint}/api/v1/events
Content-Type: application/json
Authorization: Bearer <api-key>

{
  "session_id": "<your-session-id-or-uuid>",
  "agent_name": "<agent-name-if-known>",
  "event_type": "struggle" | "suggestion" | "error" | "success" | "workflow_step",
  "severity": "low" | "medium" | "high" | "critical",
  "summary": "Concise one-line description of what happened",
  "detail": {
    "command": "the rqmd command that was involved, if any",
    "expected": "what you expected to happen",
    "actual": "what actually happened",
    "stderr_snippet": "relevant stderr output, truncated to 2000 chars",
    "suggestion": "what you think should change, for suggestion events",
    "confidence": "low | medium | high, for suggestion events",
    "context": "any other structured context that helps"
  }
}
```

## Event field reference

| Field | Required | Description |
|---|---|---|
| `session_id` | yes | A UUID or unique session identifier. Use one per chat session or agent run. |
| `agent_name` | no | The agent name, e.g. `rqmd-dev`, `rqmd-dev-longrunning`. |
| `event_type` | yes | One of: `struggle`, `suggestion`, `error`, `success`, `workflow_step`. |
| `severity` | yes | One of: `low`, `medium`, `high`, `critical`. |
| `summary` | yes | A concise one-line description. Keep under 200 characters. |
| `detail` | no | Structured JSON object with additional context. Shape varies by event type. |

## Artifact uploads

For larger payloads such as full command output, session logs, or prompt snapshots, POST to the artifact endpoint:

```
POST {endpoint}/api/v1/artifacts
Content-Type: multipart/form-data
Authorization: Bearer <api-key>

Fields:
  - session_id: <session-id>
  - event_id: <event-id-from-event-response>
  - file: <the-artifact-file>
```

The gateway stores artifacts in MinIO and links them to the originating event.

## Constraints

- **Never send telemetry without an explicitly configured endpoint.**
- Truncate stderr and stdout snippets to 2000 characters maximum.
- Do not include secrets, tokens, passwords, or file contents that may contain sensitive data in telemetry payloads.
- Prefer structured `detail` fields over dumping raw text into `summary`.
- One event per observed issue. Do not batch multiple unrelated issues into a single event.
- Skills improve workflow discovery; shell and tool approvals may still be required.
