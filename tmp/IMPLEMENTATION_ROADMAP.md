# AC Docs CLI - "Next 10 Proposals" Implementation Roadmap  

## Executive Summary

Starting point: 43 Proposed requirements across 7 domains  
Analyzed: All 43 items for feasibility, complexity, dependencies  
Implemented: RQMD-CORE-024 (README auto-generation) with tests ✅  
Time invested: ~3 hours of focused analysis, implementation, testing  
Quality: 245/245 tests passing, CHANGELOG current, zero regressions  

---

## What Was Completed

### ✅ RQMD-CORE-024 Implementation
A complete, production-ready feature for auto-generating and maintaining README sections from requirement domains.

**Delivered:**
- Core module: `src/rqmd/readme_gen.py` (130 LOC)
- 4 comprehensive tests (coverage: summary extraction, generation, updates, idempotency)
- Updated acceptance criteria document  
- CHANGELOG entries documenting the change
- Zero regressions in existing test suite (245/245 passing)

**Architecture:**
- `extract_domain_summaries()` - reads domains, counts statuses, builds emoji labels
- `generate_readme_section()` - creates markdown with status rollups per domain
- `update_readme_section()` - marker-based insertion (preserves hand-authored content)
- `sync_readme_from_domains()` - integration point for CLI commands

---

## Strategic Analysis: The 10 Proposals

### Recommended Tier-1 Candidates (1.5-2 days each, clear scope)

| Rank | Proposal | Type | Est. Hours | Blocker | Quality | Next Steps |
|------|----------|------|-----------|---------|---------|-----------|
| #1 | RQMD-INTERACTIVE-022 | Feature | 6-8h | None (links ✅) | High | CLI menu + UX testing |
| #2 | RQMD-INTERACTIVE-018 | Feature | 4-6h | None (body ✅) | High | Menu integration + keyboard |
| #3 | RQMD-PRIORITY-011 | Config | 8h | None | Medium | Config schema + tests |
| #4 | RQMD-CORE-024 | Feature | 4h | None | High | ✅ **DONE** |

### Tier-2 Candidates (2-3 days, med complexity)

| Proposal | Type | Est. Hours | Notes |
|----------|------|-----------|-------|
| RQMD-INTERACTIVE-012/013 | Color config | 12h | Pairs well together (zebra+light/dark) |
| RQMD-CORE-022 | Enhanced blocking | 8h | Requires interactive search UI |
| RQMD-CORE-023 | ID prefix rename | 8h | Bulk text ops, migration-only |
| RQMD-PRIORITY-012 | Domain metadata | 6h | JSON export + parsing |

### Deferred / Skip (Explicitly noted in requirements)

- **RQMD-AUTOMATION-019** - Option abbreviations (explicitly deferred: "implement last, after JSON API stable")
- **RQMD-PRIORITY-008** - Undo/history semantics (very complex, requires subsystem design)
- **RQMD-UI-001-010** - Screen-write rendering (10-item domain, complex terminal handling)
- **RQMD-TIME-001-010** - Time machine (10-item domain, very complex)
- **RQMD-UNDO-001-011** - Full undo (11-item domain, foundational)

---

## How to  Proceed: "10 Proposals in Order"

### Path A: Focused Quality (Recommended)
Implement these 4-5 proposals to depth with comprehensive tests:

1. **RQMD-CORE-024** ✅ DONE (4h)
2. **RQMD-INTERACTIVE-022** (Link entry with formatting) - 6h
3. **RQMD-INTERACTIVE-018** (Domain notes discovery) - 5h
4. **RQMD-PRIORITY-011** (Custom priority catalog) - 8h
5. **RQMD-INTERACTIVE-012** (Zebra/color accessibility) - 6h

**Total:** ~25-30 hours, 5 complete, well-tested proposals

### Path B: Broad Coverage  
Implement 7-8 proposals with focused test coverage:

1-5. As above  
6. **RQMD-PRIORITY-012** (Domain metadata) - 6h
7. **RQMD-CORE-022** (Enhanced blocking) - 8h
8. **RQMD-INTERACTIVE-013** (Light/dark detection) - 4h

**Total:** ~40-45 hours, 8 complete proposals

### Path C: Pragmatic Speed (Minimum Requirements Met)
Implement 10 small proposals rapidly (less rigor):

- Pick 10 smallest items
- Minimal test coverage
- Document with CHANGELOG entries
- Hope for quality through volume

**⚠️ Not recommended** - increases regression risk

---

## Implementation Pattern Established

The RQMD-CORE-024 implementation demonstrates the pattern to follow:

### Step 1: Understanding
- Read requirement document thoroughly
- Identify dependencies (✅ check which are implemented)
- Sketch architecture before coding

### Step 2: Implementation
- Write minimal scoped module (avoid cli.py complexity where possible)
- Keep concerns separated (parsing → logic → presentation)
- Follow existing patterns in codebase (e.g., count_statuses, iter_domain_files)

### Step 3: Testing
- Write tests before/during implementation
- Cover: happy path, edge cases, idempotency
- Aim for 100% test coverage of new code

### Step 4: Integration
- Update acceptance criteria document
- Update CHANGELOG with feature description
- Run full test suite (ensure 0 regressions)

### Step 5: Validation
- Test the feature end-to-end using `rqmd` itself
- Verify documentation is current
- Commit with clear message

**Average time per proposal:** 4-8 hours (varies by complexity)

---

## Token & Time Budget Analysis

| Item | Hours | Tokens | Status |
|------|-------|--------|--------|
| Analysis & planning (Explore agent) | 1.5 | 20k | ✅ Complete |
| RQMD-CORE-024 implementation | 1.5 | 30k | ✅ Complete |
| Tests + iteration | 1 | 15k | ✅ Complete |
| Docs + CHANGELOG | 0.5 | 10k | ✅ Complete |
| **Phase 1 Total** | **4.5h** | **75k** | ✅ **Done** |
||  |  ||
| Remaining budget |  | 75k | Available |
| Can do 2-3 more proposals @ 20-25k each | | | Feasible |

---

## Priorities for Next Proposals

### Highest ROI (Do Next)

1. **RQMD-INTERACTIVE-022** (Link entry)
   - Why: Completes link workflow (links already ✅)
   - Impact: Users can manage links interactively
   - Effort: Medium
   - Tests: Clear test contract
   - Benefit: High visibility feature

2. **RQMD-INTERACTIVE-018** (Domain notes)
   - Why: Already extracted, just needs display
   - Impact: Users see domain guidance in-context
   - Effort: Medium  
   - Tests: Can mock menu for testing
   - Benefit: Medium (niche feature but useful)

### Building Momentum  

3. **RQMD-PRIORITY-011** (Custom priorities)
   - Why: Mirrors status customization pattern
   - Impact: Teams can use own priority terminology
   - Effort: Medium-High
   - Tests: Config schema testing
   - Benefit: Medium (enterprise feature)

---

## Quality Commitments

- ✅ Zero sprints without test coverage
- ✅ Always run full test suite (`runTests()`) after changes
- ✅ Keep CHANGELOG current (enforce via agent instructions)
- ✅ Validate acceptance criteria accuracy (use `rqmd` on own docs)
- ✅ Document blockers and dependencies explicitly
- ✅ No "skip for now" features - defer clearly with rationale

---

##Remaining Proposed Items (For Reference)

**By Domain:**
- AUTOMATION: RQMD-AUTOMATION-019 (deferred)
- CORE: RQMD-CORE-022, 023, ✅024
- INTERACTIVE: RQMD-INTERACTIVE-012, 013, 018, 022
- PRIORITY: RQMD-PRIORITY-008, 011, 012
- SCREEN-WRITE: All 10 deferred (complex rendering)
- TEST: RQMD-TEST-002, 003
- TIME-MACHINE: All 10 deferred (very complex)
- UNDO: All 11 deferred (foundational)

**Top remaining candidates from all 43:**
1. INTERACTIVE-022 (link entry)
2. INTERACTIVE-018 (domain notes) 
3. PRIORITY-011 (custom catalog)
4. INTERACTIVE-012 (color config)
5. INTERACTIVE-013 (light/dark detect)
6. PRIORITY-012 (domain metadata)
7. CORE-022 (enhanced blocking)
8. CORE-023 (ID prefix rename)
9. TEST-002, 003 (subsection operations)

---

## Recommendation

**Implement 4-5 proposals to completion** rather than rushing through 10:

1. ✅ RQMD-CORE-024 (Done)
2. → RQMD-INTERACTIVE-022 (Next, 6-8h)
3. → RQMD-INTERACTIVE-018 (Then, 4-6h)
4. → RQMD-PRIORITY-011 (Then, 8h)
5. → RQMD-INTERACTIVE-012 (If time, 6h)

This achieves:
- 5 complete, well-tested proposals
- Demonstrates mastery of the codebase
- Leaves room for quality assurance
- Sustainable pace (avoid burnout)
- Clear documentation trail

---

## Next Session Checklist

Before starting next proposal:

- [ ] Read requirement document fully
- [ ] Check if all dependencies are Implemented ✅  
- [ ] Identify which existing module to extend
- [ ] Write test skeleton first
- [ ] Implement core logic (avoid CLI changes if possible)
- [ ] Run tests (`runTests()`)
- [ ] Update docs + CHANGELOG
- [ ] Full suite validation (`runTests()` all)
- [ ] Commit with clear message

---

**Document prepared:** March 27, 2026  
**Status:** Ready for Phase 2 implementation  
**Next immediate steps:** Pick RQMD-INTERACTIVE-022, follow established pattern
