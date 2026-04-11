# Portability Requirement

Scope: cross-project operation, path configuration, and repo-agnostic behavior.

<!-- acceptance-status-summary:start -->
Summary: 0💡 8🔧 10✅ 0⚠️ 0⛔ 1🗑️
<!-- acceptance-status-summary:end -->

### RQMD-PORTABILITY-001: Configurable repo root
- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** To pass `--project-root` so that all file discovery and updates are scoped to that root.

### RQMD-PORTABILITY-002: Configurable requirements directory
- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** To set `--docs-dir` so that markdown discovery uses that directory.

### RQMD-PORTABILITY-003: Default conventions
- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** To run rqmd so that repo root defaults to current directory.

### RQMD-PORTABILITY-004: Stable relative source display
- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** Output to reference file paths so that source paths are shown relative to repo root.

### RQMD-PORTABILITY-005: Non-project-specific assumptions
- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** To run the command against a valid docs structure so that tool behavior does not depend on Speed Steel VR-specific files.

### RQMD-PORTABILITY-006: Optional future config file support
- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** An optional project config file so that defaults for repo root and requirements path can be declared centrally.

### RQMD-PORTABILITY-007: Status customization config location and precedence
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** To enable status customization so that the tool supports loading config from a project file at `.rqmd/statuses.json` or `.rqmd/statuses.yml` by default.

### RQMD-PORTABILITY-008: Automatic requirements-dir search from current path
- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** Rqmd to scan from the current working path so that rqmd searches for viable requirements index locations including `docs/requirements/README.md` and `requirements/README.md`.

### RQMD-PORTABILITY-009: Graceful startup errors for docs availability and permissions
- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** Startup validation to fail fast so that rqmd exits with a clear, actionable error message.

### RQMD-PORTABILITY-010: One-time emoji strip and restore commands
- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** To run `--strip-status-icons` once against the docs; to run `--restore-status-icons` once against the docs so that all emoji prefixes are removed from every status line across all requirements files.

### RQMD-PORTABILITY-011: Custom status schema in config file
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** Rqmd to load status configuration from file so that each custom status definition can specify `name`, `shortcode`, `emoji`, `color`, and `rollup_color`.

### RQMD-PORTABILITY-012: User-level config file for accessibility color overrides
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** Rqmd to load configuration so that rqmd supports a user-level config file at `~/.rqmd.config`.

### RQMD-PORTABILITY-014: Configurable state directory for persisted workflow state
- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** To run filtered interactive workflows with resume enabled so that rqmd supports `--session-state-dir` with explicit modes `system-temp` and `project-local`.

### RQMD-PORTABILITY-013: Project-configurable roll-up color knobs
- **Status:** 🗑️ Deprecated
- **Priority:** 🟢 P3 - Low
- **Deprecated:** Superseded by RQMD-ROLLUP-007, which generalizes roll-up customization through declarative roll-up mappings/expressions and can represent color behavior within that model.
- **Summary:** To provide a project-level status config file (e.g. `.rqmd/statuses.json`) so that the project config can include explicit roll-up color knobs such as `rollup_mode` (values: `per_status`|`bucketed`|`monochrome`), `bucket_map` to map statuses to roll-up buckets, and optional per-bucket `color` overrides.

### RQMD-PORTABILITY-015: Upward project-root discovery
- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- **Summary:** Rqmd to discover project root by searching CWD and parent paths up to filesystem root so that root resolution follows git-like behavior and finds the nearest valid project context.

### RQMD-PORTABILITY-016: Automated performance testing for large requirement datasets
- **Status:** 🔧 Implemented
- **Priority:** 🔴 P0 - Critical
- **Summary:** Automated performance tests against large fuzzy requirement datasets so that latency guardrails defined in RQMD-UI-009 are enforced for interactive startup and render-sensitive paths as requirements evolve.

### RQMD-PORTABILITY-017: Unknown status compatibility and recovery guidance
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** Rqmd to fail with actionable compatibility guidance instead of opaque value errors so that errors identify the unknown status value, source file, and nearest configured matches.

### RQMD-PORTABILITY-018: User-facing errors without Python tracebacks
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** Rqmd to fail with a user-facing CLI error so that rqmd prints actionable diagnostics and remediation guidance without raw Python stack traces in normal CLI usage.

### RQMD-PORTABILITY-019: Flexible requirement-doc terminology
- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- **Summary:** Generated and documented requirement indexes to use terminology that allows those alternate mental models so that scaffolded and synchronized README/index content refers to requirement documents rather than assuming every markdown file is a domain document.
