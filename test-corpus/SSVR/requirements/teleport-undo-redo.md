# Teleport Undo/Redo Acceptance Criteria

Scope: player position history tracking, undo/redo navigation in pause menu, teleport stack management.

<!-- acceptance-status-summary:start -->
Summary: 10💡 0🔧 0💻 0🎮 0✅ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->

---

## Undo Last Teleport

### AC-TELEPORT-UNDO-001: Undo last teleport from pause menu
- **Status:** 💡 Proposed
- Given the player has teleported to at least one location in the current world session
- When they open the pause menu and select "Undo Teleport"
- Then the player is transported back to their position before the last teleport
- And the previous position is saved to the redo stack so the user can redo the action.

### AC-TELEPORT-UNDO-002: Undo teleport availability gating
- **Status:** 💡 Proposed
- Given the player attempts to undo a teleport
- When there are no prior teleport positions available (start of session or only 1 position in history)
- Then the "Undo Teleport" option is disabled or grayed out
- And clicking/shooting it produces an audible or visual indication that no undo is available.

---

## Redo Last Teleport

### AC-TELEPORT-REDO-001: Redo last teleport from pause menu
- **Status:** 💡 Proposed
- Given a player has performed an Undo Teleport action
- When they select "Redo Teleport" from the pause menu
- Then the player is transported forward to the location they undid
- And the redo stack is cleared (standard undo/redo semantics).

### AC-TELEPORT-REDO-002: Redo teleport availability gating
- **Status:** 💡 Proposed
- Given the player attempts to redo a teleport
- When no undo has been performed (redo stack is empty)
- Then the "Redo Teleport" option is disabled or grayed out
- And clicking/shooting it produces feedback that redo is not available.

---

## Teleport History Stack

### AC-TELEPORT-HISTORY-001: Teleport position stack contract
- **Status:** 💡 Proposed
- Given the player spawns into a world or enters a bay
- When they teleport to a new location via stage selection, teleporter, or shooter-box interaction
- Then their pre-teleport position is automatically added to an undo stack
- And the position is recorded with bay index, rotation, and eye position for perfect restoration.

> **Constraints:**
> - Stack depth: minimum 16 entries to support ~15 undo steps.
> - Session scope: stack is cleared when the player starts a new world/stage.
> - Teleport types tracked: stage load, shooter-box teleport, bay teleporter, menu selection.
> - Non-teleport position changes (walking, jumping, crouch) do NOT add to stack.

### AC-TELEPORT-HISTORY-002: Redo stack clears on new teleport
- **Status:** 💡 Proposed
- Given a player has undone one or more teleports (redo stack is populated)
- When they perform a new teleport action
- Then the redo stack is cleared (standard undo/redo behavior)
- And the new teleport position is added to the undo stack.

### AC-TELEPORT-HISTORY-003: Teleport position restoration precision
- **Status:** 💡 Proposed
- Given a player undoes or redoes a teleport
- When the position is restored from the stack
- Then the player's position, rotation, and eye height are restored exactly as they were
- And no positional artifacts, interpolation drift, or rotation jitter occur
- And the player's view immediately faces the saved direction without swing-up transitions.

---

## UI & Interaction

### AC-TELEPORT-UNDO-UI-001: Pause menu undo/redo button placement
- **Status:** 💡 Proposed
- Given the pause menu is open with visible gameplay action buttons
- When the menu is rendered
- Then "Undo Teleport" and "Redo Teleport" buttons are prominently visible
- And they follow double-tap confirmation (select then confirm) like other gameplay decisions
- And buttons are disabled/grayed only when their respective stack is empty.

### AC-TELEPORT-UNDO-UI-002: Teleport position indicator (optional)
- **Status:** 💡 Proposed
- Given the pause menu is showing undo/redo options
- When the player views the menu (optional enhancement)
- Then a small subtitle or breadcrumb shows the previous location (e.g., "Undo: Return to Bay 3")
- And a similar indicator shows the next location if redo is available.

---

## Session and Save Behavior

### AC-TELEPORT-UNDO-SAVE-001: Teleport history not persisted across save/load
- **Status:** 💡 Proposed
- Given a player saves their progress and later loads it
- When the save is restored
- Then the teleport undo/redo stack is cleared
- And the player can only undo/redo teleports that occurred in the current play session (not prior sessions).

---

## Related Features

- [AC-PAUSE-MENU-001+](pause-menu.md) — Pause menu structure and action options.
- [AC-MM-INTERACT-002](main-menu.md#ac-mm-interact-002-stage-selection-tap-sequence) — Stage selection double-tap behavior (now simplified to immediate teleport).
