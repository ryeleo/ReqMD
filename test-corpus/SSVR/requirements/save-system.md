# Save System Acceptance Criteria

Scope: save slot model, auto-save triggers, world-state persistence across sessions, calibration persistence, and save-data schema migration.

<!-- acceptance-status-summary:start -->
Summary: 12💡 0🔧 0💻 0🎮 0✅ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->


## Save Slot Model

### AC-SAVE-SLOT-001: One save slot per game mode
- **Status:** 💡 Proposed
- Given the player plays Practice or Rogue mode
- When save data is written
- Then one save slot exists per game mode (one Practice slot, one Rogue slot)
- And multiple competing save files for the same mode are not supported.

### AC-SAVE-SLOT-002: Save slot is selected automatically by active game mode
- **Status:** 💡 Proposed
- Given the player is in Practice or Rogue context
- When save/load operations occur
- Then the correct mode-specific slot is used automatically
- And the player is never asked to manually pick a slot.

### AC-SAVE-SLOT-003: Save slot displays summary on continue screen
- **Status:** 💡 Proposed
- Given a save slot exists for a mode
- When the player selects `Continue` from the main menu
- Then the existing save is described (for example, last stage, run date) before loading
- And the player is not blindly loaded without context.


## Auto-Save And Triggers

### AC-SAVE-AUTO-001: Auto-save on significant progression
- **Status:** 💡 Proposed
- Given the player makes meaningful progress (stage completion, level unlock, retry)
- When that progression event occurs
- Then game state is saved automatically without requiring player action.

### AC-SAVE-AUTO-002: Auto-save does not interrupt gameplay flow
- **Status:** 💡 Proposed
- Given auto-save is triggered mid-session
- When the save operation runs
- Then gameplay is not paused or interrupted as a result
- And save errors do not halt gameplay (they are logged and skipped).


## World-State Persistence

### AC-SAVE-WORLD-001: Practice world persists across sessions
- **Status:** 💡 Proposed
- Given the player built stages in a Practice world and closed the game
- When they load Practice mode again
- Then all previously built stages and their positions are restored
- And no regeneration occurs for already-built stages.

> **See also:** [AC-MM-PRACTICE-004](main-menu.md#ac-mm-practice-004-continue-loads-existing-practice-world) — Continue loads Practice world.

### AC-SAVE-WORLD-002: Rogue world persists across sessions
- **Status:** 💡 Proposed
- Given the player advanced through Rogue stages and closed the game
- When they load Rogue mode again
- Then progression indices, duel win counts, boss-stage state, and pending offers are restored.

> **See also:** [AC-ROGUE-SAVE-001](rogue.md#ac-rogue-save-001-rogue-slot-persists-progression-indices) — Rogue slot persistence.

### AC-SAVE-WORLD-003: Scorecard history persists across sessions
- **Status:** 💡 Proposed
- Given archived scorecard attempts exist from prior sessions
- When the player loads a mode and revisits a stage
- Then prior scorecard attempts remain available for review
- And no scorecard data is lost on app restart.

> **See also:** [AC-SCORECARD-RETRY-001](scorecards.md#ac-scorecard-retry-001-retry-archives-current-attempt-and-starts-fresh-attempt) — Retry archival contract.

### AC-SAVE-WORLD-004: Firearm calibration persists across sessions
- **Status:** 💡 Proposed
- Given the player adjusted pitch, roll, or offsets in Adjust Aim mode
- When calibration is saved and the game is restarted
- Then calibration values are restored on load
- And the player does not need to recalibrate on every session.

> **See also:** [AC-AIMADJUST-CAL-002](aim-adjust-stage.md#ac-aimadjust-cal-002-calibration-data-preservation) — Calibration data preservation.


## Data Integrity And Migration

### AC-SAVE-INTEGRITY-001: Save data is schema-versioned
- **Status:** 💡 Proposed
- Given save data is written to disk
- When the save file includes version metadata
- Then the version is used during load to detect stale or incompatible schemas
- And old save formats are migrated or flagged rather than silently corrupted.

### AC-SAVE-INTEGRITY-002: Partial write does not corrupt save
- **Status:** 💡 Proposed
- Given the game is force-quit during a save operation
- When the game is next loaded
- Then it detects the incomplete write and recovers to last valid state
- And the player is not presented with a corrupt or unreadable save.

### AC-SAVE-INTEGRITY-003: Save data does not duplicate world geometry on reload
- **Status:** 💡 Proposed
- Given a save file describes an existing set of built stages
- When the world is loaded from that save
- Then no duplicate stage geometry is spawned
- And each stage appears exactly once in the world.
