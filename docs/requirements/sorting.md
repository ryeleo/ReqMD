# Sorting Requirement

Scope: deterministic ordering, sort toggles, and priority-based ranking in interactive views.

<!-- acceptance-status-summary:start -->
Summary: 5💡 0🔧 9✅ 0⛔ 2🗑️
<!-- acceptance-status-summary:end -->

### RQMD-SORTING-001: File ranking by priority buckets
- **Status:** 🗑️ Deprecated
- **Priority:** 🟢 P3 - Low
- **Deprecated:** Conflicts with RQMD-SORTING-006 (default name ordering); deprecated in favor of explicit user-selected sort modes.
- As a rqmd user when file rows are shown in interactive selection
- I want to enable sort mode
- So that ordering prioritizes in-progress requirement counts first
- So that tie-breaking remains deterministic.

### RQMD-SORTING-002: Sort toggle key behavior
- **Status:** 🗑️ Deprecated
- **Priority:** 🟢 P3 - Low
- **Deprecated:** Replaced by RQMD-SORTING-007 which provides column-cycle sorting via `s` and clearer UX.
- As a rqmd user when users are in file or requirement selection menus
- I want to press the sort toggle key
- So that rqmd switches between default and alternate ordering modes
- So that menu output clearly reflects the current mode.

### RQMD-SORTING-003: Stable deterministic ordering
- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- As a rqmd user when multiple files or requirements share equal priority values
- I want rqmd to render sorted menus
- So that ordering remains stable across repeated renders
- So that avoids jitter between refresh cycles, including going up/down the menu hierarchy.

### RQMD-SORTING-004: Rescan preserves selected sort mode
- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- As a rqmd user when interactive mode rescans files after updates
- I want the active sort mode state to persist
- So that rescan preserves the active mode
- So that ordering is rebuilt using that mode consistently.

### RQMD-SORTING-005: Configurable sort strategy catalog
- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- As a rqmd user when teams may want alternative ranking policies
- I want configurable sort strategies
- So that rqmd allows selecting named sort strategies (for example `standard`, `status-focus`, `alpha-asc`) via CLI
- So that each strategy defines default active sort keys/directions and column cycle order for both file and requirement interactive menus
- So that strategy selection applies consistently across interactive menus.

### RQMD-SORTING-006: Default name ordering
- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- As a rqmd user when no explicit sort preference is set
- I want interactive menus to render file lists
- So that ordering defaults to the `name` sort column rather than a separate filesystem sort mode
- So that the default direction for that active sort is descending
- So that no automatic priority-based reordering is applied unless the user selects a different sort column.

### RQMD-SORTING-007: Column-cycle sorting with `s`
- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- As a rqmd user when a user is viewing a tabular menu or list with multiple sortable columns (e.g., file name, roll-up counts, changed flag)
- I want to press `s`
- So that the active sort column cycles to the next available column from left to right
- So that when the cycle advances past the last sortable column, pressing `s` again returns the view to the default menu sort (for file lists, `name`) so the cycle can continue indefinitely without a separate filesystem-only mode
- So that pressing `S` cycles the active sort column in the reverse direction using the same wrap behavior
- So that the UI indicates the active sort column and direction in the menu header/footer.

### RQMD-SORTING-008: Toggle ascending/descending with `d`
- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- As a rqmd user when a sort column is active
- I want to press `d`
- So that the sort direction toggles between ascending and descending
- So that when a new sort column becomes active, its initial direction defaults to descending
- So that the legend shows the current direction as `d=[asc|dsc]` and updates dynamically.

### RQMD-SORTING-009: Refresh/rescan with `r`
- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- As a rqmd user when the user has a current sort column and direction
- I want to press `r`
- So that the UI refreshes all screen content, rescans underlying files, and reapplies the current sort scheme
- So that `r` is a non-destructive operation that does not change the active sort column or direction.

### RQMD-SORTING-010: Standardized interaction legend
- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- As a rqmd user when the interactive UI must remain discoverable and consistent
- I want menus to render
- So that a standardized key legend is shown in the footer in this order and format:
- `keys: 1-9 select | n=next | p=prev | u=up | s=sort | S=sort-back | d=[asc|dsc] | r=rfrsh | q=quit`
- So that the `d` segment is updated dynamically to reflect the current sort direction.

### RQMD-SORTING-011: Visual indicator for active sort column and direction
- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- As a rqmd user when a column is actively used to sort a view
- I want menus to render
- So that the active column label is rendered in bold and an ASCII arrow indicator is shown to indicate direction (`↑` for ascending, `↓` for descending)
- So that in file-list sort headers, non-`name` column labels are right-aligned for quick scanning while `name` remains left-aligned
- So that the same visual cue is present in file and requirement list headers and any columnized views so users can quickly identify the current sort context.

### RQMD-SORTING-012: Per-requirement rank metadata field
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- As a rqmd user when I want to prioritize or deprioritize individual requirements without changing IDs or statuses
- I want each requirement to support an optional first-class `**Rank:**` field with a signed integer value
- So that rank can be stored directly in requirement markdown alongside other editable metadata.
- So that missing rank is treated as `0` for ordering purposes.
- So that positive rank values move items earlier in rank-aware lists and negative values move items later.
- So that rank metadata round-trips through parser, JSON export, and write-back without being mistaken for body text.

### RQMD-SORTING-013: Rank-aware requirement ordering semantics
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- As a rqmd user when rank-aware ordering is active
- I want requirements to be ordered deterministically using rank before default ID recency
- So that items with higher rank values appear before items with lower rank values.
- So that requirements with equal rank values fall back to the normal newest-first numeric ID ordering.
- So that rank-aware ordering remains stable and deterministic across repeated renders, refreshes, and interactive transitions.
- So that the contract works correctly when IDs grow past three digits (for example `REQ-1000` still sorts newer than `REQ-999` when rank values are equal).

### RQMD-SORTING-014: Sparse default rank spacing
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- As a rqmd user when rqmd suggests or initializes rank values for ordering and backlog grooming
- I want default rank assignments to leave intentional gaps between neighboring requirements
- So that inserting a newly ranked item between two existing ranked items usually does not require renumbering both sides immediately.
- So that the default seeded spacing uses a step of `10000` between adjacent canonical rank positions unless a future config explicitly overrides it.
- So that rqmd can place up to `9999` intervening requirements between two default-spaced neighbors before a full re-spacing pass is needed.
- So that rank changes such as "top", "bottom", "page up" and "page down" move in steps of `10000` to preserve this spacing property and minimize the need for renumbering when reprioritizing items.
- So that even if this rank model is put into a int32 system, the system will support the user doing "top ranking" on more than 100,000 requirements. (10000*X=2^31-1 => X=214748 default-spaced items between any two rank values, which should be sufficient for most use cases, and if not, compression could easily happen in the future to make more space while preserving relative order).

### RQMD-SORTING-015: Rank Compression if Int32 Overflow Detected
- **Status:** 💡 Proposed
- **Priority:** P3
- As a rqmd user when the system detects that rank values are approaching int32 overflow due to requirement rank going above 2,147,483,647 or below -2,147,483,648,
- I want rqmd to automatically compress rank values to make space for more ranked items
- So that the system can maintain the relative order of all existing ranked items while reassigning new rank values that fit within the int32 range.
- So that the compression algorithm intelligently compresses MORE around requirements with statuses that indicate rank will no longer change (for example, `done` items at the bottom of the list only seperated by `100` instead of `10000`).

### RQMD-SORTING-016: Positional `ranked` target for backlog grooming
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- As a rqmd user when I want to jump directly into rank-aware backlog grooming
- I want `rqmd ranked` to resolve as a first-class positional target
- So that rqmd can open the dedicated rank-focused interactive mode without requiring a separate flag sequence.
- So that the resulting view orders requirements with rank-aware semantics first and deterministic fallback ordering second.
- So that `ranked` is exposed in help text and shell completion alongside other special positional targets such as `all`.