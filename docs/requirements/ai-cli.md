# AI CLI Requirements

Scope: CLI machinery for AI: `--json` export, `--dump-*`, `--update`, `rqmd bug` command, non-interactive guarantees, and audit reporting.

<!-- acceptance-status-summary:start -->
Summary: 1💡 9🔧 0✅ 0⚠️ 0⛔ 3🗑️
<!-- acceptance-status-summary:end -->

### RQMD-AI-001: Dedicated rqmd-ai entrypoint
- **Status:** 🔧 Implemented
- **Priority:** 🔴 P0 - Critical
- **Summary:** A dedicated rqmd-ai command in this package so that AI workflows are explicit and separate from core rqmd interactive editing behavior.

### RQMD-AI-002: Read-only by default
- **Status:** 🔧 Implemented
- **Priority:** 🔴 P0 - Critical
- **Summary:** Rqmd-ai to default to read-only planning/reporting so that no requirement files are modified unless an explicit write/apply mode is requested.

### RQMD-AI-003: Deterministic machine output mode
- **Status:** 🗑️ Deprecated
- **Priority:** 🟢 P3 - Low
- **Summary:** Rqmd-ai --json to emit a stable schema with deterministic ordering so that downstream tooling can parse and diff outputs reliably.
- Superseded by `RQMD-AUTOMATION-010`, `RQMD-AUTOMATION-011`, `RQMD-AUTOMATION-012`, and `RQMD-AUTOMATION-013`, which should define the shared machine-output contract for both `rqmd` and any future `rqmd-ai` surface.

### RQMD-AI-004: Requirement context export for prompts
- **Status:** 🔧 Implemented
- **Priority:** 🔴 P0 - Critical
- **Summary:** Rqmd-ai to export selected requirement context by ID/file/status so that prompts can include only relevant requirement slices with stable identifiers.

### RQMD-AI-005: Patch-plan preview before apply
- **Status:** 🔧 Implemented
- **Priority:** 🔴 P0 - Critical
- **Summary:** Rqmd-ai to provide a patch preview and change summary first so that humans can review intended modifications before any write occurs.

### RQMD-AI-006: Apply mode with guardrails
- **Status:** 🔧 Implemented
- **Priority:** 🔴 P0 - Critical
- **Summary:** Rqmd-ai --write to enforce strict validation and conflict checks so that malformed edits, unknown IDs, and cross-file ambiguity are rejected safely.

### RQMD-AI-007: Teaching-oriented guidance output
- **Status:** 🔧 Implemented
- **Priority:** 🔴 P0 - Critical
- **Summary:** Rqmd-ai to output concise guidance on requirement conventions and status workflow so that both humans and AI systems learn the expected rqmd contract quickly.

### RQMD-AI-008: Batch suggestion ingestion
- **Status:** 🗑️ Deprecated
- **Priority:** 🟢 P3 - Low
- **Summary:** Rqmd-ai to accept JSONL/CSV suggestion files so that recommendation pipelines can be processed in deterministic batches.
- Superseded by `RQMD-AUTOMATION-004` and `RQMD-AUTOMATION-015` until `rqmd-ai` defines an input schema that is materially different from the shared batch automation model.

### RQMD-AI-009: Explicit non-interactive guarantee
- **Status:** 🗑️ Deprecated
- **Priority:** 🟢 P3 - Low
- **Summary:** Rqmd-ai modes to avoid interactive prompts unless explicitly requested so that jobs never hang waiting for terminal input.
- Superseded by `RQMD-AUTOMATION-017`, which should remain the single source of truth for prompt-suppression behavior across machine-oriented CLI modes.

### RQMD-AI-010: End-to-end audit report
- **Status:** 🔧 Implemented
- **Priority:** 🔴 P0 - Critical
- **Summary:** Rqmd-ai to emit a structured audit record of inputs, decisions, and outputs so that AI-assisted requirement changes remain traceable and reviewable.

### RQMD-AI-011: Domain-body context export for prompts
- **Status:** 🔧 Implemented
- **Priority:** 🔴 P0 - Critical
- **Summary:** Rqmd-ai exports to optionally include domain-body content aligned with RQMD-CORE-019 so that model prompts can include architecture/rationale notes without embedding those notes into individual requirement bodies.
















































### RQMD-AI-061: CLI bug filing command with VS Code handoff
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** To run `rqmd bug "short title"` and have the CLI generate a bug requirement boilerplate, append it to the appropriate domain file, and open VS Code at that location so that I can file bugs quickly from the command line with minimal friction, then finish filling out the Steps/Expected/Actual fields in my editor.
- Given the user runs `rqmd bug "Widget fails to render after config change"`
- When the CLI processes the command
- Then it discovers the appropriate domain file and next available ID via the same logic as `rqmd-ai --json`
- And it appends a bug requirement skeleton with the supplied title, `Status: 💡 Proposed`, `Type: bug`, and placeholder sections for Steps to Reproduce / Expected / Actual / Root Cause
- And it opens VS Code at the newly created requirement heading line (`code --goto file.md:line`)
- And it prints a brief confirmation with the requirement ID and file path
- And the command keeps CLI interaction short — no interactive prompts, no full editor experience in-terminal.



### RQMD-AI-063: Domain-aware `rqmd bug` with positional domain argument and tab completion
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- **Summary:** To type `rqmd bug <domain> "title"` with a positional domain argument and tab completion so that bugs land in the right domain file immediately without a post-hoc move step.
- Given the user types `rqmd bug interactive "Menu freezes on resize"`
- When the CLI processes the command
- Then it resolves `interactive` to `docs/requirements/interactive-ux.md` (or equivalent), allocates the next ID in that file, appends the bug skeleton, and opens VS Code at the new heading line
- And when the domain argument is ambiguous or matches no file it prints clear options and exits with a non-zero status without writing anything
- And shell completion for `rqmd bug` offers the list of known domain names as the first positional completion candidate.
