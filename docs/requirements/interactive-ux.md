# Interactive UX Requirement

Scope: interactive menus, keyboard navigation, and in-session requirement status editing.

<!-- acceptance-status-summary:start -->
Summary: 5💡 9🔧 20✅ 0⚠️ 0⛔ 4🗑️
<!-- acceptance-status-summary:end -->

### RQMD-INTERACTIVE-001: Interactive mode default
- **Status:** ✅ Verified
- **Priority:** 🟠 P1 - High
- **Summary:** Check mode to be disabled so that interactive flow opens by default.

### RQMD-INTERACTIVE-002: Single-key menu navigation
- **Status:** ✅ Verified
- **Priority:** 🟠 P1 - High
- **Summary:** To press menu keys so that selections and navigation are handled without pressing Enter.

### RQMD-INTERACTIVE-003: Paging controls
- **Status:** ✅ Verified
- **Priority:** 🟠 P1 - High
- **Summary:** To press next/prev page keys so that menu page changes accordingly.

### RQMD-INTERACTIVE-004: Requirement next/prev shortcuts
- **Status:** ✅ Verified
- **Priority:** 🟠 P1 - High
- **Summary:** To press down arrow (next) or up arrow (prev) so that focus moves across requirements in current ordering.

### RQMD-INTERACTIVE-004A: Next/prev stack semantics
- **Status:** ✅ Verified
- **Priority:** 🟠 P1 - High
- **Summary:** To move forward and backward across requirements so that rqmd preserves a history stack semantics for backtracking.

### RQMD-INTERACTIVE-005: Sort toggles
- **Status:** 🗑️ Deprecated
- **Priority:** 🟢 P3 - Low
- **Deprecated:** Superseded by RQMD-SORTING-007/008/010, which define sort-column cycling, direction toggling, and standardized legend behavior.
- **Summary:** To toggle sort so that ordering switches between default and priority sorting.

### RQMD-INTERACTIVE-006: Status highlight row
- **Status:** ✅ Verified
- **Priority:** 🟠 P1 - High
- **Summary:** The menu to render so that current status row is highlighted.

### RQMD-INTERACTIVE-006A: Color semantics for status families
- **Status:** ✅ Verified
- **Priority:** 🟠 P1 - High
- **Summary:** Status color styles to be applied so that Proposed uses the dedicated proposed color treatment.

### RQMD-INTERACTIVE-006B: Color roll-up and row styling
- **Status:** ✅ Verified
- **Priority:** 🟠 P1 - High
- **Summary:** Roll-up text to render so that blue/proposed, green/completed, normal/in-progress, and dimmed/blocked+deprecated buckets are visually distinct.

### RQMD-INTERACTIVE-007: Keep current requirement visible after update
- **Status:** ✅ Verified
- **Priority:** 🟠 P1 - High
- **Summary:** The update to succeed so that the currently edited requirement remains visible after the change.

### RQMD-INTERACTIVE-008: Optional reason prompts
- **Status:** ✅ Verified
- **Priority:** 🟠 P1 - High
- **Summary:** The update to be confirmed so that tool prompts for optional reason text.

### RQMD-INTERACTIVE-009: Positional requirement lookup mode
- **Status:** ✅ Verified
- **Priority:** 🟠 P1 - High
- **Summary:** The command to execute so that matching requirement panel opens directly.

### RQMD-INTERACTIVE-016: Open specific domain file from CLI entry
- **Status:** ✅ Verified
- **Priority:** 🟠 P1 - High
- **Summary:** The provided path to resolve to a valid markdown domain file containing requirements so that rqmd opens the interactive session with that file selected and the requirement list for that file presented first.
- If both an ID and a filename are provided as positional arguments, the tool should prioritize the ID for lookup and open the file containing that ID if found; if the ID is not found but the file is valid, it should open the specified file and print a warning about the missing ID.

### RQMD-INTERACTIVE-017: Interactive flagged-state toggling
- **Status:** ✅ Verified
- **Priority:** 🟠 P1 - High
- **Summary:** To toggle a requirement's binary flagged state without changing its status so that I can quickly mark or unmark items that need special attention during triage and review.

### RQMD-INTERACTIVE-018: Domain-level notes discoverability in interactive mode
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** Optional domain-level notes/body content to be discoverable in-context (for example in a compact notes pane or explicit notes command) so that implementation guidance and AI-authored domain rationale are available without cluttering individual requirement bodies.

### RQMD-INTERACTIVE-019: Explicit ReqID-list focused interactive walk
- **Status:** ✅ Verified
- **Priority:** 🟠 P1 - High
- **Summary:** To provide an explicit target list at CLI (via positional args or `--targets-file`) and launch a focused interactive walk so that the workflow behaves similarly to `--status` navigation but uses user-provided membership instead of status-based filtering.

### RQMD-INTERACTIVE-020: Case-insensitive tab completion for positional targets
- **Status:** ✅ Verified
- **Priority:** 🟠 P1 - High
- **Summary:** Tab completion for positional target tokens so that typing a prefix such as `rqmd Co<TAB>` suggests matching requirement IDs, domain identifiers, and subsection names that start with that prefix.

### RQMD-INTERACTIVE-021: Subsection navigation and discovery in interactive mode
- **Status:** ✅ Verified
- **Priority:** 🟠 P1 - High
- **Summary:** The menu to expose subsection structure so that subsections are visually grouped and labeled in the requirement list view.

### RQMD-INTERACTIVE-009A: Up key for hierarchical navigation
- **Status:** ✅ Verified
- **Priority:** 🟠 P1 - High
- **Summary:** To press `u` (up) so that rqmd moves up exactly one level in the menu hierarchy.

### RQMD-INTERACTIVE-010: Customizable status catalog and colors
- **Status:** 🗑️ Deprecated
- **Priority:** 🟢 P3 - Low
- **Deprecated:** Superseded by RQMD-PORTABILITY-007/011/012, which own status-catalog schema, configuration loading/precedence, and user/project override behavior.
- **Summary:** The tool exposes status customization settings so that each status can define icon, full_name, and short_code.

### RQMD-INTERACTIVE-011: Preflight write-permission gate before interactive mode
- **Status:** ✅ Verified
- **Priority:** 🟠 P1 - High
- **Summary:** Rqmd to validate write permissions before opening interactive menus so that rqmd validates write permissions for target requirement files up front.

### RQMD-INTERACTIVE-012: Accessibility-safe zebra and color override rendering
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** To configure user or project color overrides so that interactive list zebra striping uses configured accessible foreground/background pairs.

### RQMD-INTERACTIVE-013: Terminal light/dark detection for automatic zebra adjustment
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** Rqmd to start an interactive session so that reqmd attempts to infer a light or dark display context using a best-effort detection strategy (in priority order):.
	- explicit CLI flag `--theme light|dark`
	- project config / user config override
	- macOS system appearance (`defaults read -g AppleInterfaceStyle`) when available
	- common desktop environment settings (e.g., GNOME via `gsettings get org.gnome.desktop.interface color-scheme`) when available
	- environment hints such as `TERM_PROGRAM` or terminal-specific profile hints (best-effort only)
- **Summary:** When detection yields `dark` or `light`, reqmd automatically selects zebra foreground/background pairs and contrast-safe status colors appropriate for the detected mode.

- Implementation notes:
	- Use platform probes cautiously and only as best-effort heuristics; preferred ordered probes: explicit CLI, project/user config, platform API, terminal hints.
	- macOS probe example: `defaults read -g AppleInterfaceStyle` (returns `Dark` when dark mode enabled) — guard with platform checks and timeouts.
	- Linux desktops: try `gsettings` for GNOME when available; otherwise treat as inconclusive.
	- Windows detection requires registry/Win32 API access; implement as an optional probe behind a safe fallback.
	- Always validate chosen colors with a contrast check (WCAG-like thresholds) and auto-adjust zebra pairs if contrast is insufficient.
	- Do not block startup on probes; treat failures as "inconclusive" and continue with fallbacks.
	- Log or surface the detection source (CLI, project, user, system probe, heuristic) in verbose output or UI footer for transparency.
	- Add unit/integration tests that simulate each detection path and verify contrast-based fallbacks and final chosen colors.

### RQMD-INTERACTIVE-014: Standardized footer legend and dynamic sort indicator
- **Status:** 🗑️ Deprecated
- **Priority:** 🟢 P3 - Low
- **Deprecated:** Superseded by RQMD-SORTING-010, which owns the standardized interaction legend and dynamic sort-direction footer behavior.
- **Summary:** To open any interactive menu so that the footer displays a standardized legend in this exact order and compact format:.
- `keys: 1-9 select | n=next | p=prev | u=up | s=sort | d=[asc|dsc] | r=rfrsh | q=quit`
- **Summary:** The `d` token updates in-place to reflect the current sort direction (either `asc` or `dsc`).
	- When the cycle advances past the last sortable column, pressing `s` again returns the view to the default filesystem ordering.

### RQMD-INTERACTIVE-015: Bold active sort column and arrow direction indicator
- **Status:** 🗑️ Deprecated
- **Priority:** 🟢 P3 - Low
- **Deprecated:** Superseded by RQMD-SORTING-011, which owns active sort-column emphasis and direction indicators across interactive views.
- **Summary:** A column to be the active sort key so that the column label is rendered in bold and an ASCII arrow (`↑` or `↓`) is shown adjacent to the label to indicate ascending or descending order.
 

# optional status color overrides (names or hex)
colors:
	proposed: cyan
	in_progress: yellow
	done: green
	blocked: red
	deprecated: grey

### RQMD-INTERACTIVE-022: Interactive link entry with URL-to-hyperlink auto-formatting
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** A link-editing flow accessible from the requirement detail view so that the user can add a new link by entering either a plain URL or a pre-formatted `[label](url)` markdown hyperlink.

### RQMD-INTERACTIVE-023: Vim-style vertical navigation defaults
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** `j` and `k` to be the default down/up navigation keys so that rqmd aligns with Vim vertical motion expectations while keeping arrow-key support intact.

### RQMD-INTERACTIVE-024: Vim-style list motions and paging
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** Rqmd to support common Vim movement primitives beyond one-row navigation so that `gg` jumps to the first item and `G` jumps to the last item in the current list context.

### RQMD-INTERACTIVE-025: Vim-style search and repeat navigation
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** In-session search motions that feel like Vim so that `/` opens forward search and `?` opens reverse search for the current interactive list.

### RQMD-INTERACTIVE-026: Compact footer with full help menu
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** The default interface to stay visually uncluttered while still exposing a complete help menu so that the main footer can emphasize only the highest-frequency keys instead of listing every command at once.

### RQMD-INTERACTIVE-027: Positional status and priority filter walk
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** Rqmd to open the same focused interactive walk that explicit `--status` and `--priority` filters would produce so that commands such as `rqmd P1 Proposed` or `rqmd Prop P1` immediately start a walk over the matching requirements instead of opening the generic file menu.

### RQMD-INTERACTIVE-028: Dedicated interactive rank mode
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- **Summary:** A dedicated `rqmd rank` interactive mode so that rqmd opens directly into a ranking-focused workflow rather than the standard status-editing flow.

### RQMD-INTERACTIVE-029: Rank-editing shortcuts and placement suggestions
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- **Summary:** Rank to be editable with direct keyboard shortcuts plus guided placement suggestions so that I can move the selected requirement to the top, to the bottom, up one slot, down one slot, up one page, or down one page without manually calculating rank values.

### RQMD-INTERACTIVE-030: Open current requirement in VS Code
- **Status:** ✅ Verified
- **Priority:** 🟠 P1 - High
- **Summary:** A direct keyboard action that opens the current requirement in VS Code at its source location so that I can jump from the interactive review flow to the exact markdown block without manually searching for the file and requirement ID.

### RQMD-INTERACTIVE-031: Open linked requirement references from interactive detail view
- **Status:** ✅ Verified
- **Priority:** 🟠 P1 - High
- **Summary:** To click or otherwise activate that referenced requirement link and have rqmd offer to open the referenced requirement immediately so that I can jump quickly to related requirements such as `See also` links, blocking links, or other cross-references without manually searching by ID.

### RQMD-INTERACTIVE-032: Grapheme-safe menu alignment for emoji-rich labels
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- **Summary:** Menu alignment and padding logic to account for terminal grapheme-cluster display width more robustly so that labels do not visually swallow following spaces or collapse adjacent columns in terminals such as VS Code's integrated terminal.

### RQMD-INTERACTIVE-033: Live requirement preview sync with VS Code
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- **Summary:** VS Code to automatically scroll to and highlight the currently focused requirement as I move through the CLI menu so that I can see the full requirement body, related context, and make quick edits in the editor without manually searching for the file and line.
- Given the user has VS Code open in the same workspace where rqmd CLI is running
- When the user navigates to a different requirement in the interactive CLI
- Then VS Code receives a signal (via socket, file watcher, or VS Code extension API) and scrolls to the corresponding requirement heading line
- And the sync is optional and graceful — if VS Code is not open or the extension is not installed, the CLI continues to work normally
- And the implementation may involve a lightweight VS Code extension or the existing `code --goto` invocation in a non-blocking manner.

### RQMD-INTERACTIVE-034: "b" key in interactive mode for inline bug filing
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- **Summary:** To press `b` to file a quick bug without leaving the interactive session so that filing a defect is one keystroke away, with no context switch to a separate terminal command.
- Given the user is in interactive mode browsing `interactive-ux.md`
- When the user presses `b`
- Then the footer clears and shows an inline prompt `Submit bug [interactive]: ` where `interactive` is the current domain
- And the user types a short title and presses Enter
- Then rqmd appends a bug skeleton to the relevant domain file, prints the allocated ID and file path, and opens VS Code at the new line
- And pressing Escape cancels without writing anything and returns to the previous interactive view
- And `b` must not shadow any existing interactive key binding — confirmed free as of this writing.
