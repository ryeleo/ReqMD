# Sorting Requirement

Scope: deterministic ordering, sort toggles, and priority-based ranking in interactive views.

<!-- acceptance-status-summary:start -->
Summary: 5💡 0🔧 9✅ 0⚠️ 0⛔ 2🗑️
<!-- acceptance-status-summary:end -->

### RQMD-SORTING-001: File ranking by priority buckets
- **Status:** 🗑️ Deprecated
- **Priority:** 🟢 P3 - Low
- **Deprecated:** Conflicts with RQMD-SORTING-006 (default name ordering); deprecated in favor of explicit user-selected sort modes.
- **Summary:** To enable sort mode so that ordering prioritizes in-progress requirement counts first.

### RQMD-SORTING-002: Sort toggle key behavior
- **Status:** 🗑️ Deprecated
- **Priority:** 🟢 P3 - Low
- **Deprecated:** Replaced by RQMD-SORTING-007 which provides column-cycle sorting via `s` and clearer UX.
- **Summary:** To press the sort toggle key so that rqmd switches between default and alternate ordering modes.

### RQMD-SORTING-003: Stable deterministic ordering
- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** Rqmd to render sorted menus so that ordering remains stable across repeated renders.

### RQMD-SORTING-004: Rescan preserves selected sort mode
- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** The active sort mode state to persist so that rescan preserves the active mode.

### RQMD-SORTING-005: Configurable sort strategy catalog
- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** Configurable sort strategies so that rqmd allows selecting named sort strategies (for example `standard`, `status-focus`, `alpha-asc`) via CLI.

### RQMD-SORTING-006: Default name ordering
- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** Interactive menus to render file lists so that ordering defaults to the `name` sort column rather than a separate filesystem sort mode.

### RQMD-SORTING-007: Column-cycle sorting with `s`
- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** To press `s` so that the active sort column cycles to the next available column from left to right.

### RQMD-SORTING-008: Toggle ascending/descending with `d`
- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** To press `d` so that the sort direction toggles between ascending and descending.

### RQMD-SORTING-009: Refresh/rescan with `r`
- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** To press `r` so that the UI refreshes all screen content, rescans underlying files, and reapplies the current sort scheme.

### RQMD-SORTING-010: Standardized interaction legend
- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** Menus to render so that a standardized key legend is shown in the footer in this order and format:.
- `keys: 1-9 select | n=next | p=prev | u=up | s=sort | S=sort-back | d=[asc|dsc] | r=rfrsh | q=quit`
- **Summary:** The `d` segment is updated dynamically to reflect the current sort direction.

### RQMD-SORTING-011: Visual indicator for active sort column and direction
- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** Menus to render so that the active column label is rendered in bold and an ASCII arrow indicator is shown to indicate direction (`↑` for ascending, `↓` for descending).

### RQMD-SORTING-012: Per-requirement rank metadata field
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- **Summary:** Each requirement to support an optional first-class `**Rank:**` field with a signed integer value so that rank can be stored directly in requirement markdown alongside other editable metadata.

### RQMD-SORTING-013: Rank-aware requirement ordering semantics
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- **Summary:** Requirements to be ordered deterministically using rank before default ID recency so that items with higher rank values appear before items with lower rank values.

### RQMD-SORTING-014: Sparse default rank spacing
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- **Summary:** Default rank assignments to leave intentional gaps between neighboring requirements so that inserting a newly ranked item between two existing ranked items usually does not require renumbering both sides immediately.

### RQMD-SORTING-015: Rank Compression if Int32 Overflow Detected
- **Status:** 💡 Proposed
- **Priority:** P3
- **Summary:** Rqmd to automatically compress rank values to make space for more ranked items so that the system can maintain the relative order of all existing ranked items while reassigning new rank values that fit within the int32 range.

### RQMD-SORTING-016: Positional `ranked` target for backlog grooming
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- **Summary:** `rqmd ranked` to resolve as a first-class positional target so that rqmd can open the dedicated rank-focused interactive mode without requiring a separate flag sequence.
