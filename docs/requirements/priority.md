# Priority Requirement

Scope: add a first-class `Priority` field to requirement entries, integrate priority into interactive and non-interactive flows, and allow priority-aware sorting and summaries.

<!-- acceptance-status-summary:start -->
Summary: 0💡 2🔧 9✅ 0⚠️ 0⛔ 1🗑️
<!-- acceptance-status-summary:end -->


### RQMD-PRIORITY-001: First-class priority field

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** Rqmd to parse it so that the parser recognizes an optional `- **Priority:** <label>` line adjacent to the status line.


### RQMD-PRIORITY-002: Priority normalization and allowed values

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** The tool to read and write priorities so that a canonical default set is available (e.g., `P0`,`P1`,`P2`,`P3` or `High`,`Med`,`Low`) and project-level overrides are supported via `.reqmd/statuses.yml` or a new `.reqmd/priorities.yml`.


### RQMD-PRIORITY-003: Set status/priority combined UI

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** To open the status menu for a requirement so that the menu is extended to allow setting both `Status` and `Priority` without leaving the panel.


### RQMD-PRIORITY-004: `--focus-priority` startup flag

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** To provide `--focus-priority` at startup so that interactive entry panels default to `Priority` focus instead of `Status` focus.


### RQMD-PRIORITY-005: Persistence and summary integration

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** To generate summary/roll-up blocks so that priority-aware aggregates can be optionally included (e.g., counts by priority per file).


### RQMD-PRIORITY-006: Sorting and filters using priority

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** Sorting or filtering in interactive or non-interactive flows so that `priority` is available as a sortable/filterable column and integrates with `s` cycling and `d` direction toggles.


### RQMD-PRIORITY-007: Validation and migration

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** The parser to encounter missing priorities so that it treats them as `unset` and does not break parsing.


### RQMD-PRIORITY-008: Undo and history semantics

- **Status:** 🗑️ Deprecated
- **Priority:** 🟠 P1 - High
- **Summary:** To make or undo priority changes so that the priority system remains independent from removed undo/history workflows in the simplified 0.x scope.


### RQMD-PRIORITY-009: Automation and batch updates

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** To apply bulk priority updates (via `--update-priority` or a file) so that the tool applies updates deterministically and emits machine-readable summaries showing changed files and counts.


### RQMD-PRIORITY-010: Tests and documentation

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** To implement priority features so that unit tests cover parsing, normalization, UI toggle behavior, sorting integration, and migration; documentation and examples are added to README and examples in `.reqmd/`.


### RQMD-PRIORITY-011: Project-customizable priority catalog schema

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** Priority definitions to be configurable per project similarly to status definitions so that each priority entry supports a custom display name, shortcode, and emoji (for example `{"name": "Critical", "shortcode": "C", "emoji": "🔥"}`).


### RQMD-PRIORITY-012: Domain and sub-domain priority metadata

- **Status:** 🔧 Implemented
- **Priority:** 🟢 P3 - Low
- **Summary:** Optional priority metadata at domain and sub-domain scope so that a domain file can declare an overall domain priority and optional per-H2 sub-domain priorities.
