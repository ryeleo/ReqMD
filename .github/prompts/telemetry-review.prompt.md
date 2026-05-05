---
description: "rqmd-cli: Cluster recent telemetry events into proposed requirements."
name: "telemetry-review"
argument-hint: "Leave blank for the default 14-day window, or specify a number of days (e.g. '30')."
agent: "rqmd"
---

Triage recent telemetry signal into proposed requirements for rqmd-cli.

**Setup:**
- Ensure the SSH tunnel is running: start the `Tunnel to Az TeleVM` VS Code task if not active.
- Default query window: last 14 days. Use the argument to override.

**Query** — run this inline Python to fetch events:

```python
import psycopg2, json, os
from datetime import datetime, timedelta, timezone

WINDOW_DAYS = 14  # override from argument if provided
cutoff = datetime.now(timezone.utc) - timedelta(days=WINDOW_DAYS)

conn = psycopg2.connect(
    host="localhost", port=55432,
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
    dbname="rqmd_telemetry",
)
cur = conn.cursor()
cur.execute(
    "SELECT event_type, severity, summary, detail, agent_name, created_at "
    "FROM telemetry_events WHERE created_at >= %s ORDER BY created_at DESC",
    (cutoff,),
)
rows = [
    {"event_type": r[0], "severity": r[1], "summary": r[2],
     "detail": r[3], "agent_name": r[4], "created_at": str(r[5])}
    for r in cur.fetchall()
]
print(json.dumps(rows, indent=2, default=str))
conn.close()
```

> **⚠️ Note:** Requires `POSTGRES_USER` and `POSTGRES_PASSWORD` env vars (production credentials). Never hardcode them.

**Cluster** the returned events:
- Group by `(event_type, detail.category, root_cause_from_summary)`.
- Keep only clusters with **≥ 2 events**.
- For each cluster present: severity range, distinct `agent_name` values, representative `detail.command` and `detail.stderr_snippet`, event count, and a suggested requirement title.

**Dedup check** before drafting — scan `docs/requirements/` for open requirements with similar language. Flag matches as `⚠️ Possible duplicate of RQMD-...` and skip drafting for that cluster unless the user confirms it is distinct.

**Draft** (one cluster at a time, with confirmation):
1. Use `rqmd --json --non-interactive` to get the next available ID and identify the best-fit domain file.
2. Write a 💡 Proposed entry in the correct `docs/requirements/` file following the standard format (status, priority, summary, Given/When/Then).
3. Add a back-reference comment immediately after the heading: `<!-- sourced from telemetry cluster, query window: <ISO date range>, event_count: N -->`.
4. After all accepted drafts are written, run `rqmd --verify-summaries --non-interactive`.

**Closeout:** Report total events fetched, clusters surfaced, clusters drafted, clusters flagged as duplicates.
