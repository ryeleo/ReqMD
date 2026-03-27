# Telemetry Acceptance Criteria

Scope: game event logging, replay capture, performance metrics, and telemetry data collection infrastructure.

<!-- acceptance-status-summary:start -->
Summary: 11💡 8🔧 0💻 0🎮 0✅ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->

## Event Logging

### AC-TELEMETRY-LOG-001: Shot event capture
- **Status:** 🔧 Implemented
- Given a player fires a shot at a target
- When the bullet hit is resolved
- Then a replay shot keyframe is captured with split time plus gun/muzzle pose data
- And the event is persisted for replay reconstruction and analytics.

### AC-TELEMETRY-LOG-002: Target-hit event capture with target metadata
- **Status:** 🔧 Implemented
- Given a shot hits a steel target
- When target-hit telemetry is recorded
- Then the event includes split time, target code, target name, and stop-target flag
- And target-hit sequence index is preserved for replay/score drilldown.

### AC-TELEMETRY-LOG-003: Trigger-release intent event capture
- **Status:** 🔧 Implemented
- Given the timer is running for a live string
- When the player releases the trigger
- Then a trigger-release intent keyframe is recorded with split time
- And this event does not itself count as a scoring shot.

### AC-TELEMETRY-LOG-004: Ready-spot departure transition event capture
- **Status:** 🔧 Implemented
- Given a string capture has started from the ready state
- When firearm movement exceeds configured position/rotation departure thresholds
- Then a `ReadySpotDeparture` keyframe is captured to mark reaction onset
- And it is time-aligned to string split timing.

### AC-TELEMETRY-LOG-005: String start-position event capture
- **Status:** 🔧 Implemented
- Given replay capture begins for a valid shooter box origin
- When keyframe recording initializes
- Then a `StartPosition` keyframe is recorded at split `0.0`
- And downstream telemetry consumers can anchor subsequent events to this baseline.

### AC-TELEMETRY-LOG-006: Post-string observation event sampling
- **Status:** 🔧 Implemented
- Given a string has completed
- When post-string observation telemetry runs
- Then post-string observation keyframes are emitted on a decaying sample cadence
- And these observations are persisted with the replay record.

### AC-TELEMETRY-LOG-007: Ready-spot aim dwell telemetry intent
- **Status:** 💡 Proposed
- Given the player is aiming and dwelling on the ready spot prior to beep/start
- When telemetry event coverage is evaluated
- Then telemetry includes explicit ready-spot aim/dwell start-progress-complete events
- And these events can be correlated with reaction-time and departure telemetry.

### AC-TELEMETRY-LOG-008: Runtime warning/error diagnostics capture
- **Status:** 🔧 Implemented
- Given diagnostics reporting is enabled
- When Unity warning/error/exception logs are emitted at runtime
- Then warning/error diagnostic events are captured with severity, message, stack details, and runtime snapshot
- And events are batched for diagnostics telemetry upload.

### AC-TELEMETRY-LOG-009: Telemetry reachability diagnostics
- **Status:** 🔧 Implemented
- Given replay telemetry endpoint probing is requested
- When endpoint reachability checks complete
- Then telemetry reports reachable/unreachable state with detail
- And runtime diagnostics text reflects current telemetry availability.

### AC-TELEMETRY-LOG-010: Bullet-impact location capture
- **Status:** 💡 Proposed
- Given a shot impacts stage geometry or a steel target
- When hit telemetry is recorded
- Then the event includes bullet-impact location data (at minimum world-space position)
- And the event includes sufficient context to associate the impact with replay/string identity.

### AC-TELEMETRY-LOG-011: Replay splatter reconstruction from impact telemetry
- **Status:** 💡 Proposed
- Given bullet-impact locations were captured during a recorded string
- When replay visualization is rendered for the player
- Then bullet splatters are reproduced at the recorded impact locations
- And splatter placement is deterministic across repeated playback of the same replay.

## Replay Recording

### AC-TELEMETRY-REPLAY-001: Replay waypoint capture
- **Status:** 💡 Proposed
- Given gameplay is active
- When the player moves or adjusts aim during a locked shot
- Then player position, rotation, and firearm ballistic state are captured at regular intervals
- And these waypoints are sufficient to reconstruct the shot for replay playback.

### AC-TELEMETRY-REPLAY-002: Replay persistence
- **Status:** 💡 Proposed
- Given a replay is complete
- When the player finishes a stage or exits gameplay
- Then the replay is persisted locally in a format that survives app closure
- And replays can be loaded and played back deterministically.

## Replay-Parent Score Ingestion

### AC-TELEMETRY-SCORE-001: Score ingestion is replay-parented
- **Status:** 💡 Proposed
- Given scorecard-like score data is emitted to telemetry
- When ingestion occurs
- Then score data is attached to a parent replay identity (`replayId`)
- And score ingestion does not rely on an independent scorecard root identifier.

### AC-TELEMETRY-SCORE-002: Telemetry score rows preserve replay lineage
- **Status:** 💡 Proposed
- Given score rows are indexed for analytics or leaderboard queries
- When telemetry storage writes indexed records
- Then each indexed score row preserves replay lineage via replay identity linkage
- And every leaderboard row can be traced back to parent replay data.

### AC-TELEMETRY-SCORE-003: Denormalized score indexes remain replay-linked
- **Status:** 💡 Proposed
- Given high-scale leaderboard or analytics workloads require denormalized score indexes
- When denormalized rows are produced
- Then denormalized rows keep replay-linked foreign-key style references
- And replay-based drilldown remains possible without ambiguity.

### AC-TELEMETRY-SCORE-004: Score projection is reproducible from replay telemetry payload
- **Status:** 💡 Proposed
- Given replay telemetry payloads and scoring rules are available
- When score projection is recomputed for verification or migration
- Then projected score totals/splits are reproducible from replay telemetry alone
- And recomputation does not require an external authoritative scorecard dataset.

## Performance Instrumentation

### AC-TELEMETRY-PERF-001: Frame timing metrics
- **Status:** 💡 Proposed
- Given gameplay is active
- When frames are rendered
- Then frame time, GPU time, and CPU time are sampled periodically
- And metrics are collected without materially impacting performance.

## Data Integrity

### AC-TELEMETRY-INTEGRITY-001: Telemetry versioning
- **Status:** 💡 Proposed
- Given telemetry data is logged
- When the schema or format changes
- Then new data includes version metadata for safe forward/backward compatibility
- And legacy telemetry remains parseable.
