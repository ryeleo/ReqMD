# Bug Tracking

Scope: first-class bug tracking requirements, templates, and workflow behavior distinct from feature requirements.

Use this file for **meta-requirements about bug tracking itself**.

- Put policy and capability requirements here (metadata fields, workflow rules, templates, filtering behavior).
- Do **not** file day-to-day project defects here.
- File concrete rqmd defects in the [runtime bug backlog](bugs.md).

<!-- acceptance-status-summary:start -->
Summary: 1💡 3🔧 0✅ 0⚠️ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->


### RQMD-BUG-001: Dedicated bug-tracking requirement domain

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** Bug workflow capability is discoverable without scanning unrelated domains.


### RQMD-BUG-002: Runtime bug backlog separated from behavior requirements

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** Filed bug instances have a dedicated place to accumulate without mixing with behavior contracts.

## Boundary Rule

- If the item describes how bug tracking should work in rqmd, it belongs in this file.
- If the item describes an actual defect in rqmd behavior, it belongs in the [runtime bug backlog](bugs.md).

## Related Cross-Domain Requirements

These requirements remain in their original domains but define critical bug-tracking behavior:

- `RQMD-CORE-041` (`core-engine.md`): `type` metadata parser support.
- `RQMD-CORE-042` (`core-engine.md`): `affects` cross-reference metadata.
- `RQMD-CORE-043` (`core-engine.md`): bug-report template.
- `RQMD-AUTOMATION-039` (`automation-api.md`): `--dump-type bug` filter.
- `RQMD-AI-059` (planned, never created): brainstorm/refine bug detection and template routing.
- `RQMD-AI-060` (planned, never created): `/bug` prompt flow for bug filing.
- `RQMD-INTERACTIVE-034` (`interactive-ux.md`): inline `b` key bug filing in interactive mode.

### RQMD-AI-061: CLI bug filing command with VS Code handoff

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** To run `rqmd bug "short title"` and have the CLI generate a bug requirement boilerplate, append it to the appropriate domain file, and open VS Code at that location so that I can file bugs quickly from the command line with minimal friction, then finish filling out the Steps/Expected/Actual fields in my editor.
- Given the user runs `rqmd bug "Widget fails to render after config change"`
- When the CLI processes the command
- Then it discovers the appropriate domain file and next available ID via the same logic as `rqmd --json`
- And it appends a bug requirement skeleton with the supplied title, `Status: 💡 Proposed`, `Type: bug`, and placeholder sections for Steps to Reproduce / Expected / Actual / Root Cause
- And it opens VS Code at the newly created requirement heading line (`code --goto file.md:line`)
- And it prints a brief confirmation with the requirement ID and file path
- And the command keeps CLI interaction short — no interactive prompts, no full editor experience in-terminal.
- Relocated from `ai-cli.md` (AI CLI domain deprecated).


### RQMD-AI-063: Domain-aware `rqmd bug` with positional domain argument and tab completion

- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- **Summary:** To type `rqmd bug <domain> "title"` with a positional domain argument and tab completion so that bugs land in the right domain file immediately without a post-hoc move step.
- Given the user types `rqmd bug interactive "Menu freezes on resize"`
- When the CLI processes the command
- Then it resolves `interactive` to `docs/requirements/interactive-ux.md` (or equivalent), allocates the next ID in that file, appends the bug skeleton, and opens VS Code at the new heading line
- And when the domain argument is ambiguous or matches no file it prints clear options and exits with a non-zero status without writing anything
- And shell completion for `rqmd bug` offers the list of known domain names as the first positional completion candidate.
- Relocated from `ai-cli.md` (AI CLI domain deprecated).