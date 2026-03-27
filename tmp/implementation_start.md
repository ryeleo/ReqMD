# Implementation Progress - Phase 1

## Proposal 1: RQMD-INTERACTIVE-022
**Status:** Starting implementation
**Priority:** P1 - High
**Complexity:** Low-Medium
**Est. Time:** 1.5 days

### What it does:
When a user wants to add/manage external links on a requirement interactively:
- Accessible from requirement detail view (new menu option)
- User can enter URL or pre-formatted `[label](url)` markdown
- Plain URL triggers "Add a label? (enter to skip)" prompt
- If label provided: auto-format as `[label](url)`
- If skip: write plain URL
- Can add multiple links in session before returning to requirement view
- Can select existing links to remove or reformat

### Depends on:
- RQMD-CORE-021: Per-requirement external links field (✅ Implemented)

### Implementation plan:
1. Add menu command 'l' for "links" when in requirement view
2. Show current links or "No links yet"
3. Prompt: Edit/add/remove links menu
4. Write updated links back to requirement

### Test strategy:
- Test: Can launch link editing flow from requirement menu
- Test: Plain URL prompts for label
- Test: Label + URL formats correctly
- Test: Multiple links preserved
- Test: Links roundtrip without mangling

### Timeline:
- [ ] Test skeleton writeComplete understanding of requirements
- [ ] Implement link menu UI
- [ ] Implement link add/edit flow  
- [ ] Implement link format validation
- [ ] Run tests
- [ ] Manual validation with rqmd
- [ ] Update docs and CHANGELOGEstimate Progress

---

## Alternative if INTERACTIVE-022 is too complex:
Fall back to implementing **RQMD-CORE-024** (Auto-sync README from domains):
- Read domain files
- Extract status summary from each
- Generate README sections
- Keep between markers
- Idempotent + testable

---

## Token/Time Protection:
- Stop at 2 hours of implementation
- If not complete, pivot to 2-3 smaller features instead
- Document progress clearly
