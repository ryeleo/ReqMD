# Rogue Acceptance Criteria

Scope: Rogue mode start/load flow, world-state persistence, and baseline duel progression behavior.

<!-- acceptance-status-summary:start -->
Summary: 5💡 7🔧 0💻 0🎮 0✅ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->


## Startup And Loading

### AC-ROGUE-MENU-001: Rogue menu supports Back, Start, and Continue flows as applicable
- **Status:** 💡 Proposed
- Given the player enters the Rogue menu flow
- When menu options are rendered
- Then the Rogue menu supports `Back`, `Start`, and `Continue` actions
- And only actions applicable to the current save-state context are shown.

### AC-ROGUE-MENU-002: Rogue menu only shows applicable continuation actions
- **Status:** 💡 Proposed
- Given the player opens the Rogue menu from the main menu bay
- When the game evaluates whether a continuable Rogue run exists
- Then `Continue` is shown only when there is an existing Rogue run to continue
- And when no Rogue run exists, `Continue` is not shown and `Start` is shown instead.

> **See also:** [Main Menu – AC-MM-PRACTICE-005](main-menu.md#ac-mm-practice-005-practice-menu-only-shows-applicable-continuation-actions) — matching Practice-mode continuation contract.

### AC-ROGUE-START-001: Rogue mode option appears at startup
- **Status:** 🔧 Implemented
- Given the startup menu is visible
- When the player views available modes
- Then `ROGUE` is presented as a selectable mode.

### AC-ROGUE-START-002: Rogue mode uses tap-to-confirm start
- **Status:** 🔧 Implemented
- Given `ROGUE` is visible on startup
- When the player shoots `ROGUE` once
- Then the mode is selected/highlighted
- And when shot a second time, Rogue mode start is confirmed.

### AC-ROGUE-START-003: Rogue start loads prior run when available
- **Status:** 🔧 Implemented
- Given the player confirms Rogue mode start
- When a prior Rogue save slot exists
- Then the run loads from that slot state instead of starting a fresh run.

### AC-ROGUE-START-004: Rogue start initializes fresh run when no save exists
- **Status:** 🔧 Implemented
- Given the player confirms Rogue mode start
- When no prior Rogue save slot exists
- Then a new Rogue run is initialized from baseline starting state.

### AC-ROGUE-CONTINUE-001: Rogue continue restores world-state context
- **Status:** 💡 Proposed
- Given a Rogue save slot exists
- When the player selects `Continue`
- Then the save slot is loaded into Rogue world-state context
- And the player resumes from persisted progression state.

## Rogue World-State Persistence

### AC-ROGUE-SAVE-001: Rogue slot persists progression indices
- **Status:** 🔧 Implemented
- Given Rogue progression advances
- When Rogue slot state is saved
- Then at minimum level index and stage index are persisted for restore.

### AC-ROGUE-SAVE-002: Rogue slot persists duel and encounter state
- **Status:** 🔧 Implemented
- Given a Rogue encounter is in progress
- When Rogue slot state is saved
- Then duel win counts, current encounter stage, boss-stage flag, and pending offers state are persisted for restore.

## Baseline Duel Flow

### AC-ROGUE-DUEL-001: Concurrent player and boss participation
- **Status:** 💡 Proposed
- Given a Rogue duel string starts
- When the player and boss run the stage
- Then both participate in the same encounter window with independent result outcomes.

> **See also:** [Boss AI – AC-BOSS-CONCURRENT-001](boss-ai.md#ac-boss-concurrent-001-player-and-boss-shoot-simultaneously) — concurrent shooting behavior.  
> **See also:** [Boss AI – AC-BOSS-DUEL-002](boss-ai.md#ac-boss-duel-002-match-win-requires-winning-three-of-five-strings) — 3/5 win condition.

### AC-ROGUE-DUEL-002: Stage progression gated by duel result
- **Status:** 💡 Proposed
- Given duel win conditions are evaluated for the encounter
- When the player satisfies progression conditions for that stage
- Then Rogue progression advances to the next offered stage set.

### AC-ROGUE-DUEL-003: Boss-stage flag influences progression branch
- **Status:** 🔧 Implemented
- Given Rogue progression reaches a boss-stage boundary
- When encounter state is evaluated for progression
- Then boss-stage branch state is represented explicitly in persisted and runtime progression logic.
