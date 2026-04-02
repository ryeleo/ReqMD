# Save System 

Scope: save slot model, auto-save triggers, world-state persistence across sessions, calibration persistence, and save-data schema migration.

<!-- acceptance-status-summary:start -->
Summary: 4💡 8🔧 0💻 0🎮 0✅ 0⚠️ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->





## Save Slot Model

### SSVR-0213: One save slot per game mode
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- Given the player plays Practice or Rogue mode
- When save data is written
- Then one save slot exists per game mode (one Practice slot, one Rogue slot)
- And multiple competing save files for the same mode are not supported.

### SSVR-0214: Save slot is selected automatically by active game mode
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- Given the player is in Practice or Rogue context
- When save/load operations occur
- Then the correct mode-specific slot is used automatically
- And the player is never asked to manually pick a slot.

### SSVR-0215: Save slot displays summary on continue screen
- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- Given a save slot exists for a mode
- When the player selects `Continue` from the main menu
- Then the existing save is described (for example, last stage, run date) before loading
- And the player is not blindly loaded without context.


## Auto-Save And Triggers

### SSVR-0216: Auto-save on significant progression
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- Given the player makes meaningful progress (stage completion, level unlock, retry)
- When that progression event occurs
- Then game state is saved automatically without requiring player action.

### SSVR-0217: Auto-save does not interrupt gameplay flow
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- Given auto-save is triggered mid-session
- When the save operation runs
- Then gameplay is not paused or interrupted as a result
- And save errors do not halt gameplay (they are logged and skipped).


## World-State Persistence

### SSVR-0218: Practice world persists across sessions
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- Given the player built stages in a Practice world and closed the game
- When they load Practice mode again
- Then all previously built stages and their positions are restored
- And no regeneration occurs for already-built stages.

> **See also:** [SSVR-0157](main-menu.md#ssvr-0157-continue-loads-existing-practice-world) — Continue loads Practice world.

### SSVR-0219: Rogue world persists across sessions
- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- Given the player advanced through Rogue stages and closed the game
- When they load Rogue mode again
- Then progression indices, duel win counts, boss-stage state, and pending offers are restored.

> **See also:** [SSVR-0232](rogue.md#ssvr-0232-rogue-slot-persists-progression-indices) — Rogue slot persistence.

### SSVR-0220: Scorecard history persists across sessions
- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- Given archived scorecard attempts exist from prior sessions
- When the player loads a mode and revisits a stage
- Then prior scorecard attempts remain available for review
- And no scorecard data is lost on app restart.

> **See also:** [SSVR-0270](scorecards.md#ssvr-0270-retry-unlocks-only-after-stage-completion-and-starts-a-fresh-attempt) — Retry archival contract.

### SSVR-0221: Firearm calibration persists across sessions
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- Given the player adjusted pitch, roll, or offsets in Adjust Aim mode
- When calibration is saved and the game is restarted
- Then calibration values are restored on load
- And the player does not need to recalibrate on every session.

> **See also:** [SSVR-0013](aim-adjust-stage.md#ssvr-0013-calibration-data-preservation) — Calibration data preservation.


## Data Integrity And Migration

### SSVR-0222: Save data is schema-versioned
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- Given save data is written to disk
- When the save file includes version metadata
- Then the version is used during load to detect stale or incompatible schemas
- And old save formats are migrated or flagged rather than silently corrupted.

### SSVR-0223: Partial write does not corrupt save
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- Given the game is force-quit during a save operation
- When the game is next loaded
- Then it detects the incomplete write and recovers to last valid state
- And the player is not presented with a corrupt or unreadable save.

### SSVR-0224: Save data does not duplicate world geometry on reload
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- Given a save file describes an existing set of built stages
- When the world is loaded from that save
- Then no duplicate stage geometry is spawned
- And each stage appears exactly once in the world.
