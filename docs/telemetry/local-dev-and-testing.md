# Telemetry Local Dev and E2E Testing

How to run the telemetry stack locally, inspect the data, and send test events.

## Quick start

```bash
# From the repo root
docker compose -f docker-compose.telemetry.yml up -d
```

This starts:

| Service | URL | What it does |
|---|---|---|
| **Postgres** | `localhost:55432` | Stores telemetry events |
| **MinIO** | `localhost:19000` (API), `localhost:9001` (console) | Stores artifact uploads |
| **Gateway** | `http://localhost:18080` | FastAPI — accepts events and artifacts |
| **Adminer** | `http://localhost:8080` | Web UI for browsing Postgres tables |

Wait a few seconds for healthchecks, then verify:

```bash
curl -s http://localhost:18080/health | python3 -m json.tool
```

Expected:

```json
{
    "status": "healthy",
    "postgres": true,
    "minio": true
}
```

## Browsing the database (Adminer)

Open [http://localhost:8080](http://localhost:8080) in your browser and log in:

| Field | Value |
|---|---|
| System | PostgreSQL |
| Server | `postgres` |
| Username | `rqmd` |
| Password | `rqmd_dev_pw` |
| Database | `rqmd_telemetry` |

> **ℹ️ Info:** Adminer gives you a spreadsheet-like view of every table. Click a table name to see rows, sort columns, filter, and export. It is already included in the compose stack — no extra install needed.

### Tables you will see

- **telemetry_events** — one row per submitted event (struggles, suggestions, errors, etc.)
- **telemetry_artifacts** — metadata for uploaded files linked to events

## VS Code extensions for Postgres (optional)

If you prefer staying inside VS Code instead of Adminer:

- **[Database Client](https://marketplace.visualstudio.com/items?itemName=cweijan.vscode-database-client2)** — connect to `localhost:55432`, user `rqmd`, password `rqmd_dev_pw`, database `rqmd_telemetry`. Gives you a table browser, query editor, and spreadsheet-style result grid.
- **[SQLTools](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools)** + **[SQLTools PostgreSQL Driver](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-pg)** — similar table browser with inline query execution.

Either one lets you click through tables and see rows without leaving VS Code.

## Browsing MinIO (artifact storage)

Open [http://localhost:9001](http://localhost:9001) and log in:

| Field | Value |
|---|---|
| Username | `minioadmin` |
| Password | `minioadmin_dev_pw` |

Browse the `rqmd-telemetry` bucket to see uploaded artifact files.

## E2E testing

The local dev gateway uses a default API key of `changeme-dev-only`. All examples below use that key.

### 1. Submit a test event

```bash
curl -X POST http://localhost:18080/api/v1/events \
  -H "Authorization: Bearer changeme-dev-only" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "agent_name": "manual-test",
    "event_type": "struggle",
    "severity": "medium",
    "summary": "Test event: rqmd-ai command not found",
    "detail": {
      "category": "command_discovery",
      "commands_attempted": ["rqmd-ai --json", "python -m rqmd.ai_cli --json"],
      "fallback_action": "Edited docs/requirements/telemetry.md directly",
      "stderr_snippet": "zsh: command not found: rqmd-ai"
    }
  }'
```

Expected response (201):

```json
{
  "event_id": "<uuid>",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "accepted"
}
```

### 2. Submit a suggestion event

```bash
curl -X POST http://localhost:18080/api/v1/events \
  -H "Authorization: Bearer changeme-dev-only" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "agent_name": "manual-test",
    "event_type": "suggestion",
    "severity": "low",
    "summary": "rqmd-ai should print the resolved Python path on startup",
    "detail": {
      "suggestion": "Add a --debug flag that shows which Python and entrypoint rqmd-ai resolved to",
      "confidence": "medium"
    }
  }'
```

### 3. Query events back

```bash
curl -s "http://localhost:18080/api/v1/events?limit=10" \
  -H "Authorization: Bearer changeme-dev-only" | python3 -m json.tool
```

Filter by type:

```bash
curl -s "http://localhost:18080/api/v1/events?event_type=struggle&limit=5" \
  -H "Authorization: Bearer changeme-dev-only" | python3 -m json.tool
```

### 4. Upload an artifact

Save the `event_id` from step 1, then:

```bash
echo "This is a test session log" > /tmp/test-artifact.txt

curl -X POST http://localhost:18080/api/v1/artifacts \
  -H "Authorization: Bearer changeme-dev-only" \
  -F "session_id=550e8400-e29b-41d4-a716-446655440000" \
  -F "event_id=<paste-event-id-here>" \
  -F "file=@/tmp/test-artifact.txt"
```

### 5. Use the Python client

```bash
export RQMD_TELEMETRY_ENDPOINT=http://localhost:18080
export RQMD_TELEMETRY_API_KEY=changeme-dev-only

uv run python3 -c "
from rqmd.telemetry import resolve_telemetry_endpoint, resolve_telemetry_api_key, report_struggle

endpoint = resolve_telemetry_endpoint()
api_key = resolve_telemetry_api_key()
print(f'Endpoint: {endpoint}')
print(f'API key configured: {api_key is not None}')

result = report_struggle(
    endpoint,
    summary='Python client test: command not found',
    command='rqmd-ai --json',
    expected='JSON output',
    actual='command not found',
    api_key=api_key,
)
print(f'Result: {result}')
"
```

### 6. Check status via rqmd-ai

```bash
export RQMD_TELEMETRY_ENDPOINT=http://localhost:18080
export RQMD_TELEMETRY_API_KEY=changeme-dev-only

uv run rqmd-ai telemetry --json
```

Expected:

```json
{
  "mode": "telemetry",
  "configured": true,
  "endpoint": "http://localhost:18080",
  "api_key_configured": true,
  "reachable": true,
  "health": { "status": "healthy", "postgres": true, "minio": true }
}
```

### 7. Verify in Adminer

After sending test events, open [http://localhost:8080](http://localhost:8080), navigate to the `telemetry_events` table, and click **Select data**. You should see your test rows with all fields populated.

## Verify auth is enforced

```bash
# No auth header — should get 401
curl -s -o /dev/null -w "%{http_code}" http://localhost:18080/api/v1/events

# Wrong key — should get 401
curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer wrong-key" \
  http://localhost:18080/api/v1/events
```

## Tear down

```bash
docker compose -f docker-compose.telemetry.yml down
```

Add `-v` to also remove the Postgres and MinIO data volumes:

```bash
docker compose -f docker-compose.telemetry.yml down -v
```

## Connecting to the remote Azure VM

If the VM is deployed and you want to test against production:

```bash
export RQMD_TELEMETRY_ENDPOINT=http://<vm-public-ip>:18080
export RQMD_TELEMETRY_API_KEY=<your-production-api-key>

uv run rqmd-ai telemetry --json
```

See [azure-v1-single-vm.md](azure-v1-single-vm.md) for deployment details.
