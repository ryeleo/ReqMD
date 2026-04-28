---
name: dev
description: Repository-specific development commands for build, run, smoke-test, and environment setup in this project.
argument-hint: Describe whether you need environment setup, build, run, or smoke-test guidance for this repository.
user-invocable: true
metadata:
  guide:
    summary: Use the repository's canonical agent workflow entry point and development commands instead of guessing build, run, or smoke flows.
    workflow:
      - Start with `bash ./agent-workflow.sh preflight` to verify repository readiness before implementation.
      - Use the canonical build, run, and smoke commands below for active development work.
      - Prefer `bash ./agent-workflow.sh validate --profile build` or `bash ./agent-workflow.sh validate --profile smoke` before handoff when those profiles fit the task.
      - Update this generated skill if the repository's real commands differ from the scaffold.
    examples:
      - Ask which `bash ./agent-workflow.sh` profile should be used before implementation or handoff.
      - Ask for the canonical build or run command before launching local development.
---

Use this skill when implementation work needs the repository's actual development commands.

## VS Code-native first (per RQMD-EXT-090)

This is a VS Code workspace — prefer native execution surfaces over raw shell:

- **Use `run_task` for tasks.json labels** before falling back to `run_in_terminal`. Discovered labels in `.vscode/tasks.json`:
  - `Tunnel to Az TeleVM` — runs `./scripts/telemetry-tunnel.sh 20.94.227.192` (background)
  - `Start Remote Admin Tools` — `docker compose -f docker-compose.telemetry-admin.yml up -d`
  - `SSH to Az TeleVM` — `ssh azureuser@20.94.227.192` (background)
- **No `launch.json` exists yet.** When the user says "run XYZ" and no matching task exists, fall back to the canonical agent-workflow entry point or the raw commands below — and call out the fallback in one short line.
- When you discover a useful new VS Code-native surface, record it here so the next session does not re-discover it.

Canonical agent workflow entry point:
- `bash ./agent-workflow.sh preflight`
- `bash ./agent-workflow.sh validate --profile build`
- `bash ./agent-workflow.sh validate --profile smoke`

Detected sources:
- pyproject.toml
- scripts/local-smoke.sh

Environment setup:
- `uv sync --extra dev`

Build commands:
- No canonical build command was detected yet. Replace this with the repository's real build step.

Run commands:
- No canonical run or dev-server command was detected yet. Replace this with the repository's real run step.

Smoke commands:
- `./scripts/local-smoke.sh`

Playtest (dogfood) commands:
- `./scripts/playtest.sh` — build and install **both** rqmd-cli and rqmd-vscode from local source. Run after any implementation change to eat your own dog food.
- `./scripts/playtest.sh cli` — refresh only the global `rqmd` CLI.
- `./scripts/playtest.sh vscode` — rebuild and install only the VS Code extension.

Notes:
- Smoke coverage was detected under the development skill; keep `/test` focused on repeatable automated checks.
- Review the generated commands and tighten them to the repository's canonical workflows before relying on them in automation.

Constraints:
- Prefer the canonical agent workflow entry point for readiness and validation checks, and use the commands below for direct development work.
- Review and edit this generated skill after bootstrap if the detected commands are incomplete or stale.
