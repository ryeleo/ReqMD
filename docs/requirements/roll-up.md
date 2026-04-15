# Roll-up Requirement

Scope: status aggregation, per-file summary generation, and roll-up display output.

<!-- acceptance-status-summary:start -->
Summary: 0💡 0🔧 6✅ 0⚠️ 0⛔ 1🗑️
<!-- acceptance-status-summary:end -->


### RQMD-ROLLUP-001: Summary count generation per status

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** Rqmd to compute roll-up values so that counts are generated for each supported status in canonical order.


### RQMD-ROLLUP-002: Inline summary block lifecycle

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** Rqmd to process files so that summary blocks are inserted or replaced idempotently.


### RQMD-ROLLUP-003: Summary table output control

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** To toggle summary table options so that roll-up table output is shown or suppressed as requested.


### RQMD-ROLLUP-004: Colored roll-up rendering in interactive menus

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** Roll-up text to render so that status-family color buckets are visually distinct.


### RQMD-ROLLUP-005: Cross-file/global roll-up report mode

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** A global roll-up mode so that rqmd can output aggregate status totals across all domain files.


### RQMD-ROLLUP-006: Project-configurable roll-up color knobs

- **Status:** 🗑️ Deprecated
- **Priority:** 🟢 P3 - Low
- **Deprecated:** Superseded by RQMD-ROLLUP-007 which provides a more general `rollup_map`/`rollup_equations` mechanism for defining roll-up columns and mappings; color knobs can be represented within that model.
- **Summary:** A project-level status config file to provide roll-up settings so that rqmd supports `rollup_mode` with values like `per_status`, `bucketed`, or `monochrome`, supports `bucket_map` to map statuses into roll-up buckets, and allows per-bucket `color` overrides.


### RQMD-ROLLUP-007: Custom roll-up expressions and mappings

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** A project-level config to define roll-up mappings so that rqmd supports a declarative `rollup_map` (or `rollup_equations`) where each roll-up column may be defined by an expression of statuses, for example:.
- `C1 = Implemented + Verified`
- `C2 = Proposed`
- **Summary:** Shorthand using shortcodes is allowed (e.g., `C1 = I + V`), with parsing tolerant to whitespace and case.
- ```yaml
- rollup_map:
-   C1: [implemented, verified]
-   C2: [proposed]
- ```
- or using equation syntax:
- ```yaml
- rollup_equations:
-   - "C1 = I + V"
-   - "C2 = P"
- ```
- **Summary:** Evaluation semantics are simple set-union: a requirement with any of the listed statuses contributes to that roll-up column; a requirement may contribute to multiple roll-up columns if configured to do so.
