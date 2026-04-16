# Bugs

<!-- acceptance-status-summary:start -->
Summary: 4💡 0🔧 0✅ 0⚠️ 0⛔ 0🗑️
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
- **Status:** 💡 Proposed
- **Type:** bug
- **Priority:** 🟠 P1 - High

#### Description
As a user, I encountered [problem] so that [impact].

#### Steps to Reproduce
1. 
2. 

#### Expected Behavior
- 

#### Actual Behavior
- 

#### Root Cause
- 

#### Acceptance Criteria
- [ ] Bug is fixed
- [ ] Regression test added

### RQMD-BUG-005: sync-index-metadata adds blank lines on repeat runs
- **Status:** 💡 Proposed
- **Type:** bug
- **Priority:** 🟠 P1 - High

#### Description
As a user, I encountered [problem] so that [impact].

#### Steps to Reproduce
1. 
2. 

#### Expected Behavior
- 

#### Actual Behavior
- 

#### Root Cause
- 

#### Acceptance Criteria
- [ ] Bug is fixed
- [ ] Regression test added

### RQMD-BUG-006: sync-index-metadata adds blank lines on repeat runs
- **Status:** 💡 Proposed
- **Type:** bug
- **Priority:** 🟠 P1 - High

#### Description
As a user, I encountered [problem] so that [impact].

#### Steps to Reproduce
1. 
2. 

#### Expected Behavior
- 

#### Actual Behavior
- 

#### Root Cause
- 

#### Acceptance Criteria
- [ ] Bug is fixed
- [ ] Regression test added
