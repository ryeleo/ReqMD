# RQMD Data Schema & Contract

This document comprehensively specifies the data structures, parsing rules, and metadata contracts used by rqmd.

## Table of Contents
1. [Requirement (Criterion) Object](#requirement-criterion-object)
2. [Subsection (H2) Structure](#subsection-h2-structure)
3. [Markdown Syntax](#markdown-syntax)
4. [Status & Priority Models](#status--priority-models)
5. [JSON Export Contracts](#json-export-contracts)
6. [Parsing Rules](#parsing-rules)

---

## Requirement (Criterion) Object

Each parsed requirement is represented as a dictionary with the following fields:

### Core Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | ✅ Yes | Requirement identifier (e.g., `AC-001`, `R-CORE-042`). Format: `PREFIX-ID` where prefix is configurable. |
| `title` | string | ✅ Yes | Requirement title extracted from H3 header. |
| `header_line` | int | ✅ Yes | Zero-based line number of the H3 requirement header in source file. |
| `status` | string \| null | ⚠️ Conditional | Current status as canonical label (e.g., `✅ Verified`). Must be present for requirement to be indexed. |
| `status_line` | int \| null | ✅ Yes | Zero-based line number of status line (`- **Status:** ...`). Null if no status line found. |

### Optional Metadata Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `priority` | string \| null | `null` | Optional priority level (e.g., `🔴 P0 - Critical`). Parsed from `- **Priority:** ...` |
| `priority_line` | int \| null | `null` | Line number of priority line. |
| `blocked_reason` | string \| null | `null` | Free-text reason if status is Blocked. Parsed from `**Blocked:** <reason>`. |
| `blocked_reason_line` | int \| null | `null` | Line number of blocked reason. |
| `deprecated_reason` | string \| null | `null` | Free-text reason if status is Deprecated. Parsed from `**Deprecated:** <reason>`. |
| `deprecated_reason_line` | int \| null | `null` | Line number of deprecated reason. |
| `flagged` | bool \| null | `null` | Binary marker for triage/attention (true/false). Parsed from `- **Flagged:** true\|false`. |
| `flagged_line` | int \| null | `null` | Line number of flagged line. |

### Subsection Field (Wave 1)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `sub_domain` | string \| null | `null` | Name of containing H2 subsection header (e.g., "Query API"). Null if requirement is not within an H2 section. Subsection names are trimmed whitespace but preserve original casing for display. |

---

## Subsection (H2) Structure

**RQMD-CORE-020** introduces optional H2 headers for organizing requirements within a domain file.

### Syntax

```markdown
## Subsection Name Here

Optional body text describing the subsection scope, design rationale, or implementation notes.

### AC-001: First requirement in subsection
- **Status:** ✅ Verified
...

### AC-002: Second requirement in subsection
- **Status:** 💡 Proposed
...

## Another Subsection

### AC-003: Requirement in different subsection
- **Status:** ✅ Verified
...
```

### Parsing Rules

- H2 header **must** be detected before H3 requirement headers to assign subsection membership.
- Pattern: `^##\s+(?P<section_title>.+?)\s*$` (matches `## Subsection Name`)
- Subsection name is **extracted as verbatim text** (preserve casing, internal whitespace).
- When parsing encounters an H2, it becomes the `current_subsection` for all subsequent H3 requirements until another H2 is found.
- Resetting subsection: parsing next H2 overwrites `current_subsection`; there is **no** explicit "end of subsection" marker.
- Body content between H2 and first H3 is **not currently captured** by core parser (RQMD-CORE-020 for future enhancement).

### Example with Parser State

```
Line 5:  ## Query API                     ← current_subsection = "Query API"
Line 7:  ### AC-001: Get user           ← parsed with sub_domain = "Query API"
Line 12: ### AC-002: Search items       ← parsed with sub_domain = "Query API"
Line 18: ## Mutation API                ← current_subsection = "Mutation API"
Line 20: ### AC-003: Create entity      ← parsed with sub_domain = "Mutation API"
```

---

## Markdown Syntax

### Full Requirement Example (All Optional Fields)

```markdown
## Query API

Details about this subsection go here (optional).

### AC-001: Retrieve user by ID
- **Status:** ✅ Verified
- **Priority:** 🟠 P1 - High
- **Flagged:** false
- Given a valid user ID
- When the API endpoint is called
- Then the user object is returned with all fields
- And response time is < 100ms.

**Blocked:** This is blocked reason text.

## Mutation API

### AC-002: Update user profile
- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- Given a user with edit permissions
- When updating a field
- Then the field is persisted
- And an audit log entry is created.
```

### Parsing Precedence

**Status line search** happens **once per requirement** (uses first match):
```python
if status_match and current and current["status"] is None:
    # Parse and normalize
    current["status"] = coerce_status_label(status_match.group("status"))
    current["status_line"] = index
    continue  # Subsequent matches ignored
```

**Reason lines** can appear on consecutive lines:
```python
blocked_match = BLOCKED_REASON_PATTERN.match(line)
if blocked_match and current and current["status_line"] is not None:
    current["blocked_reason"] = blocked_match.group(1).strip()
    current["blocked_reason_line"] = index
    # Does NOT continue; allows multiple reason lines
```

---

## Status & Priority Models

### Canonical Status Order

| Label | Emoji | Shortcode | Internal | Aliases |
|-------|-------|-----------|----------|---------|
| Proposed | 💡 | P | proposed | proposal, propose |
| Implemented | 🔧 | I | implemented | — |
| Verified | ✅ | V | verified | done |
| Blocked | ⛔ | B | blocked | — |
| Deprecated | 🗑️ | D | deprecated | — |

### Canonical Priority Order

| Label | Emoji | Shortcode | Internal | Aliases |
|-------|-------|-----------|----------|---------|
| P0 - Critical | 🔴 | C | p0 | critical |
| P1 - High | 🟠 | H | p1 | high |
| P2 - Medium | 🟡 | M | p2 | medium |
| P3 - Low | 🟢 | L | p3 | low |

### Coercion Rules

**Status:**
- Input examples: `✅ Verified`, `verified`, `Verified`, `V`, `Done`, `✅ Done`
- Output: Always canonical form with emoji prefix (e.g., `✅ Verified`)
- Unrecognized values raise `ValueError` and are **not** coerced
- Exception: Input `✅ Done` maps to `✅ Verified` (legacy alias)

**Priority:**
- Input examples: `P1 - High`, `p1`, `high`, `🟠 P1 - High`
- Output: Always canonical form with emoji prefix
- Unrecognized values raise `ValueError`

---

## JSON Export Contracts

### Filtered Status Query Response

```json
{
  "filtering": {
    "status": "Verified",
    "criteria_dir": "docs/requirements",
    "criteria_dir_abs": "/absolute/path/docs/requirements",
    "total": 45,
    "match_count": 12
  },
  "files": [
    {
      "path": "core-engine.md",
      "path_display": "core-engine.md",
      "path_abs": "/absolute/path/docs/requirements/core-engine.md",
      "criteria": [
        {
          "id": "RQMD-CORE-001",
          "title": "Domain file discovery",
          "status": "✅ Verified",
          "priority": null,
          "sub_domain": null,
          "flagged": false,
          "blocked_reason": null,
          "deprecated_reason": null
        }
      ]
    }
  ]
}
```

### Key Contract Points

- `path_display` is relative to repo root (human-readable)
- `path_abs` is absolute (machine-safe for cross-machine workflows)
- `criteria_dir_abs` included to allow relative-path reconstruction
- `total` = all requirements in domain directory
- `match_count` = requirements matching filter
- Each criterion includes all metadata fields (null if absent)
- Array order is deterministic (sorted by file, then by header_line within file)
- `sub_domain` field present for all entries (null if requirement has no subsection)

---

## Parsing Rules

### File Discovery

- **Pattern**: `*.md` files in `--requirements-dir` (default: `docs/requirements/`).
- **Order**: Sorted lexicographically by filename.
- **Exclusions**: Files starting with `.`, directories, non-markdown files.

### Requirement Indexing

A requirement is **indexed** (included in result sets) if and only if:
1. **Header matches** `###\s+(?P<id>PREFIX-ID):\s*(?P<title>.+?)` pattern, AND
2. **Status line exists** (`- **Status:** ...`) somewhere in requirement block

If header matches but no status line found, requirement is **not indexed** but does not raise error.

### ID Prefix Detection

rqmd auto-detects valid ID prefixes by:
1. Scanning `docs/requirements/README.md` for requirement headers
2. Following markdown links in the index to discover domain files
3. Collecting all observed ID prefixes (e.g., `AC`, `R`, `RQMD`)
4. Fallback: If no detection possible, use `DEFAULT_ID_PREFIXES = ("AC", "R", "RQMD")`

Override with `--id-prefix AC,R` (comma-separated list).

### Deterministic Ordering

- **Files**: Sorted by filename (ASCII/lexicographic)
- **Requirements within file**: Sorted by `header_line` (appearance order in file)
- **Deterministic tie-breaking**: No ties possible (each requirement has unique line number)

---

## Configuration & Customization

### Project Config Files

rqmd supports optional `.rqmd.yml` or `.rqmd.json` for custom status/priority catalogs:

```yaml
# .rqmd.yml
statuses:
  - name: Proposed
    shortcode: P
    emoji: "💡"
  - name: Implemented
    shortcode: I
    emoji: "🔧"
  - name: Verified
    shortcode: V
    emoji: "✅"
```

Custom statuses **override** canonical order and aliases. Schema must include `name`, `shortcode`, and `emoji` fields.

---

## Future Enhancements

- **RQMD-CORE-020+**: Subsection-level body content capture (narrative + optional metadata per subsection)
- **RQMD-AUTOMATION-032+**: Domain-level body parsing (domain-scope narrative separate from requirements)
- **Schema versioning**: JSON responses will include `schema_version` field when versioning policy is established
