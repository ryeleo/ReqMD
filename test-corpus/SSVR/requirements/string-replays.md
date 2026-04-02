# String Replays 

Scope: string replay capture, schema semantics, telemetry upload, replay diagnostics, boss/replay compatibility behavior, and replay-parent scorecard contracts.

<!-- acceptance-status-summary:start -->
Summary: 5💡 10🔧 2💻 0🎮 6✅ 0⚠️ 4⛔ 0🗑️
<!-- acceptance-status-summary:end -->





## Capture Contract

### SSVR-0287: Replay capture occurs for recorded strings
- **Status:** ✅ Done
- Given a gameplay string is recorded successfully
- When replay capture completes
- Then a string replay record is produced for that string.

### SSVR-0288: Replay keyframes are origin-relative
- **Status:** ⛔ Blocked
- **Priority:** 🟠 P1 - High
- **Blocked:** Replay inspection and validation tooling is still too weak to verify origin-relative keyframes with confidence; this needs a purpose-built verification path rather than manual JSON inspection.
- Given a new replay capture is recorded
- When keyframes are serialized
- Then they are stored relative to the shooter-box replay origin instead of raw world space.

- **Status:** 💻 Desktop-Verified
- **Status:** 🔧 Implemented
- Given replay capture is about to be saved
- When shooter-box origin cannot be resolved at string start
- Then that replay capture is skipped instead of persisting ambiguous spatial data.

### SSVR-0289: Start-position keyframe is captured at string start
- **Status:** ✅ Done
- Given a string begins
- When replay recording starts
- Then a `StartPosition` replay keyframe is recorded at split time `0.0`.

### SSVR-0290: Trigger release emits replay intent keyframe
- **Status:** ⛔ Blocked
- **Priority:** 🟡 P2 - Medium
- **Blocked:** The current verification path does not clearly prove that trigger-release intent is emitted without also registering a scoring shot.
- Given the player releases the trigger after firing flow
- When replay capturing
- Then a `TriggerRelease` keyframe is emitted without registering a scoring shot.

### SSVR-0291: Ready-spot departure captures reaction onset
- **Status:** ✅ Done
- Given the player leaves the ready pose meaningfully
- When replay capturing
- Then a `ReadySpotDeparture` keyframe is recorded to preserve reaction-time onset.

### SSVR-0292: Post-string observation is sampled after string end
- **Status:** ✅ Done
- Given a string has completed
- When replay capturing
- Then post-string behavior is recorded using decaying sample density after string completion.

## Replay Schema Contract

### SSVR-0293: Replay records are schema-versioned
- **Status:** ✅ Done
- Given a replay record is serialized
- When the record is emitted (e.g. to disc or telemetry)
- Then it includes a replay schema version value.

### SSVR-0294: Replay keyframe kinds distinguish intent
- **Status:** ✅ Done
- Given replay keyframes are stored or consumed
- When keyframe semantics are evaluated
- Then keyframe kinds distinguish at least `Shot`, `TriggerRelease`, `StartPosition`, `PostStringObservation`, and `ReadySpotDeparture` intent.

### SSVR-0295: Stage name and version are in every replay
- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- Given a replay record is serialized
- When metadata is written for playback, debugging, or telemetry
- Then stage name and stage version are top-level replay JSON fields.

### SSVR-0296: Replay schema version increments for flattened metadata layout
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given replay JSON moves metadata out of nested `replay` structures
- When the flattened top-level schema is emitted
- Then replay schema version is incremented to a new value
- And consumers can branch parsing by schema version.

### SSVR-0297: Replay payload contains top-level metadata plus keyframes
- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- Given a replay record is serialized in the new schema version
- When payload structure is validated
- Then replay overall metadata fields are top-level fields
- And metadata includes objects such as `replayOriginPosition`, `replayOriginRotation`, and `settingsSnapshot` at the top level (including difficulty and accessibility settings)
- And `keyframes` is a top-level array containing the keyframes with all per-shot data and metadata.


## Scorecard Integration (Golden Data Contract)

### SSVR-0298: Replay record is the parent record for scorecard data
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- Given a string replay has been recorded
- When scorecard data is persisted or reconstructed
- Then the replay record is the parent source of truth
- And scorecard data does not require an independent root record lifecycle.

> **See also:** [Scorecards – SSVR-0252](scorecards.md#ssvr-0252-scorecards-are-child-data-of-string-replays) — scorecard side of the golden-data contract.

### SSVR-0299: Scorecard rows reference replay identity
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- Given scorecard rows are indexed for runtime or backend queries
- When rows are stored or transmitted
- Then each scorecard row references the replay identity (`replayId`) as its parent key.

### SSVR-0300: Leaderboard indexing may denormalize but remains replay-linked
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given leaderboard/query scalability requires additional indexed tables
- When score-related data is denormalized for performance
- Then denormalized rows keep a foreign-key style link to parent replay identity
- And replay lineage remains traceable for every leaderboard entry.

### SSVR-0301: Scorecard projection is deterministic from replay payload
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- Given a replay payload and its scoring rules are available
- When scorecard projection is computed
- Then string splits, penalties, misses, and totals are deterministically reproducible
- And repeated projection yields the same scorecard output for identical replay input.

## Replay Playback And Compatibility

### SSVR-0302: Playback fires only on shot keyframes
- **Status:** ⛔ Blocked
- **Priority:** 🟠 P1 - High
- **Blocked:** Replay playback is not currently in a verification-ready state, so shot-keyframe-only behavior cannot be validated yet.
- Given replay playback interpolates through recorded keyframes
- When scoring or firing behavior is reproduced
- Then only `Shot` keyframes register shot events
- And non-shot keyframes do not generate extra scoring shots.

- **Status:** ⛔ Blocked
**Blocked:** Boss-playback compatibility validation can wait until replay playback is functional again.
- **Status:** 🔧 Implemented
- Given a replay is considered for boss playback compatibility
- When required origin-relative metadata is missing
- Then that replay is rejected for compatibility use.

## Local Persistence And Telemetry

- **Status:** 💻 Desktop-Verified
- **Status:** 🔧 Implemented
- Given a replay is recorded
- When persistence completes
- Then the replay remains stored locally in save/archive data.

### SSVR-0303: Replay is uploaded best effort to telemetry gateway
- **Status:** 🔧 Implemented
- Given a replay is recorded
- When telemetry upload is attempted
- Then the replay is wrapped in a telemetry envelope and posted best effort to the telemetry gateway.

### SSVR-0304: Desktop and Quest use different endpoint selection rules
- **Status:** 🔧 Implemented
- Given replay telemetry upload is attempted
- When endpoint selection occurs
- Then desktop or editor builds prefer the desktop telemetry URL
- And Quest or Android prefers the Quest telemetry URL when configured.

### SSVR-0305: Full replay blob and indexed metadata are both retained
- **Status:** 🔧 Implemented
- Given the telemetry gateway accepts replay telemetry
- When storage completes
- Then full replay JSON is retained in blob storage
- And indexed replay metadata is stored in PostgreSQL.

## Replay Diagnostics

### SSVR-0306: Scorecard shows last replay telemetry upload state
- **Status:** 🔧 Implemented
- Given a replay telemetry attempt has or has not occurred
- When the scorecard is shown
- Then a telemetry diagnostics line communicates the last replay upload state and timestamp context.

### SSVR-0307: Diagnostics distinguish never uploaded, success, and failure
- **Status:** 🔧 Implemented
- Given replay telemetry status is reported in-game
- When diagnostics text is updated
- Then it distinguishes `never uploaded`, successful upload, and failed upload states.
