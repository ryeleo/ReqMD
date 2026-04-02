# Rogue 

Scope: Rogue mode start/load flow, world-state persistence, and baseline duel progression behavior.

<!-- acceptance-status-summary:start -->
Summary: 5💡 8🔧 0💻 0🎮 0✅ 0⚠️ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->





## Startup And Loading

### SSVR-0225: Rogue menu supports Back, Start, and Continue flows as applicable
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given the player enters the Rogue menu flow
- When menu options are rendered
- Then the Rogue menu supports `Back`, `Start`, and `Continue` actions
- And only actions applicable to the current save-state context are shown.

### SSVR-0226: Rogue menu only shows applicable continuation actions
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given the player opens the Rogue menu from the main menu bay
- When the game evaluates whether a continuable Rogue run exists
- Then `Continue` is shown only when there is an existing Rogue run to continue
- And when no Rogue run exists, `Continue` is not shown and `Start` is shown instead.

> **See also:** [Main Menu – SSVR-0158](main-menu.md#ssvr-0158-practice-menu-only-shows-applicable-continuation-actions) — matching Practice-mode continuation contract.

### SSVR-0227: Rogue mode option appears at startup
- **Status:** 🔧 Implemented
- Given the startup menu is visible
- When the player views available modes
- Then `ROGUE` is presented as a selectable mode.

### SSVR-0228: Rogue mode uses tap-to-confirm start
- **Status:** 🔧 Implemented
- Given `ROGUE` is visible on startup
- When the player shoots `ROGUE` once
- Then the mode is selected/highlighted
- And when shot a second time, Rogue mode start is confirmed.

### SSVR-0229: Rogue start loads prior run when available
- **Status:** 🔧 Implemented
- Given the player confirms Rogue mode start
- When a prior Rogue save slot exists
- Then the run loads from that slot state instead of starting a fresh run.

### SSVR-0230: Rogue start initializes fresh run when no save exists
- **Status:** 🔧 Implemented
- Given the player confirms Rogue mode start
- When no prior Rogue save slot exists
- Then a new Rogue run is initialized from baseline starting state.

### SSVR-0231: Rogue continue restores world-state context
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given a Rogue save slot exists
- When the player selects `Continue`
- Then the save slot is loaded into Rogue world-state context
- And the player resumes from persisted progression state.

## Rogue World-State Persistence

### SSVR-0232: Rogue slot persists progression indices
- **Status:** 🔧 Implemented
- Given Rogue progression advances
- When Rogue slot state is saved
- Then at minimum level index and stage index are persisted for restore.

### SSVR-0233: Rogue slot persists duel and encounter state
- **Status:** 🔧 Implemented
- Given a Rogue encounter is in progress
- When Rogue slot state is saved
- Then duel win counts, current encounter stage, boss-stage flag, and pending offers state are persisted for restore.

## Baseline Duel Flow

### SSVR-0234: Rogue review flow does not expose retry
- **Status:** 🔧 Implemented
- Given the player is in Rogue mode and reaches scorecard or encounter review flow
- When review actions are presented
- Then `Retry` is not offered as a stage action
- And the player must continue within the Rogue progression rules rather than restarting the encounter through scorecard retry.

### SSVR-0235: Concurrent player and boss participation
- **Status:** 💡 Proposed
- **Priority:** ☁️ P5 - Dreams
- Given a Rogue duel string starts
- When the player and boss run the stage
- Then both participate in the same encounter window with independent result outcomes.

> **See also:** [Boss AI – SSVR-0042](boss-ai.md#ssvr-0042-player-and-boss-shoot-simultaneously) — concurrent shooting behavior.  
> **See also:** [Boss AI – SSVR-0051](boss-ai.md#ssvr-0051-match-win-requires-winning-three-of-five-strings) — 3/5 win condition.

### SSVR-0236: Stage progression gated by duel result
- **Status:** 💡 Proposed
- **Priority:** ☁️ P5 - Dreams
- Given duel win conditions are evaluated for the encounter
- When the player satisfies progression conditions for that stage
- Then Rogue progression advances to the next offered stage set.

### SSVR-0237: Boss-stage flag influences progression branch
- **Status:** 🔧 Implemented
- Given Rogue progression reaches a boss-stage boundary
- When encounter state is evaluated for progression
- Then boss-stage branch state is represented explicitly in persisted and runtime progression logic.
