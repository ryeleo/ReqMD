# Proposed Requirements Analysis — Implementation Candidates

**Analysis Date:** March 27, 2026  
**Current Status:** 132 tests passing, 5✅ completed, 3💡 Proposed items analyzed

## Executive Summary: Top 4 Recommendations

### 🥇 **Tier 1: Quick Wins (Do First — 1-2 days each)**

1. **RQMD-INTERACTIVE-018** — Domain notes discoverability
   - **Why:** Builds directly on existing `scope_and_body_from_file()` (already implemented)
   - **Effort:** Low (menu display only, ~100-150 lines)
   - **Value:** Unblocks domain-level interaction pattern for future features
   
2. **RQMD-INTERACTIVE-022** — Interactive link entry with auto-formatting
   - **Why:** Links are already parsed and stored (RQMD-CORE-021 ✅ Verified); just need UI flow
   - **Effort:** Low-Medium (~150-200 lines for prompt + formatting)
   - **Value:** Self-contained, fully testable, complete link workflow

### 🥈 **Tier 2: Medium Effort (2-3 days each)**

3. **RQMD-PRIORITY-011** — Project-customizable priority catalog
   - **Why:** Pattern already exists for status catalog (RQMD-PORTABILITY-007 model)
   - **Effort:** Medium (~300-400 lines, mirrors status_model.py structure)
   - **Value:** Enables per-project priority terminology, completes priority customization story

4. **RQMD-CORE-024** — Generated top-level README from requirement domains
   - **Why:** Domain parsing exists; template logic is straightforward
   - **Effort:** Medium (~250-350 lines for template + regeneration)
   - **Value:** Enables CI-friendly README sync, "eating your own dogfood"

---

## Detailed Per-Requirement Analysis

### ✅ Already Completed
- **RQMD-CORE-019** (Domain-level body parsing) — ✅ Verified
- **RQMD-CORE-020** (H2 subsection parsing) — ✅ Verified
- **RQMD-CORE-021** (External links field) — ✅ Verified
- **RQMD-PRIORITY-001 through 007** — ✅ Verified (parsing, normalization, UI)

---

## Individual Requirement Assessments

### 1. RQMD-AUTOMATION-019: Unique-Prefix Abbreviations
**Status:** 💡 Proposed  
**Priority:** P2 - Medium  
**Complexity:** Medium-High  

| Aspect | Rating | Notes |
|--------|--------|-------|
| Self-contained? | ❌ No | Depends on stable CLI flag surface |
| Testable? | ✅ Yes | Clear inputs/outputs, deterministic |
| Buildable on existing? | ✅ Yes | Status/priority validation already supports prefix matching |
| Eat own food? | ⚠️ Partial | Tool doesn't use many abbreviations itself |

**Why skip:** User explicitly deferred. Adds complexity during active CLI development.  
**Blocking status:** ⛔ Explicitly deferred per user requirements

---

### 2. RQMD-CORE-022: Enhanced Blocking with Linked Requirements
**Status:** 💡 Proposed  
**Priority:** P2 - Medium  
**Complexity:** Medium  

| Aspect | Rating | Notes |
|--------|--------|-------|
| Self-contained? | ⚠️ Mostly | Requires link parsing (✅ done), linking logic new |
| Testable? | ✅ Yes | Can mock requirement lookup; block reason updates already work |
| Buildable on existing? | ✅ Yes | Uses RQMD-CORE-010 (reason extraction) + RQMD-CORE-021 (links field) |
| Eat own food? | ✅ Yes | Block reasons with IDs are validatable |

**Complexity breakdown:**
- Link/unlink matching: ~80 lines
- Interactive selection/search: ~120 lines  
- Reason line formatting with markdown: ~60 lines
- Tests: ~15-20 test cases

**Why defer:** Requires building interactive requirement-search UI (shares logic with ✅-completed RQMD-INTERACTIVE-019/020 but needs refinement). Not critical for core workflow.

---

### 3. RQMD-CORE-023: Global ID Prefix Renaming Tool  ⚠️
**Status:** 💡 Proposed  
**Priority:** P3 - Low  
**Complexity:** Medium-High  

| Aspect | Rating | Notes |
|--------|--------|-------|
| Self-contained? | ✅ Yes | Pure text replacement + validation |
| Testable? | ✅ Yes | Regex/replacement patterns straightforward |
| Buildable on existing? | ✅ Yes | Uses existing parsing, idempotency patterns |
| Eat own food? | ⚠️ Limited | Rarely needed, one-time operation per project |

**Complexity breakdown:**
- Validation (uniqueness, format checks): ~100 lines
- Bulk replacement across files: ~80 lines
- Summary report generation: ~60 lines
- Tests: ~12-15 cases (edge cases: subsection links, JSON exports, etc.)

**Why medium-low priority:**  
- One-time migration operation, not ongoing workflow
- Not on critical path for core feature parity
- Could be deferred past priority customization

**Can implement if:** Paired with comprehensive test suite covering all cross-file references (headers, links, subsections).

---

### 4. RQMD-CORE-024: Generated Top-Level README from Requirement Domains
**Status:** 💡 Proposed  
**Priority:** P2 - Medium  
**Complexity:** Medium  

| Aspect | Rating | Notes |
|--------|--------|-------|
| Self-contained? | ✅ Yes | Markdown generation + file markers |
| Testable? | ✅ Yes | Templating is deterministic, idempotency testable |
| Buildable on existing? | ✅ Yes | Uses `scope_and_body_from_file()` + summary counts |
| Eat own food? | ✅✅ Yes | Tool can validate its own README sync |

**Complexity breakdown:**
- Template definition + rendering: ~120 lines
- Marker-based insertion/replacement: ~80 lines (mirrors RQMD-CORE-005)
- Idempotency checking: ~60 lines
- CI/on-change hook registration: ~40 lines
- Tests: ~20-25 cases (template vars, idempotency, marker handling)

**Why prioritize:**  
- Directly validates tool's own capability ("eating your own dogfood")
- Supports CI-friendly README maintenance
- Uses existing patterns (summary blocks, marker insertion)
- Clear acceptance criteria (idempotent, no diff on unchanged inputs)

**Blocked on:** None — can implement immediately.

---

### 5. RQMD-INTERACTIVE-018: Domain Notes Discoverability in Interactive Mode
**Status:** 💡 Proposed  
**Priority:** P1 - High  
**Complexity:** Low ✅  

| Aspect | Rating | Notes |
|--------|--------|-------|
| Self-contained? | ✅ Yes | UI-only feature, no mutation |
| Testable? | ✅ Yes | Menu rendering + navigation testable |
| Buildable on existing? | ✅✅ Yes | `scope_and_body_from_file()` already extracts body |
| Eat own food? | ✅ Yes | Navigation behavior testable via interactive walk |

**Implementation sketch:**
```python
# In require-selection menu, show domain body as collapsible note
# Option 1: Inline pane (slow on 80-char terminals)
# Option 2: Press 'd' to "display domain notes" — fullscreen, return with 'q'
# Option 3: Show first 2-3 lines of scope/body in menu title
```

**Complexity breakdown:**
- Note extraction + caching: ~40 lines (already in `scope_and_body_from_file()`)
- Menu display helper: ~60 lines
- Paging/clearing logic: ~40 lines
- Tests: ~8-10 cases

**Why prioritize:**  
- **Highest ROI:** 140 lines, low risk, unblocks pattern for future domain-level features
- Validates domain-body model (RQMD-CORE-019) end-to-end
- Prerequisite for future "domain-level metadata" workflows

**Ready to implement:** ✅ All dependencies exist.

---

### 6. RQMD-INTERACTIVE-012: Accessibility Zebra/Color Overrides
**Status:** 💡 Proposed  
**Priority:** P1 - High  
**Complexity:** Low-Medium  

| Aspect | Rating | Notes |
|--------|--------|-------|
| Self-contained? | ⚠️ Mostly | Config layer exists; color/contrast logic new |
| Testable? | ✅ Yes | Color hex parsing, contrast checks straightforward |
| Buildable on existing? | ✅ Yes | Config loading (RQMD-PORTABILITY-006 ✅ done) |
| Eat own food? | ⚠️ Limited | Requires manual terminal testing |

**Complexity breakdown:**
- Config schema additions (zebra/status colors): ~50 lines
- Color/contrast validation: ~70 lines
- Integration into menu rendering: ~40 lines
- Tests: ~12-15 cases (valid/invalid colors, contrast fallbacks)

**Why defer vs implement:**  
- Requires manual visual validation on real terminals (not ideal for automation)
- Prerequisite to RQMD-INTERACTIVE-013 (platform detection)
- Nice-to-have after tier 1 items

**Recommendation:** Defer until paired with #7 (light/dark detection) for motivation.

---

### 7. RQMD-INTERACTIVE-013: Terminal Light/Dark Detection
**Status:** 💡 Proposed  
**Priority:** P1 - High  
**Complexity:** Medium  

| Aspect | Rating | Notes |
|--------|--------|-------|
| Self-contained? | ✅ Yes | Platform probes + fallback logic isolated |
| Testable? | ✅ Partial | Hard to mock terminals; behavior testable but requires fixtures |
| Buildable on existing? | ✅ Yes | Extends RQMD-INTERACTIVE-012 (color config) |
| Eat own food? | ⚠️ Limited | Requires actual terminal with OS theme set |

**Complexity breakdown:**
- macOS probe: ~30 lines (`defaults read` via subprocess)
- Linux probe: ~50 lines (gsettings + fallbacks)
- Fallback logic + caching: ~40 lines
- Tests: ~15-20 cases (mocked probes, fallback paths, invalid responses)

**Why defer:**  
- Depends on RQMD-INTERACTIVE-012 (color config)
- Platform-specific, requires careful subprocess handling + error isolation
- Test mocking is complex; fixtures span multiple platforms
- Medium priority relative to tier 1 items

**Recommendation:** Implement as part of "accessibility polish" sprint after tier 1 and tier 2.

---

### 8. RQMD-INTERACTIVE-022: Interactive Link Entry with Auto-Formatting
**Status:** 💡 Proposed  
**Priority:** P1 - High  
**Complexity:** Low-Medium ✅  

| Aspect | Rating | Notes |
|--------|--------|-------|
| Self-contained? | ✅ Yes | Pure UI flow, uses existing link storage |
| Testable? | ✅ Yes | Prompt/formatting logic deterministic |
| Buildable on existing? | ✅✅ Yes | Link parsing (RQMD-CORE-021 ✅), reason prompt pattern (RQMD-CORE-010) |
| Eat own food? | ✅ Yes | Can add links to tool's own requirements |

**Implementation sketch:**
```
# When user navigates to requirement detail:
1. Show "Links: <count>" in menu
2. Press 'L' to edit links
3. Menu: "Add / ([1] Item 1) / ([2] Item 2) / ... / Remove / Back"
4. For "Add":
   a. Prompt: "Enter URL or markdown hyperlink: "
   b. If plain URL: Prompt "Add label? (enter to skip): "
   c. If label: Format as [label](url); else keep as plain URL
   d. Insert into **Links:** field or create field
   e. Return to link edit menu
```

**Complexity breakdown:**
- Link display helper: ~50 lines
- Interactive link editor menu: ~80 lines
- Prompt + formatting logic: ~60 lines
- Integration with requirement submission: ~40 lines
- Tests: ~20-25 cases

**Why prioritize:**  
- **Self-contained:** Uses existing links field, no parsing changes
- **Completes feature:** RQMD-CORE-021 ✅ is verified but only via non-interactive batch updates
- **Testable:** Automation-friendly, can validate from CLI
- **High ROI:** ~230 lines, fills workflow gap, no blockers

**Ready to implement:** ✅ All patterns exist (reason prompts, link storage, field update logic).

---

### 9. RQMD-PRIORITY-008: Undo/History Semantics
**Status:** 💡 Proposed  
**Priority:** P1 - High  
**Complexity:** High ❌  

| Aspect | Rating | Notes |
|--------|--------|-------|
| Self-contained? | ❌ No | Requires history system foundation (RQMD-UNDO-001 etc.) |
| Testable? | ✅ Partial | Can test state transitions; integration testing complex |
| Buildable on existing? | ❌ No | Depends on non-existent RQMD-UNDO subsystem |
| Eat own food? | ✅ Yes | Undo can validate itself |

**Complexity breakdown:**
- History model definition: ~150 lines
- State serialization/deserialization: ~120 lines
- Undo/redo stack management: ~100 lines
- Integration into all mutation paths: ~200+ lines
- Tests: ~30+ cases (state machines, edge cases, atomicity)

**Why skip (for now):**  
- **Explicit user guidance:** "complex, likely skip"
- **Blocked on system design:** Requires root RQMD-UNDO-001 architecture decision (time-based, operation-based, checkpoint-based?)
- **High integration burden:** Touches status, priority, link, flag mutations
- **Medium priority:** Users can work around via git history; not critical

**Recommendation:** Defer to dedicated "undo/history sprint" after priority customization and link workflows complete. Plan as 2-3 day effort.

---

### 10. RQMD-PRIORITY-011: Project-Customizable Priority Catalog Schema
**Status:** 💡 Proposed  
**Priority:** P1 - High  
**Complexity:** Medium ✅  

| Aspect | Rating | Notes |
|--------|--------|-------|
| Self-contained? | ✅ Yes | Mirrors status catalog pattern (proven design) |
| Testable? | ✅ Yes | Normalization, lookup, rendering all testable |
| Buildable on existing? | ✅✅ Yes | `status_model.py` provides exact template to follow |
| Eat own food? | ✅ Yes | Tool can define custom priorities; validates itself |

**Complexity breakdown:**
- `priority_catalog.py` module: ~300 lines (mirror of `status_model.py`)
  - Lookup/slug functions: ~80 lines
  - Customization hooks: ~70 lines
  - Styling + rendering: ~80 lines
  - Validation: ~70 lines
- Config integration: ~40 lines (load + validate in `config.py`)
- CLI option wiring: ~30 lines (`--priorities-file` or config merge)
- Tests: ~20-25 cases (parsing, normalization, rendering, edge cases)

**Why prioritize:**  
- **Proven pattern:** Status catalog model already working; replicating is low-risk
- **Completes story:** RQMD-PRIORITY-001 through 007 ✅ done; #011 rounds out customization
- **Enables new workflows:** Teams with custom priority terms (critical, important, tofu, etc.)
- **Self-contained:** No UI changes needed; extends existing priority field

**Dependencies:**  
- ✅ Priority parsing (RQMD-PRIORITY-001)
- ✅ Priority field in UI (RQMD-PRIORITY-003)
- ✅ Config file support (RQMD-PORTABILITY-006)

**Ready to implement:** ✅ All dependencies in place.

---

## Recommendation Matrix

| # | Feature | Priority | Complexity | Est. Effort | Dependencies | Recommendation |
|---|---------|----------|-----------|------------|---|---|
| 1 | RQMD-INTERACTIVE-018 | P1 | Low | 1 day | ✅ All met | **Implement First** |
| 2 | RQMD-INTERACTIVE-022 | P1 | Low-Med | 1.5 days | ✅ All met | **Implement 2nd** |
| 3 | RQMD-PRIORITY-011 | P1 | Med | 2 days | ✅ All met | **Implement 3rd** |
| 4 | RQMD-CORE-024 | P2 | Med | 2 days | ✅ All met | **Implement 4th** |
| 5 | RQMD-INTERACTIVE-012 | P1 | Low-Med | 1.5 days | ⚠️ Pair with #7 | Defer (pair later) |
| 6 | RQMD-INTERACTIVE-013 | P1 | Med | 2 days | ⚠️ Depends on #5 | Defer (polish sprint) |
| 7 | RQMD-CORE-022 | P2 | Med | 2 days | ⚠️ Refine UI | Defer (lower ROI) |
| 8 | RQMD-CORE-023 | P3 | Med-High | 2 days | ✅ All met | Defer (migration only) |
| 9 | RQMD-PRIORITY-008 | P1 | High | 3+ days | ❌ System design | Defer (major sprint) |
| 10 | RQMD-AUTOMATION-019 | P2 | Med-High | 2 days | ⚠️ Explicit skip | **Skip** (user deferred) |

---

## Implementation Plan: 3-4 Items (6-8 Days)

### Phase 1: Domain & Link Workflows (4 days)
**Priority:** Unblock interactive patterns  
**Items:**  
1. **RQMD-INTERACTIVE-018** (1 day)
   - Extract domain body in menu context
   - Display as paged note view (press 'd' to view, 'q' to return)
   - Tests: domain body extraction, menu rendering, navigation

2. **RQMD-INTERACTIVE-022** (1.5 days)
   - Link editor menu (add/remove/view flows)
   - Auto-formatting for plain URLs
   - Label prompt with skip option
   - Tests: prompt behavior, markdown formatting, field updates

3. **RQMD-PRIORITY-011** (2 days)
   - Mirror `status_model.py` as `priority_catalog.py`
   - Config loading + validation
   - Styling + lookup functions
   - Tests: parsing, normalization, color assignment

### Phase 2: README Automation (2 days)
**Priority:** Validate "eating your own dogfood"  
**Items:**  
4. **RQMD-CORE-024** (2 days)
   - Template definition (domain summary generation)
   - Marker insertion/replacement
   - Idempotency validation
   - CLI hook (`--sync-readme` or auto on mutation)
   - Tests: template rendering, idempotency, marker safety

---

## Validation Strategy

### Testing
- **Unit tests:** 60-80 new test cases across 4 features
- **Integration:** Each feature validates via tool's own workflows
- **Smoke tests:** Run tool against self (test-corpus, docs/requirements)

### Self-Validation ("Eating Your Own Dogfood")
- Use tool to update tool's own requirement docs
- Validate RQMD-INTERACTIVE-018: Display domain notes for RQMD-INTERACTIVE-018 requirement itself
- Validate RQMD-INTERACTIVE-022: Add links to requirements
- Validate RQMD-PRIORITY-011: Define custom priority names in tool's config
- Validate RQMD-CORE-024: Auto-sync tool's README against requirement summaries

### Exit Criteria
- ✅ All new tests passing (original 132 + new ~60-80 = ~200)
- ✅ No regressions (all original tests still pass)
- ✅ Tool runs cleanly on self: `rqmd --check --no-interactive` succeeds
- ✅ Interactive workflows functional on real terminal
- ✅ Documentation updated (CHANGELOG.md + requirement status updates)

---

## Risk Assessment

### Low-Risk Items (1-2): RQMD-INTERACTIVE-018, RQMD-INTERACTIVE-022
- **Why:** UI-only, no parsing changes, use existing storage
- **Mitigation:** Unit test every code path, interactive smoke tests

### Medium-Risk Item (3): RQMD-PRIORITY-011
- **Why:** Extends customization surface; must match status catalog patterns exactly
- **Mitigation:** Parallel structure comparison, mirror test approach, config validation

### Medium-Risk Item (4): RQMD-CORE-024
- **Why:** Marker injection (like summary blocks); changes to README structure
- **Mitigation:** Idempotency testing mandatory, backup/dry-run simulation, validation on real repos

---

## Summary

**Top 4 Recommendations (6-8 days):**

1. **RQMD-INTERACTIVE-018** — Domain notes (1 day, P1, Low complexity) ✅
2. **RQMD-INTERACTIVE-022** — Interactive links (1.5 days, P1, Low-Med) ✅
3. **RQMD-PRIORITY-011** — Priority catalog (2 days, P1, Med) ✅
4. **RQMD-CORE-024** — README sync (2 days, P2, Med) ✅

**Why these 4?**
- ✅ All dependencies satisfied (no blockers)
- ✅ Self-contained or low-coupling (50-300 lines each)
- ✅ Testable with clear acceptance criteria
- ✅ Tool can validate itself ("eating your own dogfood")
- ✅ Build on proven patterns (status catalog, summary blocks, config loading)
- ✅ Progressive unblocking (domain workflow → priority customization → README automation)

**Skip:**
- RQMD-AUTOMATION-019: User explicit defer
- RQMD-PRIORITY-008: Requires system design sprint (undo/history foundation)
- RQMD-INTERACTIVE-012/013: Defer as "accessibility polish sprint" (depends on coordination)
- RQMD-CORE-022, 023: Deferred as medium-priority, lower ROI relative to above

---

**Next Steps:**
1. Approve top 4 recommendation
2. Start Phase 1 (RQMD-INTERACTIVE-018 first — 1 day, proven return)
3. Run full test suite after each feature
4. Update CHANGELOG.md + requirement docs on completion
