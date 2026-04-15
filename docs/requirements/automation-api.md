# Automation API Requirement

Scope: non-interactive updates, machine-friendly batch operations, and CI-friendly check behavior.

<!-- acceptance-status-summary:start -->
Summary: 0💡 29🔧 10✅ 0⚠️ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->


### RQMD-AUTOMATION-001: Check-only mode

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- Given docs may be out of sync
- When `--verify-summaries` is used
- Then no files are written
- And process exits non-zero if any summary changes would be required.


### RQMD-AUTOMATION-002: Single requirement update mode

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- Given requirement ID and status are provided
- When `--update-id` and `--update-status` are used
- Then only that requirement is updated
- And summary block for its file is refreshed.


### RQMD-AUTOMATION-003: Repeatable bulk set mode

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- Given multiple `--update REQUIREMENT-ID=STATUS` arguments
- When command runs
- Then each update is applied in argument order
- And command exits successfully when all updates succeed.


### RQMD-AUTOMATION-004: Batch updates via file

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- Given a JSONL/CSV/TSV update file
- When `--update-file` is used
- Then each row is parsed and applied
- And row-level validation errors include file and line context.


### RQMD-AUTOMATION-005: Batch row schema aliases

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- Given batch rows use `requirement_id`, `requirement_id`, `id`, `ac_id`, or `r_id`
- When parser reads rows
- Then any supported key is accepted for requirement identifier
- And status remains required.


### RQMD-AUTOMATION-006: Conflicting mode guardrails

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- Given user combines incompatible command modes
- When arguments are validated
- Then command fails fast with explicit message
- And no file writes are performed.


### RQMD-AUTOMATION-007: File scope disambiguation

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- Given duplicate requirement IDs might exist across files
- When user provides `--scope-file` scope
- Then update resolves only within that file
- And ambiguity errors are avoided.


### RQMD-AUTOMATION-008: Filtered tree output

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- Given `--status` with `--as-tree`
- When command runs in non-interactive mode
- Then tool prints grouped requirements tree by file
- And exits without opening interactive menus.


### RQMD-AUTOMATION-009: Summary table control

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- Given automation may not want console tables
- When `--non-interactive` is used
- Then summary table output is suppressed
- And command behavior otherwise remains unchanged.


### RQMD-AUTOMATION-010: JSON output for filtered status queries

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- Given machine consumers need parse-friendly output
- When `--json` is used in non-interactive command flows
- Then rqmd prints valid JSON for summary/check/set/filter-status modes
- And filter mode includes status, criteria_dir, total, and grouped requirements by file
- And rqmd exits without interactive prompts or tree formatting noise.


### RQMD-AUTOMATION-011: Empty filter JSON result

- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- **Summary:** `--json` filter queries with no matches to return `total: 0` and `files: []` so that zero-match runs are handled as valid outcomes without brittle parsing.


### RQMD-AUTOMATION-012: Stable JSON schema contract

- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- **Summary:** Documented required JSON keys and value types per mode so that integrations are predictable and versioned when schema changes.


### RQMD-AUTOMATION-013: Deterministic JSON ordering

- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- **Summary:** JSON arrays emitted in deterministic order so that repeated runs on unchanged inputs produce stable diffs.


### RQMD-AUTOMATION-014: Dry-run for mutation commands

- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- **Summary:** Dry-run behavior for write commands (`--update`, `--update-file`, `--update-priority`, `--seed-priorities`) so that I can preview exact changes before applying them.


### RQMD-AUTOMATION-015: Batch partial-failure report model

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** Per-row success/failure results in JSON and text batch modes so that retry logic can target only failed rows.


### RQMD-AUTOMATION-016: Exit code matrix

- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- **Summary:** Explicit documented exit codes by outcome type so that pipeline control flow remains unambiguous.


### RQMD-AUTOMATION-017: Prompt suppression guarantee

- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- **Summary:** Non-interactive and JSON modes to never prompt so that jobs never hang waiting for input.


### RQMD-AUTOMATION-018: Migration mode automation contract

- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- **Summary:** `init --scaffold --force-yes` and `--seed-priorities` to be idempotent, deterministic, and JSON-reportable so that migration steps are reliable in CI/CD workflows.


### RQMD-AUTOMATION-019: Unique-prefix argument/value abbreviations

- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- **Summary:** Unique minimal prefixes for long option names and enumerated values to be accepted (for example, `--filt V` -> `--status Verified`) so that fast terminal usage is supported without sacrificing determinism.
- **Note:** The enumerated-value prefix half (e.g. `V` → `Verified`) is already implemented and tested. The option-name abbreviation half (e.g. `--stat` → `--status`) via single-character shortcode is a reasonable approach, but is explicitly deferred to **absolute lowest priority** — implement this last, only after the JSON API contract is fully stable and no further breaking changes are expected. Adding abbreviation resolution to a large option set risks surfacing ambiguity regressions during active development.


### RQMD-AUTOMATION-020: Ambiguous option-prefix error contract

- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- **Summary:** Ambiguous long-option prefixes to fail deterministically so that the error output lists candidate option names and recommended full invocations.


### RQMD-AUTOMATION-021: Ambiguous value-prefix error contract

- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- **Summary:** Ambiguous enumerated value prefixes (for example status values) to fail deterministically so that the error output lists candidate canonical values and recommended full values.


### RQMD-AUTOMATION-022: JSON-formatted ambiguity errors

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** Ambiguity failures in `--json` mode to return a stable machine-readable error payload so that tools can branch on error type, inspect candidates, and auto-remediate input expansion.


### RQMD-AUTOMATION-023: Filter flagged requirements

- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- **Summary:** A `--flagged` mode for non-interactive workflows so that flagged requirements can be listed, walked, or exported without relying on status changes.


### RQMD-AUTOMATION-024: JSON output for flagged items

- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- **Summary:** `--flagged --json` to return flagged requirements in the same stable grouped structure used by other filter modes so that bots and scripts can consume focus lists consistently.


### RQMD-AUTOMATION-025: Direct flagged-state mutation

- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- **Summary:** To set flagged state directly with `--update-flagged REQUIREMENT-ID=true|false` so that workflows can mutate flagged state deterministically without requiring interactive mode.


### RQMD-AUTOMATION-026: Full domain-document JSON contract

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** Each domain entry to include all domain-document sections needed to reconstruct context, including `scope` and domain-level `body` aligned to RQMD-CORE-019 so that machine consumers do not need to re-parse markdown to recover domain context beyond requirement rows.


### RQMD-AUTOMATION-027: ReqID list input mode

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** A non-interactive/selection mode that accepts a CLI token list of requirement IDs and/or domain identifiers so that filtering and downstream operations can be scoped to exact IDs or whole domains instead of status or priority filters.


### RQMD-AUTOMATION-028: ReqID list file parsing and comment support

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** Rqmd to accept a simple `.txt`/`.conf`/`.md` list file where requirement IDs, domain tokens, and subsection tokens may appear one-per-line or as comma/whitespace-separated tokens on any line so that teams can maintain lightweight worklists without strict CSV/JSONL schema overhead.


### RQMD-AUTOMATION-029: Filtered query by subsection

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** A `--sub-domain <NAME>` flag to filter results by subsection so that similar to `--status`, only requirements matching the subsection name are included.


### RQMD-AUTOMATION-030: Sub-domain metadata in JSON output

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** Each requirement entry to include a `sub_domain` field (string or null) so that metadata consumers can understand and reconstruct subsection structure.


### RQMD-AUTOMATION-031: Minimal differentiable token matching for CLI args and values

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** All CLI argument values that support enumerations/aliases to accept their smallest differentiable tokens and shortcodes so that canonical labels are tokenized by whitespace-separated units and each unit is eligible for deterministic matching.
- `🟡`
- `P2`
- `-`
- `Medium`
- **Summary:** Inputs like `--priority P2` resolve to the canonical configured priority label (for example `🟡 P2 - Medium`).


### RQMD-AUTOMATION-032: Link-based filtering with `--has-link` and `--no-link`

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** To filter requirements by link presence so that `--has-link` returns only requirements with one or more links configured.


### RQMD-AUTOMATION-033: Schema versioning in JSON contract

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** The JSON contract to include a schema version field so that breaking changes to the JSON structure are explicitly versioned.


### RQMD-AUTOMATION-034: Inverse flagged filter with `--no-flag`

- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- **Summary:** An inverse flagged filter mode so that `--no-flag` returns only requirements with `Flagged: false` or no flagged metadata.


### RQMD-AUTOMATION-035: Positional filter-token precedence and flexible matching

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** Rqmd to recognize status and priority filter tokens positionally before attempting requirement-ID or domain-token resolution so that fast ad hoc filter launches do not require explicit `--status` or `--priority` flags.


### RQMD-AUTOMATION-036: Positional `all` target for newest-first overview

- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- **Summary:** `rqmd all` to resolve as a special positional target so that rqmd selects all requirements regardless of status without needing a separate flag.


### RQMD-AUTOMATION-037: Canonical machine-readable validation entry point

- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- **Summary:** One canonical validation entry point, ideally exposed as a `validate` subcommand on the same agent workflow surface used for preflight so that validation does not fragment into ad hoc shell snippets that other tools have to scrape and reinterpret.
- Given a developer or AI agent needs to validate a planned change before closing a batch
- When they run the repository's canonical validation entry point
- Then it should orchestrate the approved compile, focused test, broader test, and rqmd verification steps for that batch
- And it should support a single agent-facing workflow shape where `preflight` and `validate` live under the same maintained command or script instead of separate unrelated entry points
- And it should emit machine-readable status for each stage so other tools can make decisions without scraping ad hoc shell output
- And machine-readable output should include per-stage status in a stable structure rather than only one aggregated success or failure bit
- And it should allow focused modes for compile-only, docs-only, SDK-only, and repository-specific targeted validation without inventing parallel workflows.


### RQMD-AUTOMATION-038: Multi-query batch mode for rqmd-ai

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** Rqmd-ai to accept multiple queries in one invocation so that startup, import, and catalog-parse costs are paid once instead of N times so that an AI workflow that currently runs 5-15 separate rqmd-ai commands per step can collapse those into one or two batch invocations.


### RQMD-AUTOMATION-039: `--dump-type` filter for rqmd-ai

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** `rqmd-ai` to accept a `--dump-type bug` (or `--dump-type feature`) flag that filters output by the `type` metadata field introduced in RQMD-CORE-041 so that `--dump-type` composes with existing filters like `--dump-status`, enabling queries such as `--dump-type bug --dump-status proposed` (open unfixed bugs) or `--dump-type feature --dump-status proposed` (net-new feature proposals).
