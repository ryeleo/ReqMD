# Scorecards Acceptance Criteria

Scope: scorecard presentation and review flow derived from string replay data, archived attempts, and leaderboard/scorecard interactions.

<!-- acceptance-status-summary:start -->
Summary: 9💡 11🔧 1💻 0🎮 3✅ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->


## Data Derivation And Relationship

### AC-SCORECARD-DATA-001: Scorecards are child data of string replays
- **Status:** 💡 Proposed
- Given a stage result produces one or more string replays
- When scorecard data is stored or reconstructed
- Then scorecard rows are treated as child/projection data of replay records
- And scorecards are not treated as an independent parent data model.

> **See also:** [String Replays – AC-REPLAY-SCORECARD-001](string-replays.md#ac-replay-scorecard-001-replay-record-is-the-parent-record-for-scorecard-data) — replay as parent record contract.

### AC-SCORECARD-DATA-002: Scorecard storage carries replay linkage and core score fields
- **Status:** 💡 Proposed
- Given scorecard data is indexed for query or UI use
- When persistence completes
- Then stored scorecard rows include parent replay linkage plus stage name, player name, total time, misses, make-up shots, and per-string breakdown.

### AC-SCORECARD-DATA-003: Runtime keeps target-coded split detail from replay-compatible data
- **Status:** ✅ Done
- Given shots are recorded during strings
- When runtime split data is retained
- Then per-shot target-coded splits such as `T1` through `T4`, `S`, and `MISS` remain available for drilldown UI use.

### AC-SCORECARD-DATA-004: Leaderboard rows remain replay-traceable
- **Status:** 💡 Proposed
- Given leaderboard-oriented score rows are persisted separately for scalability
- When leaderboard entries are queried
- Then each entry remains traceable to a parent replay identity
- And replay lineage can be used for audit, drilldown, or re-scoring.

### AC-SCORECARD-DATA-005: Scorecard views can be rebuilt from replay data
- **Status:** 💡 Proposed
- Given replay payloads and scoring rules are available
- When scorecard state is rebuilt for migration or recovery
- Then scorecard views can be regenerated without requiring a separate authoritative scorecard source.

### AC-SCORECARD-DATA-006: Scorecard rows track shots fired and compact hit order
- **Status:** 💡 Proposed
- Given scorecard data is produced from replay/scoring events
- When a row is written for UI or persistence
- Then `targetsHit` is replaced by `shotsFired` to reflect all fired rounds
- And hit result detail remains visible in that row so target-hit context is easy to inspect
- And a compact `hitOrder` comma-separated string is stored to show scored-hit sequence (for example `T1,T2,T4,T3,Stop`).

## Scorecard Presentation

### AC-SCORECARD-VIEW-001: Scorecard panel shows up to five strings
- **Status:** ✅ Done
- Given the scorecard panel is rendered for a stage
- When string results are displayed
- Then the panel shows up to five strings with stop, penalty, and total columns plus placeholder rows.

### AC-SCORECARD-VIEW-002: Scorecard is built into the timed bay
- **Status:** 💻 Desktop-Verified
- Given a timed stage bay is generated
- When scene construction completes
- Then a static scorecard display exists in the bay positioned to the shooter's **LEFT**.

### AC-SCORECARD-VIEW-003: Scorecard and next-stage menu are separate systems
- **Status:** ✅ Done
- Given stage review is active
- When the player interacts with post-stage UI
- Then the scorecard display and next-stage selection menu remain separate systems
- And the next-stage selection is managed by its own gong array.

### AC-SCORECARD-VIEW-004: LED displays always fit their authored text
- **Status:** 💡 Proposed
- Given any LED-backed gameplay display is rendering runtime text
- When the display text length changes (including long stage descriptions)
- Then the display width/scale/wrapping behavior ensures text remains fully readable without clipping or overflow.
- Test: stage description overflows presently, and pause menu.

### AC-SCORECARD-VIEW-005: Stage description is visible on scorecard arrival
- **Status:** 💡 Proposed
- Given the shooter arrives at a newly loaded stage
- When the scorecard display initializes for that stage
- Then the stage description text is shown on the scorecard display without requiring extra player interaction.

### AC-SCORECARD-VIEW-006: Scorecard appears after each completed string
- **Status:** 💡 Proposed
- Given the shooter completes a string
- When the string result is finalized
- Then the scorecard display is presented or refreshed to show the latest string result.

## Review And Acceptance Flow

### AC-SCORECARD-REVIEW-001: Readiness is gated after five strings
- **Status:** 🔧 Implemented
- Given five strings have been completed for the current stage
- When the player attempts to begin another string immediately
- Then readiness remains gated until the player reviews or accepts the scorecard flow.

### AC-SCORECARD-REVIEW-002: Review scorecard waits for explicit stage-accept flow
- **Status:** 🔧 Implemented
- Given stage review begins after the fifth string
- When the review state is shown
- Then the scorecard remains in review flow until the player explicitly confirms the next action.

### AC-SCORECARD-REVIEW-003: Accepting next stage advances to the bay on the right
- **Status:** 🔧 Implemented
- Given the player accepts the next stage from review flow
- When stage advancement occurs
- Then the selected stage is built in the bay to the right rather than replacing the current bay.

### AC-SCORECARD-REVIEW-004: Completed bays remain in place as history
- **Status:** 🔧 Implemented
- Given the player advances to another stage
- When the next bay is built
- Then previously completed bays remain in place instead of being destroyed.

### AC-SCORECARD-REVIEW-005: Review scorecard is archived as visual history
- **Status:** 🔧 Implemented
- Given the player advances after review
- When archival occurs
- Then the current review panel is frozen in place as non-interactive visual history.

## Retry And Attempt History

### AC-SCORECARD-RETRY-001: Retry archives current attempt and starts fresh attempt
- **Status:** 🔧 Implemented
- Given the player activates `Retry` for a stage
- When retry begins
- Then the current attempt is archived
- And a fresh attempt on the same stage starts.

### AC-SCORECARD-RETRY-002: Incomplete archived attempts are padded to full rows
- **Status:** 🔧 Implemented
- Given an unfinished attempt is archived through retry flow
- When the archived scorecard is normalized
- Then missing rows are padded as `30.000s` rows.

### AC-SCORECARD-RETRY-003: Previous and Next cycle archived and live attempts
- **Status:** 🔧 Implemented
- Given multiple archived attempts and a current live attempt exist for a stage
- When the player uses `Previous` or `Next`
- Then scorecard navigation cycles archived attempts and the current live attempt for that stage.

### AC-SCORECARD-RETRY-004: Scorecard history navigation only shows applicable buttons
- **Status:** 💡 Proposed
- Given the player is viewing scorecard history controls for a stage
- When the game evaluates whether previous or next attempt history exists
- Then only navigation buttons applicable to the available history are shown
- And `Previous` and `Next` do not appear on fresh stage entry before retry/history state exists.

> **See also:** [Main Menu – AC-MM-PRACTICE-005](main-menu.md#ac-mm-practice-005-practice-menu-only-shows-applicable-continuation-actions) — same context-sensitive button-visibility contract.  
> **See also:** [Rogue – AC-ROGUE-MENU-002](rogue.md#ac-rogue-menu-002-rogue-menu-only-shows-applicable-continuation-actions) — matching Rogue continuation contract.

## Leaderboard And Detailed Scorecard Interaction

### AC-SCORECARD-LEADERBOARD-001: Pause menu leaderboard is stage-scoped
- **Status:** 🔧 Implemented
- Given the player is in a shooter box and opens the pause menu
- When leaderboard content is available
- Then the leaderboard panel is scoped to the current stage.

> **See also:** [Leaderboards – AC-LEADERBOARD-PANEL-001](leaderboards.md#ac-leaderboard-panel-001-leaderboard-appears-as-pause-menu-panel) — leaderboard panel behavior.

### AC-SCORECARD-LEADERBOARD-002: Leaderboard row selection is shot-driven
- **Status:** 🔧 Implemented
- Given the leaderboard panel is visible
- When the player shoots a record row once
- Then that row is selected
- And when the player shoots the same row a second time, a detailed scorecard panel opens.

### AC-SCORECARD-LEADERBOARD-003: Detailed scorecard close uses two-shot close flow
- **Status:** 🔧 Implemented
- Given a detailed scorecard panel is open
- When the player shoots the panel once
- Then close is armed
- And when they shoot again, the panel closes.
