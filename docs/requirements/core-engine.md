# Core Engine Requirement

Scope: parsing, status normalization, summary generation, and requirement discovery.

<!-- acceptance-status-summary:start -->
Summary: 14💡 26🔧 16✅ 0⚠️ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->


### RQMD-CORE-001: Domain file discovery

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** The tool to scan for domain docs so that all markdown files in that directory are discovered in stable sorted order.


### RQMD-CORE-002: Status line parsing

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** The parser to read the document so that the status is extracted from `- **Status:** ...`.


### RQMD-CORE-003: Canonical status normalization

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** Normalization to run so that the status is rewritten to canonical labels.


### RQMD-CORE-004: Summary block insertion

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** Processing to run so that a summary block is inserted near the top of the file.


### RQMD-CORE-005: Summary block replacement

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** Status counts change so that only the existing summary block content is replaced.


### RQMD-CORE-006: Status count model

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** Counts to be computed so that counts include all supported statuses in fixed order.


### RQMD-CORE-007: Requirement header matching

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** Parsing to run so that each matching requirement is discoverable by ID.


### RQMD-CORE-008: Idempotent processing

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** Processing to run repeatedly so that generated output remains byte-stable for those files.


### RQMD-CORE-009: Missing domain docs handling

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** To run the command so that reqmd prints a clear, actionable error message.


### RQMD-CORE-010: Blocked/deprecated reason extraction

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** Parsing to run so that those reason lines are captured with line references.


### RQMD-CORE-011: Project scaffold initialization

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** To run an initialization command so that boilerplate docs are created including `docs/requirements/README.md`.


### RQMD-CORE-012: Starter dummy requirement generation

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** To create starter domain docs so that at least one easy-to-delete sample requirement `<PREFIX>-HELLO-001` is included.


### RQMD-CORE-013: Domain-sync maintenance over time

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** To run sync/maintenance commands so that index and domain-document references are kept consistent with current domain files.


### RQMD-CORE-014: Automatic ID prefix detection from requirements index

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** Rqmd to read `docs/requirements/README.md` and linked domain docs so that requirement ID prefixes are auto-detected from discovered requirement headers.


### RQMD-CORE-015: Scaffold init key prompt with customizable default

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** Scaffold initialization to start so that rqmd prompts for a starter requirement key prefix.


### RQMD-CORE-016: Initial scaffolding content/copy

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** Scaffold initialization to execute so that generated `docs/requirements/README.md` includes a welcome message and instructions for getting started that is copied from:.
    - ./src/rqmd/resources/init/README.md for the domain index (requirements/README.md)
    - ./src/rqmd/resources/init/domain-example.md for the starter domain doc (requirements/domain-example.md)
- **Summary:** Those instructions are included in the python package README somewhere, so they are published on pypi.org as a simple web page.


### RQMD-CORE-017: Branded init and README messaging

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** Branded, persuasive copy and direct project links so that the tool clearly positions itself as human-readable, AI-readable, and ready for Requirements Driven Development (RDD).


### RQMD-CORE-018: First-class binary flagged field

- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- **Summary:** A simple binary flagged field on requirements so that I can mark items for attention without introducing a new `Flagged` status into the status catalog.


### RQMD-CORE-019: Domain-level body parsing and preservation

- **Status:** 🔧 Implemented
- **Priority:** 🔴 P0 - Critical
- **Summary:** Each domain markdown file to support an explicit optional domain-level body section (separate from per-requirement bodies) so that implementation rationale, migration guidance, and AI-generated domain notes can live at domain scope without polluting requirement entries.


### RQMD-CORE-020: H2 subsection parsing and metadata capture

- **Status:** 🔧 Implemented
- **Priority:** 🔴 P0 - Critical
- **Summary:** Rqmd to recognize H2 headers as subsection boundaries so that each requirement captures a `sub_domain` metadata field indicating which H2 section contains it.


### RQMD-CORE-021: Per-requirement external links field

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** Each requirement to support an optional top-level `**Links:**` field so that the field appears directly below Status/Priority and contains one or more link entries as list items.


### RQMD-CORE-022: Enhanced blocking with linked requirements

- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- **Summary:** To optionally link it to another requirement that is blocking it so that the block reason field supports both free-form text and markdown hyperlinks to other requirement IDs.


### RQMD-CORE-023: Global requirement ID prefix renaming tool

- **Status:** 🔧 Implemented
- **Priority:** 🟢 P3 - Low
- **Summary:** A one-time bulk rename command so that all requirement headers, links, and citations are updated consistently across all domain files.


### RQMD-CORE-024: Generated top-level README from requirement domains

- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- **Summary:** Rqmd to generate the project-level README requirement index sections from domain files automatically and on demand so that top-level README sections describing requirement domains and status rollups are regenerated deterministically from `docs/requirements/*.md`.


### RQMD-CORE-025: Optional native acceleration layer for parse/export hot paths

- **Status:** 🔧 Implemented
- **Priority:** 🟢 P3 - Low
- **Summary:** Rqmd to support an optional native acceleration layer for hot paths such as parsing, indexing, and JSON contract generation so that large repositories can get better throughput without replacing the existing Python CLI and interactive workflow surface.


### RQMD-CORE-026: Stable immutable requirement IDs

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** Each requirement ID to behave as a stable identifier instead of an editable label so that links, discussion references, history entries, and automation can rely on one immutable ID per requirement.


### RQMD-CORE-027: Sequential numeric ID allocation

- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- **Summary:** Rqmd to allocate IDs using compound per-domain prefixes such as `RQMD-CORE-001`, `RQMD-CORE-002`, `RQMD-UI-001` so that ID order communicates relative creation order within each domain.


### RQMD-CORE-028: Sequential ID width overflow past 999

- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- **Summary:** Sequential IDs to continue as `REQ-1000`, `REQ-1001`, and higher without rollover or truncation so that 3 digits are treated as the default minimum width rather than a hard upper limit.


### RQMD-CORE-029: Canonical init command with scaffold compatibility path

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** The public CLI to standardize on `init` as the primary initialization term so that the command surface is simpler, more conventional, and easier to remember than a long-term mix of `init` and `bootstrap` wording.


### RQMD-CORE-030: Scaffold-first default onboarding from rqmd init

- **Status:** 🔧 Implemented
- **Priority:** 🔴 P0 - Critical
- **Summary:** `rqmd init` (no flags) runs the scaffold flow directly, creating starter requirement docs without requiring `--scaffold`. The AI-guided path was removed from the CLI; onboarding is now scaffold-first, with AI-assisted setup available via the VS Code extension.


### RQMD-CORE-031: First-class user-story and Given/When/Then blocks

- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- **Summary:** Each requirement to fully support both a user-story block and a Given/When/Then acceptance block as first-class structured content so that the requirement can communicate both product intent and executable acceptance behavior without forcing teams to choose one style over the other.


### RQMD-CORE-032: Init scaffolds explicit project config by default

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** Init flows to create a `rqmd.yml` file at the project root by default so that the chosen requirements directory, ID prefix, status catalog, and priority catalog are explicit for both humans and AI agents from the first run.


### RQMD-CORE-033: Versioned requirement markdown schema and migration path

- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- **Summary:** Rqmd-managed requirement files and generated scaffolds to carry an explicit markdown schema version marker so that rqmd can detect older catalog formats deterministically instead of guessing from incidental document shape.


### RQMD-CORE-034: Guided duplicate-ID repair workflow

- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- **Summary:** Rqmd to offer a guided repair workflow instead of only failing fast so that the tool can preview safe rename or reassignment options for each collision before writing changes.


### RQMD-CORE-035: Packaged-resource source of truth for shipped templates and built-in catalogs

- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- **Summary:** Rqmd to keep those shipped defaults in packaged resource files rather than scattered Python literals so that built-in statuses, priorities, scaffold templates, schema snippets, and other shipped markdown or YAML defaults can be edited as data with fewer code touchpoints.


### RQMD-CORE-036: Requirements index tooling metadata and version-mismatch warning

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** The requirements index README to record the project's current rqmd and JSON schema versions and for rqmd to warn when that recorded metadata no longer matches the running tool so that I can tell from the local repository docs which rqmd version last refreshed the tracked requirements metadata without needing AI-specific bundle files or external release notes.


### RQMD-CORE-037: Lazy import strategy for non-interactive codepaths

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** Rqmd to defer importing modules that are only needed for interactive TUI, color rendering, telemetry client, and other heavyweight subsystems until they are actually used so that the ~80ms import overhead measured on typical machines is reduced to the minimum required for the codepath being exercised.


### RQMD-CORE-038: Filesystem-cached parsed catalog for repeated invocations

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** Rqmd to cache parsed requirement data in a lightweight filesystem cache keyed by file mtime and size so that the second and subsequent invocations within the same working tree skip re-parsing unchanged requirement files.


### RQMD-CORE-039: Non-interactive latency budget and CI gate

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** A defined latency budget for non-interactive JSON and automation paths, separate from the interactive RQMD-UI-009 budget so that AI-path commands such as `rqmd-ai --json --dump-status` and `rqmd --json --non-interactive` have an explicit measurable target (e.g., <=80ms for single-requirement lookups, <=150ms for full catalog exports on a warm cache).


### RQMD-CORE-040: Native Rust or C acceleration for parse and index hot paths

- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- **Summary:** Rqmd to support a native Rust or C extension that accelerates the requirement markdown parser and in-memory index construction so that the parse+index phase can drop from tens of milliseconds to single-digit milliseconds for catalogs of several hundred requirements.


### RQMD-CORE-041: `type` metadata field and parser support

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** Rqmd to recognize a `type` metadata field in requirement headers (e.g., `<!-- type: bug -->`) so I can distinguish bugs from features without abusing the status lifecycle so that `type` defaults to `feature` when omitted, keeping backwards compatibility with every existing requirement doc.


### RQMD-CORE-042: `affects` cross-reference field for bugs

- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- **Summary:** To add an `affects: PROJ-XXX` metadata comment to a bug so it is linked back to the requirement it is a defect against so that `affects` is semantically distinct from `blocked-by` — a bug *affects* the parent requirement's validity rather than blocking its own implementation.


### RQMD-CORE-043: Bug-specific template in scaffold and skills

- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- **Summary:** Rqmd to offer a Steps to Reproduce / Expected / Actual / Root Cause template when creating a bug, since the user-story + Given/When/Then shape does not fit defect reports naturally so that `rqmd init --scaffold` includes an example bug entry alongside the feature example.


### RQMD-CORE-044: `rqmd --inbox` CLI append command

- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- **Summary:** As a developer working in a terminal, I want `rqmd --inbox "my idea"` to append a `- my idea` line to `docs/inbox.md` (creating the file with a `# Inbox` header if absent) so that I can capture ideas from any shell without opening an editor or chat panel.

- Given the developer runs `rqmd --inbox "some idea"`
- When the command executes
- Then it appends `- some idea` to `docs/inbox.md` relative to the project root
- And if `docs/inbox.md` does not exist, it creates it with `# Inbox\n\n- some idea\n`

- And it prints a confirmation: `📥 Added to inbox (N items)`
- And multiple arguments are joined: `rqmd --inbox one-liner about capybaras` works without quotes

<a id="rqmd-core-045"></a>

### RQMD-CORE-045: `rqmd --staleness` — per-requirement staleness scoring

- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- **Summary:** As a developer or AI agent wanting to prioritize tech-debt cleanup, I want `rqmd --staleness` to produce a per-requirement staleness report with a normalized 0–100 composite score based on git history and code cross-references so that the most impactful cleanup targets surface automatically.

- Given the developer runs `rqmd --staleness` in a tracked project
- When the command executes
- Then it outputs a table (or `--json` structured data) with one row per requirement showing:
  - **ID, title, status**
  - **Last status change** — date from `git blame` on the status line
  - **Code cross-refs** — count of source files referencing the requirement ID (grep-based)
  - **Code freshness** — most recent commit date touching files that reference the ID
  - **Staleness score** — a normalized 0–100 composite, higher = more stale / more likely debt
- And the composite score is computed from named, weighted signals with documented defaults (e.g., `status_age_weight=0.3`, `xref_count_weight=0.3`, `code_freshness_weight=0.2`, `status_flag_weight=0.2`)
- And all signal weights are documented in `--staleness --explain` output and adjustable per-project via `.rqmd/config.toml` `[staleness]` section
- And 🗑️ Deprecated requirements with code cross-ref count > 0 are flagged as **"deprecated but alive"** (automatic score boost to near-100)
- And 🔧 Implemented requirements with zero code cross-refs are flagged as **"implemented but unreferenced"** (possible orphan)
- And the output is sorted by staleness score descending
- And `--staleness --json` produces machine-readable output consumable by prompts/skills
- And `--staleness --deprecated-only` filters to 🗑️ Deprecated requirements with live code cross-refs, reports ID/file/line/content grouped by requirement ID, and exits non-zero when matches are found (useful for CI)

<a id="rqmd-core-046"></a>

### RQMD-CORE-046: Exclude `archived/` from default requirement processing

- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- **Summary:** As a developer who archives deprecated requirement docs, I want `rqmd` to skip `docs/requirements/archived/` by default so that archived specs don't inflate summary counts or appear in `--json` output.

- Given `docs/requirements/archived/` contains moved requirement files
- When `rqmd` runs in any mode (summary, `--json`, `--verify-summaries`, `--staleness`)
- Then files under `archived/` are excluded from processing by default
- And a `--include-archived` flag re-includes them for audit/migration use
- And `rqmd --json` includes an `"archived_files"` count in metadata so agents know archived docs exist
- And the `docs/requirements/README.md` index does not list archived files (but a footnote mentions the archived count)

<a id="rqmd-core-047"></a>

### RQMD-CORE-047: Configurable decay curve for staleness time-based signals

- **Status:** 💡 Proposed
- **Priority:** 🟢 P3 - Low
- **Summary:** As a project maintainer tuning staleness scoring for my codebase's evolution patterns, I want time-based staleness signals (status age, code freshness) to support configurable decay curves so that projects with different development cadences can weight recency appropriately.

- Given `rqmd --staleness` computes time-based signals
- When a decay curve is configured in `.rqmd/config.toml` `[staleness]` section (e.g., `decay_curve = "logarithmic"`)
- Then that curve is applied to status age and code freshness before the composite score
- And the default is `linear` for simplicity
- And supported options are `linear`, `logarithmic`, `exponential`
- And `--staleness --explain` documents the active curve and its effect on scoring

<a id="rqmd-core-048"></a>

### RQMD-CORE-048: Interactive metadata sync prompt on version mismatch

- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- **Summary:** As a developer who just upgraded rqmd, I want the CLI to prompt me to sync the requirements index metadata when it detects a version mismatch so that the metadata stays current without requiring me to remember the `--sync-index-metadata` incantation.

- Given the developer runs `rqmd` (any subcommand) in interactive mode
- When the requirements index exists and its recorded `rqmd_version` or `json_schema_version` does not match the running tool
- Then rqmd prompts: `"rqmd version changed (0.2.6 → 0.2.7). Update requirements/README.md metadata? [Y/n]"`
- And on `Y` (or Enter for default), rqmd applies the metadata sync inline before continuing normal processing and prints: `"ℹ️ Updated requirements index metadata (rqmd 0.2.6 → 0.2.7)"`
- And on `n`, rqmd continues with a one-line reminder: `"Skipped — run \`rqmd --sync-index-metadata --force-yes\` when ready."`
- And the prompt is suppressed when `--non-interactive`, `--json`, or `--force-yes` is active (these modes already have their own contracts)
- And when `--force-yes` is active without `--non-interactive`, the sync is applied automatically without prompting (consistent with `--force-yes` semantics elsewhere)
- And the prompt fires at most once per invocation (before any other processing)

<a id="rqmd-core-049"></a>

### RQMD-CORE-049: `--json` output includes metadata mismatch info

- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- **Summary:** As an AI agent or automation consumer parsing `rqmd --json` output, I want the JSON payload to include metadata mismatch info when the recorded index metadata doesn't match the running tool so that agents can detect and fix version drift programmatically without parsing stderr warnings.

- Given the developer or agent runs `rqmd --json` in any mode (summary, filter, check, etc.)
- When the requirements index exists and its recorded metadata does not match the running tool
- Then the top-level JSON payload includes a `"metadata_mismatch"` object with `"recorded_rqmd_version"`, `"recorded_schema_version"`, `"running_rqmd_version"`, `"running_schema_version"`, and `"sync_command": "rqmd --sync-index-metadata --force-yes --non-interactive"`
- And when metadata matches (or no index exists), the `"metadata_mismatch"` key is absent (not null — absent)
- And the existing stderr warning for non-JSON mode is preserved unchanged
- And agents can check for the key's presence as a simple `if "metadata_mismatch" in data:` gate

<a id="rqmd-core-050"></a>

### RQMD-CORE-050: `rqmd init` README template includes install breadcrumb

- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- **Summary:** As a developer browsing a requirements index for the first time, I want a lightweight human-readable note that tells me the index is managed by rqmd so that I know what tool to install without needing to ask a teammate or search the repo.

- Given a developer runs `rqmd init` to bootstrap a new requirements directory
- When the generated `README.md` is written
- Then the file includes a brief info callout near the top (after the title), such as: `> **ℹ️ Info:** This index is managed by [rqmd](https://pypi.org/project/rqmd/) — a lightweight requirements tracker for AI-assisted development.`
- And the callout is a single Markdown blockquote line — not a section header, not instructions
- And the callout does not duplicate the Schema Reference or How To Use content already in the template
- And existing projects that already ran `rqmd init` can pick up the breadcrumb by running `rqmd --sync-index-metadata --force-yes` or by manually adding the line (it is not a metadata field — it is static template content)

<a id="rqmd-core-051"></a>

### RQMD-CORE-051: Dogfood — refresh rqmd-cli requirements index from current template

- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- **Summary:** As the rqmd maintainer, I want the rqmd-cli project's own `docs/requirements/README.md` to reflect the current `rqmd init` template so that the project eats its own dogfood and the README serves as a living example of best practice.

- Given the `rqmd init` template (`src/rqmd/resources/init/README.md`) has evolved since this project's requirements README was originally written
- When this requirement is implemented
- Then the project's `docs/requirements/README.md` is updated to include all template sections: **Requirement Structure**, **Subsection Organization**, **File Organization**, **Status Workflow**, **Schema Reference** (Requirement Entry Fields, Supported Markdown Structure, JSON Output Contract)
- And project-specific content that is not in the template (Requirement Documents listing, ID Prefixes table, Verification section, Archived section, Tracking Rule) is preserved and positioned after the template-derived sections
- And the `## How To Use` section uses the template's subsection structure (H3 headers for Requirement Structure, Subsection Organization, File Organization) instead of the current flat bullet list
- And the metadata block and any project-specific callouts remain unchanged
- And the refresh is a one-time manual merge — not an automated `rqmd init --refresh` command (that would be a separate proposal)

<a id="rqmd-core-052"></a>

### RQMD-CORE-052: `rqmd release --preflight` — machine-readable release readiness check

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** As a developer preparing a release, I want a single CLI command that checks whether my CHANGELOG is stamped, version strings agree across configured files, and the working tree is clean, so that I catch release blockers before tagging.

- Given a project has `rqmd.yml` (or equivalent) with configured version files
- When the user runs `rqmd release --preflight`
- Then rqmd checks that `CHANGELOG.md` contains a `## [x.y.z]` entry matching the project version
- And rqmd verifies all configured version-source files contain the same version string
- And rqmd reports whether the git working tree is clean
- And the output is structured JSON (with `"ok": true/false` and per-check detail) so agents and CI can parse it
- And the exit code is 0 when all checks pass, 1 when any check fails

<a id="rqmd-core-053"></a>

### RQMD-CORE-053: `rqmd release --stamp` — roll changelog and bump versions in one shot

- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- **Summary:** As a developer cutting a release, I want a single command that renames `[Unreleased]` to `[x.y.z] - YYYY-MM-DD` in my CHANGELOG and updates all configured version-source files, so that I don't forget a file or mis-stamp the date.

- Given a project has version-source files configured (or auto-discovered)
- When the user runs `rqmd release --stamp 0.3.0`
- Then rqmd renames the `[Unreleased]` section in `CHANGELOG.md` to `[0.3.0] - <today>` and inserts a fresh empty `[Unreleased]` above it
- And rqmd updates the version string in every configured version-source file (`pyproject.toml`, `package.json`, etc.)
- And the command is preview-first: without `--write`, it shows a dry-run diff of what would change
- And the command fails with a clear message if `[Unreleased]` is empty (no entries to release)

<a id="rqmd-core-054"></a>

### RQMD-CORE-054: Auto-discover version-source files on first run

- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- **Summary:** As a developer setting up rqmd in a new project, I want rqmd to discover every place the current version string appears — both well-known package files and unexpected locations like prompt descriptions, badge URLs, or docker tags — and confirm which ones to track, so that nothing drifts silently across releases.

#### Phase 1 — structural scan (well-known files)

- Given a project has no `version_sources` configured in `rqmd.yml`
- When the user runs `rqmd release --preflight` or `rqmd release --stamp` for the first time
- Then rqmd scans the project root for well-known version-source file patterns (`pyproject.toml`, `package.json`, `Cargo.toml`, `setup.cfg`, `version.txt`, etc.)
- And for each discovered file, rqmd extracts the current version string and reports it

#### Phase 2 — broad grep (version string search)

- Given Phase 1 has identified at least one authoritative version string (e.g. `0.2.9`)
- When discovery runs (or when the user runs `rqmd release --discover`)
- Then rqmd greps the project tree for literal occurrences of that version string, respecting `.gitignore` (skips `.git/`, docker volume mounts, `node_modules/`, build artifacts, etc.) and skipping binary files
- And the exclusion layers are applied in order (cheapest first) so the scan stays fast even in workspaces with large bound volumes
- And each hit is reported with file path, line number, and a context snippet
- And hits already covered by Phase 1 are grouped under their well-known source (not duplicated)
- And remaining hits are listed as **"unexpected version references"** for the user to review
- And **CHANGELOG version headers are excluded from bump targets** — `## [0.2.8] - 2026-04-10` is a historical record, not a version source to rewrite

> **Counterexample — what NOT to bump:**
> ```markdown
> ## [0.2.8] - 2026-04-10    ← historical changelog entry, NEVER rewrite
> ## [0.2.9] - 2026-04-17    ← the *current* release stamp (written by --stamp, not --discover)
> ```

#### Confirmation and persistence

- Then rqmd presents all discovered locations (both phases) and prompts the user to confirm which to track: `"Track this location? [Y/n]"` per group
- And confirmed locations are saved to `rqmd.yml` under a `version_sources` key, each with `file` and `line` (the line number where the version was found at discovery time)
- And on subsequent runs, rqmd re-greps each tracked file for the old version string to relocate the line (lines shift as files are edited) — if the old version string is not found in the file, rqmd warns and skips that source
- And `rqmd release --discover` re-runs both phases on demand (e.g. after adding new files) and highlights new/missing locations vs. the saved config
- And in `--non-interactive` mode, Phase 1 sources are auto-accepted and Phase 2 sources are reported but not auto-tracked (requires explicit confirmation)

> **Example `rqmd.yml` after first discovery:**
> ```yaml
> version_sources:
>   - file: pyproject.toml
>     line: 7           # version = "0.2.9"
>   - file: package.json
>     line: 3           # "version": "0.2.9"
>   - file: prompts/go.prompt.md
>     line: 2           # description: "... rqmd (v0.2.9) ..."
>   - file: README.md
>     line: 12          # ![version](https://img.shields.io/badge/v0.2.9)
> ```
>
> On `rqmd release --stamp 0.3.0`, rqmd greps each file for `0.2.9` to find the current line, then replaces `0.2.9` → `0.3.0` in that occurrence. If `0.2.9` is not found in a tracked file, rqmd warns: `"⚠️ Could not find '0.2.9' in prompts/go.prompt.md — skipped."` and the developer decides whether to remove or fix the entry.

<a id="rqmd-core-055"></a>

### RQMD-CORE-055: Release version-source drift warning across releases

- **Status:** 💡 Proposed
- **Priority:** 🟢 P3 - Low
- **Summary:** As a developer who has added or removed version-source files since the last release, I want rqmd to warn me if a previously-bumped file is missing or a new version file appeared that isn't tracked, so that version strings don't silently drift.

- Given a project has released at least once with `rqmd release --stamp`
- When the user runs `rqmd release --preflight` for the next release
- Then rqmd re-runs Phase 2 discovery (broad grep for the current version string) and compares results against the `version_sources` saved in `rqmd.yml`
- And if a tracked file no longer contains the expected version string, rqmd emits: `"⚠️ version source prompts/go.prompt.md was bumped in 0.2.9 but '0.2.9' not found now — file deleted or version edited manually?"`
- And if a new file containing the version string is discovered that isn't in `version_sources`, rqmd emits: `"ℹ️ new version reference in docker-compose.yml:5 — consider adding to version_sources"`
- And **CHANGELOG entries are excluded from drift warnings** (same exclusion as RQMD-CORE-054 Phase 2)
- And the stored `version_sources` in `rqmd.yml` is the sole source of truth — no separate git-tag state needed


<a id="rqmd-core-056"></a>

### RQMD-CORE-056: Staleness distinguishes "unannotated" from "orphaned" requirements

- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- **Summary:** As a developer running `rqmd --staleness`, I want the tool to distinguish between genuinely orphaned requirements (no living code at all) and unannotated requirements (code exists but lacks a `# RQMD-*` cross-reference comment), so that the report recommends annotation for the common case instead of suggesting deprecation.

- Given a requirement has `Status: 🔧 Implemented` or `Status: ✅ Verified`
- When `--staleness` computes the cross-reference signal and finds zero grep hits for the requirement ID
- Then the report classifies the requirement as **"unannotated"** (default assumption for non-deprecated statuses with zero xrefs) rather than the current `"implemented-but-unreferenced"` label
- And the recommendation text says `"Add # RQMD-CORE-NNN annotation to the implementing test/source"` instead of `"Consider deprecating"`
- And `--staleness --json` includes `"flag": "unannotated"` (replacing `"implemented-but-unreferenced"`) so that tooling and `/tech-debt` can render the bucket distinctly
- And `--staleness` summary output shows a separate count line: `"N implemented reqs missing xref annotations (unannotated)"` beneath the deprecated-alive count
- And the existing `"deprecated-but-alive"` flag and behavior are unchanged
- And a future heuristic pass (title-keyword grep, test-name fuzzy match) could further split "unannotated" into confirmed-unannotated vs. likely-orphaned — but that is out of scope for this requirement
