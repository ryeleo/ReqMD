# Scorecards 

Scope: scorecard presentation and review flow derived from string replay data, archived attempts, and leaderboard/scorecard interactions.

<!-- acceptance-status-summary:start -->
Summary: 10💡 12🔧 1💻 0🎮 3✅ 0⚠️ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->





## Data Derivation And Relationship

### SSVR-0252: Scorecards are child data of string replays
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- Given a stage result produces one or more string replays
- When scorecard data is stored or reconstructed
- Then scorecard rows are treated as child/projection data of replay records
- And scorecards are not treated as an independent parent data model.

> **See also:** [String Replays – SSVR-0296](string-replays.md#ssvr-0296-replay-record-is-the-parent-record-for-scorecard-data) — replay as parent record contract.

### SSVR-0253: Scorecard storage carries replay linkage and core score fields
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- Given scorecard data is indexed for query or UI use
- When persistence completes
- Then stored scorecard rows include parent replay linkage plus stage name, player name, total time, misses, make-up shots, and per-string breakdown.

### SSVR-0254: Runtime keeps target-coded split detail from replay-compatible data
- **Status:** ✅ Done
- Given shots are recorded during strings
- When runtime split data is retained
- Then per-shot target-coded splits such as `T1` through `T4`, `S`, and `MISS` remain available for drilldown UI use.

### SSVR-0255: Leaderboard rows remain replay-traceable
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given leaderboard-oriented score rows are persisted separately for scalability
- When leaderboard entries are queried
- Then each entry remains traceable to a parent replay identity
- And replay lineage can be used for audit, drilldown, or re-scoring.

### SSVR-0256: Scorecard views can be rebuilt from replay data
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- Given replay payloads and scoring rules are available
- When scorecard state is rebuilt for migration or recovery
- Then scorecard views can be regenerated without requiring a separate authoritative scorecard source.

### SSVR-0257: Scorecard rows track shots fired and compact hit order
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given scorecard data is produced from replay/scoring events
- When a row is written for UI or persistence
- Then `targetsHit` is replaced by `shotsFired` to reflect all fired rounds
- And hit result detail remains visible in that row so target-hit context is easy to inspect
- And a compact `hitOrder` comma-separated string is stored to show scored-hit sequence (for example `T1,T2,T4,T3,Stop`).

## Scorecard Presentation

### SSVR-0258: Scorecard panel shows up to five strings
- **Status:** ✅ Done
- Given the scorecard panel is rendered for a stage
- When string results are displayed
- Then the panel shows up to five strings with stop, penalty, and total columns plus placeholder rows.

### SSVR-0259: Scorecard is built into the timed bay
- **Status:** 💻 Desktop-Verified
- Given a timed stage bay is generated
- When scene construction completes
- Then a static scorecard display exists in the bay positioned to the shooter's **LEFT**.

### SSVR-0260: Scorecard and next-stage menu are separate systems
- **Status:** ✅ Done
- Given stage review is active
- When the player interacts with post-stage UI
- Then the scorecard display and next-stage selection menu remain separate systems
- And the next-stage selection is managed by its own gong array.

### SSVR-0261: LED displays always fit their authored text
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- Given any LED-backed gameplay display is rendering runtime text
- When the display text length changes (including long stage descriptions)
- Then the display width/scale/wrapping behavior ensures text remains fully readable without clipping or overflow.
- Test: stage description overflows presently, and pause menu.

### SSVR-0262: Stage description is visible on scorecard arrival
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given the shooter arrives at a newly loaded stage
- When the scorecard display initializes for that stage
- Then the stage description text is shown on the scorecard display without requiring extra player interaction.

### SSVR-0263: Scorecard appears after each completed string
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given the shooter completes a string
- When the string result is finalized
- Then the scorecard display is presented or refreshed to show the latest string result.

### SSVR-0264: Interactive scorecard actions are array-managed
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given scorecard review exposes interactive gong-button actions such as next stage, retry, previous, or next attempt
- When those controls are presented near the scorecard flow
- Then those controls are grouped into one or more gong arrays with their own placement slots
- And the scorecard panel remains responsible for information display rather than manually placing individual action gongs.

## Review And Acceptance Flow

### SSVR-0265: Readiness is gated after five strings
- **Status:** 🔧 Implemented
- Given five strings have been completed for the current stage
- When the player attempts to begin another string immediately
- Then readiness remains gated until the player reviews or accepts the scorecard flow.

### SSVR-0266: Review scorecard waits for explicit stage-accept flow
- **Status:** 🔧 Implemented
- Given stage review begins after the fifth string
- When the review state is shown
- Then the scorecard remains in review flow until the player explicitly confirms the next action.

### SSVR-0267: Accepting next stage advances to the bay on the right
- **Status:** 🔧 Implemented
- Given the player accepts the next stage from review flow
- When stage advancement occurs
- Then the selected stage is built in the bay to the right rather than replacing the current bay.

### SSVR-0268: Completed bays remain in place as history
- **Status:** 🔧 Implemented
- Given the player advances to another stage
- When the next bay is built
- Then previously completed bays remain in place instead of being destroyed.

### SSVR-0269: Review scorecard is archived as visual history
- **Status:** 🔧 Implemented
- Given the player advances after review
- When archival occurs
- Then the current review panel is frozen in place as non-interactive visual history.

## Retry And Attempt History

### SSVR-0270: Retry unlocks only after stage completion and starts a fresh attempt
- **Status:** 🔧 Implemented
- Given the player is in a retry-eligible non-Rogue stage review state after completing the stage
- When they activate `Retry`
- Then the current attempt is archived
- And a fresh attempt on the same stage starts
- And `Retry` is not shown during the active in-progress strings before the stage is completed.

### SSVR-0271: Incomplete archived attempts are padded to full rows
- **Status:** 🔧 Implemented
- Given an unfinished attempt is archived through retry flow
- When the archived scorecard is normalized
- Then missing rows are padded as `30.000s` rows.

### SSVR-0272: Previous and Next cycle archived and live attempts
- **Status:** 🔧 Implemented
- Given multiple archived attempts and a current live attempt exist for a stage
- When the player uses `Previous` or `Next`
- Then scorecard navigation cycles archived attempts and the current live attempt for that stage.

### SSVR-0273: Scorecard history navigation only shows applicable buttons
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given the player is viewing scorecard history controls for a stage
- When the game evaluates whether previous or next attempt history exists
- Then only navigation buttons applicable to the available history are shown
- And `Previous` and `Next` do not appear on fresh stage entry before retry/history state exists.

> **See also:** [Main Menu – SSVR-0158](main-menu.md#ssvr-0158-practice-menu-only-shows-applicable-continuation-actions) — same context-sensitive button-visibility contract.  
> **See also:** [Rogue – SSVR-0226](rogue.md#ssvr-0226-rogue-menu-only-shows-applicable-continuation-actions) — matching Rogue continuation contract.

### SSVR-0274: Retry is unavailable in Rogue mode
- **Status:** 🔧 Implemented
- Given the player is in Rogue mode
- When they view scorecard or stage review actions
- Then `Retry` is not offered as an available action
- And Rogue progression is not rewound through scorecard retry behavior.

## Leaderboard And Detailed Scorecard Interaction

### SSVR-0275: Pause menu leaderboard is stage-scoped
- **Status:** 🔧 Implemented
- Given the player is in a shooter box and opens the pause menu
- When leaderboard content is available
- Then the leaderboard panel is scoped to the current stage.

> **See also:** [Leaderboards – SSVR-0281](leaderboards.md#ssvr-0281-leaderboard-appears-as-pause-menu-panel) — leaderboard panel behavior.

### SSVR-0276: Leaderboard row selection is shot-driven
- **Status:** 🔧 Implemented
- Given the leaderboard panel is visible
- When the player shoots a record row once
- Then that row is selected
- And when the player shoots the same row a second time, a detailed scorecard panel opens.

### SSVR-0277: Detailed scorecard close uses two-shot close flow
- **Status:** 🔧 Implemented
- Given a detailed scorecard panel is open
- When the player shoots the panel once
- Then close is armed
- And when they shoot again, the panel closes.
