# String Replays Acceptance Criteria

Scope: string replay capture, schema semantics, telemetry upload, replay diagnostics, boss/replay compatibility behavior, and replay-parent scorecard contracts.

<!-- acceptance-status-summary:start -->
Summary: 7💡 8🔧 2💻 0🎮 6✅ 4⛔ 0🗑️
<!-- acceptance-status-summary:end -->


## Capture Contract

### AC-REPLAY-CAPTURE-001: Replay capture occurs for recorded strings
- **Status:** ✅ Done
- Given a gameplay string is recorded successfully
- When replay capture completes
- Then a string replay record is produced for that string.

### AC-REPLAY-CAPTURE-002: Replay keyframes are origin-relative
- **Status:** ⛔ Blocked
- **Blocked:** Gotta have a tool to actually test this - it is too hard to read the JSON data and determine if the keyframes are origin-relative or world-relative, and we don't want to just trust that they are correct without some proper tests.
- Given a new replay capture is recorded
- When keyframes are serialized
- Then they are stored relative to the shooter-box replay origin instead of raw world space.

- **Status:** 💻 Desktop-Verified
- **Status:** 🔧 Implemented
- Given replay capture is about to be saved
- When shooter-box origin cannot be resolved at string start
- Then that replay capture is skipped instead of persisting ambiguous spatial data.

### AC-REPLAY-CAPTURE-004: Start-position keyframe is captured at string start
- **Status:** ✅ Done
- Given a string begins
- When replay recording starts
- Then a `StartPosition` replay keyframe is recorded at split time `0.0`.

### AC-REPLAY-CAPTURE-005: Trigger release emits replay intent keyframe
- **Status:** ⛔ Blocked
**Blocked:** "without registering a scoring shot." is hard to test right now -- I'm unsure it is implemented yet.
- Given the player releases the trigger after firing flow
- When replay capturing
- Then a `TriggerRelease` keyframe is emitted without registering a scoring shot.

### AC-REPLAY-CAPTURE-006: Ready-spot departure captures reaction onset
- **Status:** ✅ Done
- Given the player leaves the ready pose meaningfully
- When replay capturing
- Then a `ReadySpotDeparture` keyframe is recorded to preserve reaction-time onset.

### AC-REPLAY-CAPTURE-007: Post-string observation is sampled after string end
- **Status:** ✅ Done
- Given a string has completed
- When replay capturing
- Then post-string behavior is recorded using decaying sample density after string completion.

## Replay Schema Contract

### AC-REPLAY-SCHEMA-001: Replay records are schema-versioned
- **Status:** ✅ Done
- Given a replay record is serialized
- When the record is emitted (e.g. to disc or telemetry)
- Then it includes a replay schema version value.

### AC-REPLAY-SCHEMA-002: Replay keyframe kinds distinguish intent
- **Status:** ✅ Done
- Given replay keyframes are stored or consumed
- When keyframe semantics are evaluated
- Then keyframe kinds distinguish at least `Shot`, `TriggerRelease`, `StartPosition`, `PostStringObservation`, and `ReadySpotDeparture` intent.

### AC-REPLAY-SCHEMA-003: Stage name and version are in every replay
- **Status:** 💡 Proposed
- Given a replay record is serialized
- When metadata is written for playback, debugging, or telemetry
- Then stage name and stage version are top-level replay JSON fields.

### AC-REPLAY-SCHEMA-004: Replay schema version increments for flattened metadata layout
- **Status:** 💡 Proposed
- Given replay JSON moves metadata out of nested `replay` structures
- When the flattened top-level schema is emitted
- Then replay schema version is incremented to a new value
- And consumers can branch parsing by schema version.

### AC-REPLAY-SCHEMA-005: Replay payload contains top-level metadata plus keyframes
- **Status:** 💡 Proposed
- Given a replay record is serialized in the new schema version
- When payload structure is validated
- Then replay overall metadata fields are top-level fields
- And metadata includes objects such as `replayOriginPosition`, `replayOriginRotation`, and `settingsSnapshot` at the top level (which includes difficulty and accessability settings)
- And `keyframes` is a top-level array, which contains the key frames with all their per shot data and metadata


## Scorecard Integration (Golden Data Contract)

### AC-REPLAY-SCORECARD-001: Replay record is the parent record for scorecard data
- **Status:** 💡 Proposed
- Given a string replay has been recorded
- When scorecard data is persisted or reconstructed
- Then the replay record is the parent source of truth
- And scorecard data does not require an independent root record lifecycle.

> **See also:** [Scorecards – AC-SCORECARD-DATA-001](scorecards.md#ac-scorecard-data-001-scorecards-are-child-data-of-string-replays) — scorecard side of the golden-data contract.

### AC-REPLAY-SCORECARD-002: Scorecard rows reference replay identity
- **Status:** 💡 Proposed
- Given scorecard rows are indexed for runtime or backend queries
- When rows are stored or transmitted
- Then each scorecard row references the replay identity (`replayId`) as its parent key.

### AC-REPLAY-SCORECARD-003: Leaderboard indexing may denormalize but remains replay-linked
- **Status:** 💡 Proposed
- Given leaderboard/query scalability requires additional indexed tables
- When score-related data is denormalized for performance
- Then denormalized rows keep a foreign-key style link to parent replay identity
- And replay lineage remains traceable for every leaderboard entry.

### AC-REPLAY-SCORECARD-004: Scorecard projection is deterministic from replay payload
- **Status:** 💡 Proposed
- Given a replay payload and its scoring rules are available
- When scorecard projection is computed
- Then string splits, penalties, misses, and totals are deterministically reproducible
- And repeated projection yields the same scorecard output for identical replay input.

## Replay Playback And Compatibility

### AC-REPLAY-PLAYBACK-001: Playback fires only on shot keyframes
- **Status:** ⛔ Blocked
**Blocked:** unable to play replays right now for testing, need to reimplement that
- Given replay playback interpolates through recorded keyframes
- When scoring or firing behavior is reproduced
- Then only `Shot` keyframes register shot events
- And non-shot keyframes do not generate extra scoring shots.

- **Status:** ⛔ Blocked
**Blocked:** rogue is not priority for now
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

### AC-REPLAY-STORE-002: Replay is uploaded best effort to telemetry gateway
- **Status:** 🔧 Implemented
- Given a replay is recorded
- When telemetry upload is attempted
- Then the replay is wrapped in a telemetry envelope and posted best effort to the telemetry gateway.

### AC-REPLAY-STORE-003: Desktop and Quest use different endpoint selection rules
- **Status:** 🔧 Implemented
- Given replay telemetry upload is attempted
- When endpoint selection occurs
- Then desktop or editor builds prefer the desktop telemetry URL
- And Quest or Android prefers the Quest telemetry URL when configured.

### AC-REPLAY-STORE-004: Full replay blob and indexed metadata are both retained
- **Status:** 🔧 Implemented
- Given the telemetry gateway accepts replay telemetry
- When storage completes
- Then full replay JSON is retained in blob storage
- And indexed replay metadata is stored in PostgreSQL.

## Replay Diagnostics

### AC-REPLAY-DIAG-001: Scorecard shows last replay telemetry upload state
- **Status:** 🔧 Implemented
- Given a replay telemetry attempt has or has not occurred
- When the scorecard is shown
- Then a telemetry diagnostics line communicates the last replay upload state and timestamp context.

### AC-REPLAY-DIAG-002: Diagnostics distinguish never uploaded, success, and failure
- **Status:** 🔧 Implemented
- Given replay telemetry status is reported in-game
- When diagnostics text is updated
- Then it distinguishes `never uploaded`, successful upload, and failed upload states.
