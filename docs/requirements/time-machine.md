> **🚨 Warning:** This requirement domain document is currently deprecated and pending archival.

# Time Machine Requirement

Scope: branch-aware temporal navigation, historical inspection, detached point-in-time views, replay from past states, and timeline-oriented UX for requirement catalogs.

<!-- acceptance-status-summary:start -->
Summary: 0💡 0🔧 0✅ 0⚠️ 0⛔ 10🗑️
<!-- acceptance-status-summary:end -->

### RQMD-TIME-001: Point-in-time catalog browsing
- **Status:** 🗑️ Deprecated
- **Priority:** 🟡 P2 - Medium
- **Summary:** To select a prior timestamp, revision, or history entry so that rqmd can present the full catalog as it existed at that point in time without mutating the current working state.

### RQMD-TIME-002: Branch-aware historical timeline
- **Status:** 🗑️ Deprecated
- **Priority:** 🟡 P2 - Medium
- **Summary:** Rqmd to render timeline history so that the timeline shows branch structure explicitly rather than flattening divergent paths into a single linear list.

### RQMD-TIME-003: Detached historical view mode
- **Status:** 🗑️ Deprecated
- **Priority:** 🟡 P2 - Medium
- **Summary:** To enter a historical point from the timeline so that rqmd opens a detached read-only view rooted at that historical revision.

### RQMD-TIME-004: Historical context and activity inspection
- **Status:** 🗑️ Deprecated
- **Priority:** 🟡 P2 - Medium
- **Summary:** Rqmd to render that historical state so that the UI shows what changed at that point including changed files, affected requirement IDs, before/after status values, reason text, and actor/context metadata.

### RQMD-TIME-005: Compare historical points and branches
- **Status:** 🗑️ Deprecated
- **Priority:** 🟡 P2 - Medium
- **Summary:** To select two points in time, two branches, or a branch point and current head so that rqmd can render a diff-oriented comparison of summaries, requirement statuses, reasons, and affected documents.

### RQMD-TIME-006: Replay and restore from historical points
- **Status:** 🗑️ Deprecated
- **Priority:** 🟡 P2 - Medium
- **Summary:** To choose to restore, replay, or cherry-pick from that point so that rqmd offers explicit actions to (a) restore the catalog to that exact state, (b) replay subsequent changes from a chosen branch, or (c) cherry-pick selected historical entries onto current head.

### RQMD-TIME-007: Timeline filters and queryable navigation
- **Status:** 🗑️ Deprecated
- **Priority:** 🟡 P2 - Medium
- **Summary:** To browse the timeline so that rqmd supports filters by branch, requirement ID, file path, actor, status transition, date range, and operation type.

### RQMD-TIME-008: Stable historical identifiers and deep links
- **Status:** 🗑️ Deprecated
- **Priority:** 🟡 P2 - Medium
- **Summary:** Rqmd to expose a timeline node or detached historical view so that each point-in-time state has a stable identifier that can be referenced in CLI commands, JSON output, and future UI deep links.

### RQMD-TIME-009: Exportable temporal reports
- **Status:** 🗑️ Deprecated
- **Priority:** 🟡 P2 - Medium
- **Summary:** Automation to request a historical export so that rqmd can emit JSON and text reports for a selected point-in-time state or comparison range including branch metadata, summary totals, and per-requirement status details.

### RQMD-TIME-010: Verification coverage for temporal navigation
- **Status:** 🗑️ Deprecated
- **Priority:** 🟡 P2 - Medium
- **Summary:** To implement the time-machine feature set so that tests cover branch graph reconstruction, detached historical reads, point-to-point diffs, replay/restore previews, and stable identifier resolution.
