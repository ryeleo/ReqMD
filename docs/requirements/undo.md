> **🚨 Warning:** This requirement domain document is currently deprecated and pending archival.

# Undo / History Requirement

Scope: full undo/redo semantics, persistent history across restarts/crashes, branching and "lost changes" recovery, UI affordances, and storage/retention policies.

<!-- acceptance-status-summary:start -->
Summary: 0💡 0🔧 0✅ 0⚠️ 0⛔ 11🗑️
<!-- acceptance-status-summary:end -->

### RQMD-UNDO-001: Full undo/redo semantics
- **Status:** 🗑️ Deprecated
- **Priority:** 🟡 P2 - Medium
- **Summary:** To request `undo` so that the most recent change is reverted and the UI updates to reflect the prior state.

### RQMD-UNDO-002: Persistent history across restarts and crashes
- **Status:** 🗑️ Deprecated
- **Priority:** 🟡 P2 - Medium
- **Summary:** To restart rqmd so that the full undo/redo history up to the last acknowledged write is available for inspection and replay.

### RQMD-UNDO-003: Branching history and "lost changes" visibility
- **Status:** 🗑️ Deprecated
- **Priority:** 🟡 P2 - Medium
- **Summary:** The divergence to occur so that the system preserves the prior undone sequence as an alternate branch (not permanently discarded).

### RQMD-UNDO-004: Interactive reconfirmation when rewriting history
- **Status:** 🗑️ Deprecated
- **Priority:** 🟡 P2 - Medium
- **Summary:** Such an action to require explicit confirmation in interactive mode so that rqmd prompts the user with a concise summary of what will be lost and requires explicit confirmation before proceeding.

### RQMD-UNDO-005: Storage backend and crash-safety
- **Status:** 🗑️ Deprecated
- **Priority:** 🟡 P2 - Medium
- **Summary:** To implement undo stack storage so that rqmd uses a single hidden local git repository as the canonical history backend, initialized as `rqmd-history` under `.rqmd/history/`.

### RQMD-UNDO-006: Metadata, auditability, and provenance
- **Status:** 🗑️ Deprecated
- **Priority:** 🟡 P2 - Medium
- **Summary:** To record history entries so that each entry includes timestamp, actor (user or automated), command context, affected file paths, file diffs or delta payloads, and optional human-supplied reason text.

### RQMD-UNDO-007: UI affordances and commands
- **Status:** 🗑️ Deprecated
- **Priority:** 🟡 P2 - Medium
- **Summary:** To expose history controls so that rqmd provides:.
  - `undo` and `redo` commands / keys
  - `history` listing with paging that shows branches, commits, and diffs
  - `branch` and `checkout` primitives for working with alternate histories
  - `replay` and `cherry-pick` for applying past changes to current head
  - safe `gc`/`prune` commands that require confirmation
- **Summary:** Interactive prompts clearly explain consequences and offer to save named snapshots before destructive operations.

### RQMD-UNDO-008: Size, retention, and compaction policy
- **Status:** 🗑️ Deprecated
- **Priority:** 🟡 P2 - Medium
- **Summary:** Storage to grow beyond configured thresholds so that rqmd supports configurable retention policies: retain-last-N, retain-by-age, and retain-by-size.

### RQMD-UNDO-009: Programmatic API and automation
- **Status:** 🗑️ Deprecated
- **Priority:** 🟡 P2 - Medium
- **Summary:** Automation to invoke history APIs so that a machine-friendly interface is available (JSON output, programmatic commands) to list entries, export patches, and apply or revert specific entries.

### RQMD-UNDO-010: Tests and verification
- **Status:** 🗑️ Deprecated
- **Priority:** 🟡 P2 - Medium
- **Summary:** To implement the system so that an extensive test matrix covers unit tests for journal/git operations, integration tests for crash recovery (simulating abrupt termination), and UX tests for branch/replay flows.

### RQMD-UNDO-011: Unified undo and audit capture
- **Status:** 🗑️ Deprecated
- **Priority:** 🟡 P2 - Medium
- **Summary:** Every rqmd write operation to be recorded in the same `rqmd-history` backend used for undo/redo so that undo/history and audit logging cannot drift or contradict each other.
