# Bugs

<!-- acceptance-status-summary:start -->
Summary: 1💡 3🔧 0✅ 0⚠️ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->


This file is the runtime bug backlog for concrete rqmd defects that need fixing.

- File real bugs here as backlog entries (symptom, impact, repro steps, expected vs actual).
- Do **not** define bug-tracking policy here.
- Bug-tracking behavior requirements live in [Bug Tracking](bug-tracking.md).

Quick rule:

- "rqmd is broken in this specific way" -> this file.
- "rqmd should support this bug-tracking capability" -> [Bug Tracking](bug-tracking.md).

<a id="rqmd-bug-003"></a>

### RQMD-BUG-003: `--project-root .` resolves relative to `uv --directory`, not shell cwd

- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- **Type:** bug
- **Affects:** RQMD-PORTABILITY-001

#### Steps to Reproduce

1. Have two rqmd-managed repos side by side: `rqmd-cli/` and `rqmd-vscode/`
2. `cd rqmd-vscode`
3. Run: `uv run --directory ../rqmd-cli rqmd --non-interactive --project-root .`

#### Expected

rqmd processes `rqmd-vscode/docs/requirements/` (the shell's cwd).

#### Actual

rqmd processes `rqmd-cli/docs/requirements/` because Python's `Path(".")` resolves relative to the process working directory, which `uv run --directory` changes to the `--directory` target before launching rqmd.

#### Root Cause

`--project-root .` is resolved by `Path(".").resolve()` inside the rqmd process. When invoked via `uv run --directory ../rqmd-cli`, `uv` changes the process cwd to `rqmd-cli/` before executing rqmd, so `.` means `rqmd-cli/`, not the shell's cwd.

#### Impact

- Multi-root workspaces using `uv run --directory` to invoke rqmd against a different project silently process the wrong project's requirements
- Summary counts, verify-summaries, and `--json` output are all incorrect but appear valid
- The rqmd-vscode agent instructions use this exact invocation pattern: `uv run --directory ../rqmd-cli rqmd ... --project-root .`

#### Possible Fix

Document the gotcha (use absolute paths with `--project-root "$PWD"` instead of `.`) and/or resolve `--project-root` relative to an env var like `RQMD_CALLER_CWD` that callers can set before `uv run --directory` changes cwd.

### RQMD-BUG-004: sync-index-metadata adds blank lines on repeat runs
- **Status:** 🔧 Implemented
- **Type:** bug
- **Priority:** � P2 - Medium
- **Affects:** RQMD-CORE-033

#### Steps to Reproduce

1. Have a requirements index with an existing `## Project Tooling Metadata` section
2. Run `rqmd --sync-index-metadata --force-yes`
3. Run it again — observe blank lines growing around the metadata section
4. Repeat — each invocation adds more vertical whitespace

#### Expected Behavior

Running `--sync-index-metadata` repeatedly with no substantive changes should be idempotent — the file should not change at all after the first successful sync.

#### Actual Behavior

Each run adds extra blank lines above and/or below the `## Project Tooling Metadata` section. The whitespace accumulates with every invocation.

#### Root Cause

In `sync_requirements_index_tooling_metadata()` ([markdown_io.py](../../src/rqmd/markdown_io.py)), the regex pattern uses `\n?` anchors (consuming at most one newline) but the replacement string injects `\n\n...\n\n` (two newlines on each side). On each run the pattern under-consumes surrounding newlines while the replacement over-produces them, causing a net gain of blank lines per invocation.

#### Acceptance Criteria
- [ ] Running `--sync-index-metadata` twice in a row produces identical output
- [ ] Regression test asserts idempotency (run sync, run again, assert no diff)

<a id="rqmd-bug-005"></a>

### RQMD-BUG-005: `rqmd init` requires `--scaffold` even though it is the only mode

- **Status:** 🔧 Implemented
- **Type:** bug
- **Priority:** 🔴 P0 - Critical

#### Steps to Reproduce

1. Clone a fresh repo with no requirement docs
2. Run `rqmd` — observe the "no requirement docs found" help text, which recommends: _"AI-driven (recommended): run `rqmd init`"_
3. Run `rqmd init`

#### Expected Behavior

`rqmd init` scaffolds the requirements directory directly (same as `rqmd init --scaffold` today). The "AI-driven" path referenced in the help text is gone from the CLI; `--scaffold` is the only mode, so the bare command should just work.

#### Actual Behavior

`rqmd init` prints:
```
Error: AI-guided init is no longer part of the CLI. Use `rqmd init --scaffold` to create a starter requirements scaffold, or use the rqmd VS Code extension for AI-assisted setup.
```
The user just followed the help text and got an error with no productive output. Two-step failure.

#### Root Cause

When AI-guided init was removed from the CLI, `rqmd init` (no flags) was left as a dead end rather than being aliased to `--scaffold` behavior. The "no docs found" error message was not updated to remove the now-misleading AI-driven recommendation.

#### Acceptance Criteria
- [ ] `rqmd init` (no flags) runs the scaffold flow — same outcome as `rqmd init --scaffold`
- [ ] `rqmd init --scaffold` continues to work unchanged (backwards compatible)
- [ ] The "no requirement docs found" help text no longer references an AI-driven `rqmd init` path; the scaffold path is the primary recommendation
- [ ] RQMD-CORE-030 status updated to reflect the current (non-AI) default behavior

### RQMD-BUG-006: Auto-install failure message too vague, hides console output
- **Status:** 🔧 Implemented
- **Type:** bug
- **Priority:** � P2 - Medium
- **Affects:** VS Code extension bootstrap / auto-install flow

#### Description
When the VS Code extension's auto-install of the `rqmd` CLI fails, the user sees only a generic message: "Could not install rqmd automatically. Check network, permissions, or Python toolchain and try again." This message discards the actual subprocess output and exception details, leaving the user with no actionable information about what went wrong.

#### Steps to Reproduce
1. Open VS Code with the rqmd extension installed.
2. Trigger a condition that causes auto-install to fail (e.g., no network, broken pip, missing Python, insufficient permissions).
3. Observe the error notification or output panel message.

#### Expected Behavior
- The error message includes the captured stdout/stderr from the failed install subprocess.
- The message surfaces the specific failure reason (e.g., "pip: command not found", "Permission denied: /usr/local/lib", "SSL: CERTIFICATE_VERIFY_FAILED").
- Where possible, the message links to a troubleshooting doc or suggests a concrete next step based on the error type.

#### Actual Behavior
- User sees only: "Could not install rqmd automatically. Check network, permissions, or Python toolchain and try again."
- No subprocess output is shown.
- No indication of which of the three possible causes (network, permissions, toolchain) actually occurred.
- User has no console output or log reference to diagnose the failure.

#### Root Cause
- The auto-install error handler catches the exception but discards the subprocess stdout/stderr rather than forwarding it to the notification or output channel.

#### Acceptance Criteria
- [ ] Subprocess stdout/stderr from the failed install is captured and shown in the VS Code output channel.
- [ ] The user-facing notification includes or links to the captured output.
- [ ] If the error can be classified (network / permissions / toolchain), the message names the specific category and suggests a targeted next step.
- [ ] Regression test verifies that a simulated install failure surfaces the subprocess output.
