# Core Engine Requirement

Scope: parsing, status normalization, summary generation, and requirement discovery.

<!-- acceptance-status-summary:start -->
Summary: 5💡 22🔧 16✅ 0⚠️ 0⛔ 0🗑️
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

### RQMD-CORE-030: Chat-first default onboarding from rqmd init
- **Status:** 🔧 Implemented
- **Priority:** 🔴 P0 - Critical
- **Summary:** `rqmd init` to default to the AI-guided chat onboarding flow rather than dropping me into lower-level manual setup details so that the first-run experience leads users through the strongest supported path with minimal decision overhead.

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
