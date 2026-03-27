# Requirements

This document is the source-of-truth index for rqmd requirements.
Generated from init-docs/README.md.

## How To Use

### Requirement Structure

- Keep requirement IDs stable and unique (e.g., `AC-001`, `R-CORE-042`).
- Keep one status line directly below each requirement heading: `- **Status:** <Status>` (e.g., `- **Status:** ✅ Verified`).
- Use Given/When/Then format for detailed acceptance criteria — or keep requirements as simple title + status.
- Optional fields:
  - Priority: `- **Priority:** <Level>` (e.g., `🔴 P0 - Critical`, `🟡 P2 - Medium`)
  - Blocked/Deprecated reasons: `**Blocked:** <reason>` or `**Deprecated:** <reason>` on line(s) following status line
  - Flagged state: `- **Flagged:** true|false` — for marking items needing attention without changing status

### Subsection Organization (Optional)

Domain files can use **H2 headers** (`##`) to organize requirements into logical subsections. Subsections:
- Are optional — requirements without a containing H2 have no subsection assignment.
- Help organize large requirement sets (e.g., "Query API", "Mutation API", "Authentication").
- Can have optional body content between the H2 header and the first H3 requirement below it.
- Are discoverable via `--filter-sub-domain <NAME>`, tab completion, and JSON metadata.
- Example structure:
  ```markdown
  ## Query API
  Handles read-only data retrieval and projection.
  
  ### AC-001: Simple query retrieval
  - **Status:** ✅ Verified
  ...
  
  ### AC-002: Complex query filtering
  - **Status:** 💡 Proposed
  ...
  
  ## Mutation API
  Handles write operations and side effects.
  
  ### AC-003: Create operation
  - **Status:** ✅ Verified
  ...
  ```

### File Organization

- Keep this index at {{INDEX_DISPLAY}}.
- Keep domain docs under {{CRITERIA_DIR_DISPLAY}}/.
- Each markdown file represents a domain (e.g., `auth.md`, `payment.md`, `audit.md`).
- Domain ID prefixes are auto-detected from requirement IDs; can override with `--id-prefix`.

### Status Workflow

Canonical status progression:
- `💡 Proposed` → `🔧 Implemented` → `✅ Verified`
- Use `⛔ Blocked` or `🗑️ Deprecated` when needed.

## Domain Documents

### Starter
- [Starter]({{STARTER_DISPLAY}}) - bootstrap requirement for first-run setup
