# AI CLI Requirements

Scope: CLI machinery for AI: `--json` export, `--dump-*`, `--update`, `rqmd bug` command, non-interactive guarantees, and audit reporting.

<!-- acceptance-status-summary:start -->
Summary: 0💡 0🔧 0✅ 0⚠️ 0⛔ 11🗑️
<!-- acceptance-status-summary:end -->


### RQMD-AI-001: Dedicated rqmd-ai entrypoint

- **Status:** �️ Deprecated
- **Priority:** 🟢 P3 - Low
- **Summary:** A dedicated rqmd-ai command in this package so that AI workflows are explicit and separate from core rqmd interactive editing behavior.
- Deprecated: the `rqmd-ai` entrypoint was never built. AI-facing capabilities are now delivered via the rqmd VS Code extension's skill-based workflow.


### RQMD-AI-002: Read-only by default

- **Status:** �️ Deprecated
- **Priority:** 🟢 P3 - Low
- **Summary:** Rqmd-ai to default to read-only planning/reporting so that no requirement files are modified unless an explicit write/apply mode is requested.
- Deprecated: superseded by extension skill-based workflow; `rqmd-ai` entrypoint was never built.


### RQMD-AI-003: Deterministic machine output mode

- **Status:** 🗑️ Deprecated
- **Priority:** 🟢 P3 - Low
- **Summary:** Rqmd-ai --json to emit a stable schema with deterministic ordering so that downstream tooling can parse and diff outputs reliably.
- Superseded by `RQMD-AUTOMATION-010`, `RQMD-AUTOMATION-011`, `RQMD-AUTOMATION-012`, and `RQMD-AUTOMATION-013`, which should define the shared machine-output contract for both `rqmd` and any future `rqmd-ai` surface.


### RQMD-AI-004: Requirement context export for prompts

- **Status:** �️ Deprecated
- **Priority:** 🟢 P3 - Low
- **Summary:** Rqmd-ai to export selected requirement context by ID/file/status so that prompts can include only relevant requirement slices with stable identifiers.
- Deprecated: context export is handled by the extension's `rqmd-export-context` skill; `rqmd-ai` entrypoint was never built.


### RQMD-AI-005: Patch-plan preview before apply

- **Status:** �️ Deprecated
- **Priority:** 🟢 P3 - Low
- **Summary:** Rqmd-ai to provide a patch preview and change summary first so that humans can review intended modifications before any write occurs.
- Deprecated: superseded by extension skill-based workflow; `rqmd-ai` entrypoint was never built.


### RQMD-AI-006: Apply mode with guardrails

- **Status:** �️ Deprecated
- **Priority:** 🟢 P3 - Low
- **Summary:** Rqmd-ai --write to enforce strict validation and conflict checks so that malformed edits, unknown IDs, and cross-file ambiguity are rejected safely.
- Deprecated: superseded by extension skill-based workflow; `rqmd-ai` entrypoint was never built.


### RQMD-AI-007: Teaching-oriented guidance output

- **Status:** �️ Deprecated
- **Priority:** 🟢 P3 - Low
- **Summary:** Rqmd-ai to output concise guidance on requirement conventions and status workflow so that both humans and AI systems learn the expected rqmd contract quickly.
- Deprecated: guidance is delivered via the extension's agent mode and skill-based workflow; `rqmd-ai` entrypoint was never built.


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

- **Status:** �️ Deprecated
- **Priority:** 🟢 P3 - Low
- **Summary:** Rqmd-ai to emit a structured audit record of inputs, decisions, and outputs so that AI-assisted requirement changes remain traceable and reviewable.
- Deprecated: superseded by extension skill-based workflow; `rqmd-ai` entrypoint was never built.


### RQMD-AI-011: Domain-body context export for prompts

- **Status:** �️ Deprecated
- **Priority:** 🟢 P3 - Low
- **Summary:** Rqmd-ai exports to optionally include domain-body content aligned with RQMD-CORE-019 so that model prompts can include architecture/rationale notes without embedding those notes into individual requirement bodies.
- Deprecated: context export is handled by the extension's `rqmd-export-context` skill; `rqmd-ai` entrypoint was never built.
