# Steel Target 

Scope: steel-target rendering, hit behavior, sound feedback, physical response, and interaction model.

<!-- acceptance-status-summary:start -->
Summary: 16💡 11🔧 0💻 0🎮 0✅ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->




## Target Types and Sizing

### SSVR-0358: Target size variants
- **Status:** 🔧 Implemented
- Given steel targets are included in a stage
- When targets are instantiated
- Then standard sizes are supported: gong (large), 12-inch plate, 10-inch plate
- And each size is visually and physically distinct.

### SSVR-0359: Gong-style targets (stage gameplay)
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given a stage includes gong-style targets
- When targets are rendered and shot
- Then gongs behave as primary gameplay indicators with clear hit feedback
- And gongs ring and swing/recoil on impact.

### SSVR-0360: Small-plate targets (precision)
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given a stage includes small plates (10in, 12in)
- When targets are rendered and shot
- Then plates present a more challenging precision target
- And hit feedback (sound, visual) is distinct from gongs.

### SSVR-0361: Stop-Plate designation
- **Status:** 🔧 Implemented
- Given a stage includes one Stop Plate target
- When that target is identified in stage definition
- Then the Stop Plate is marked as the final target of the stage
- And hitting the Stop Plate concludes the stage run and records time.

## Visual Presentation

### SSVR-0362: Steel material appearance
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given steel targets are rendered
- When environmental lighting and reflections apply
- Then targets display realistic steel surface properties (metallic sheen, reflections)
- And surface patina or weathering may be visible at applicable texture resolutions.

### SSVR-0363: Target color coding
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given multiple targets exist in a stage
- When distinct visual identification is helpful
- Then targets may be color-coded by difficulty or type (bright vs. dull finish, painted accents)
- And color does not overwhelm realistic steel appearance.

### SSVR-0364: Target wear and bullet holes
- **Status:** 💡 Proposed
- **Priority:** ☁️ P5 - Dreams
- Given a target is struck repeatedly
- When cumulative hits occur
- Then visible impact marks, pitting, or bullet holes may accumulate on the surface
- And the target remains visually coherent and playable.

### SSVR-0365: Replay splatter appears at recorded impact points
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given a recorded replay includes bullet-impact location data
- When replay visualization is shown on steel targets
- Then splatter/impact decals appear at the recorded impact points
- And visual placement is consistent across repeated playback of the same replay.

## Hit Detection and Ballistics

### SSVR-0366: Bullet hit registration
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- Given a bullet is fired at a steel target
- When ballistic collision occurs
- Then the hit is registered for scoring and stage progression
- And hit registration is deterministic and repeatable in replays.

### SSVR-0367: Off-axis and edge hits
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- Given a bullet strikes a target at an angle or near the edge
- When hit detection evaluates the strike
- Then edge and off-axis hits are handled robustly
- And false-miss or false-hit artifacts do not occur.

### SSVR-0368: Multi-hit tolerance
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- Given a player may fire multiple shots at the same target
- When each shot registers
- Then each distinct hit is counted separately
- And the target does not become "stuck" in a hit state.

## Audio Feedback

### SSVR-0369: Steel ring sound signature by size
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given a steel target is struck
- When the hit is registered
- Then an appropriate metallic ring or clang sound is played
- And sound pitch and duration vary by target size (gongs: deep ring; small plates: higher ring).

### SSVR-0370: Impact sound spatial origin
- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- Given a target is struck
- When audio feedback plays
- Then the sound originates from the target's location in 3D space
- And panning and attenuation create proper spatial audio cues.

### SSVR-0371: Repeated impact audio variation
- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- Given a target is struck multiple times in quick succession
- When audio plays for each impact
- Then audio samples or parameters vary slightly (pitch, reverb, duration)
- And repeated strikes do not produce identically monotonous sound sequences.

### SSVR-0372: Steel ring sound sourced from WAV asset
- **Status:** 🔧 Implemented
- Given a steel target is struck
- When the impact sound plays
- Then the sound is sourced from a fixed WAV file asset in the project (not a procedurally generated tone)
- And the WAV asset is referenced via `AudioClip` field on the target or a shared audio configuration object
- And a procedural fallback tone is only acceptable if the WAV asset is missing at runtime.

### SSVR-0373: Per-shot pitch variation on ring sound
- **Status:** 🔧 Implemented
- Given a steel target is struck
- When the ring sound plays
- Then the playback pitch is randomized within a narrow range (±10% of the base pitch) on each hit
- And the randomization is independent per hit so consecutive strikes do not repeat the same pitch
- And the pitch shift is small enough that the sound remains clearly recognizable as a metallic ring.

## Physical Response

### SSVR-0374: Target recoil/swing on impact
- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- Given a steel target is struck by a bullet
- When the hit is registered
- Then the target displays a brief recoil, swing, or wobble animation
- And the physical response completes within a short time window (< 1 second).

### SSVR-0375: Recoil intensity scaled by mass
- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- Given targets of different sizes are hit with similar force
- When recoil is calculated
- Then heavier targets (gongs) display less recoil than lighter targets (small plates)
- And recoil magnitude is visually consistent with expected physics.

### SSVR-0376: No penetration through targets
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given a bullet strikes a steel target
- When the collision resolves
- Then the bullet does not penetrate through the target mesh
- And the target collision geometry blocks bullets from passing through.

## Durability and Longevity

### SSVR-0377: Target resilience across stage runs
- **Status:** 💡 Proposed
- **Priority:** 🔵 P4 - Eventually
- Given a stage is played through multiple times
- When targets are reused
- Then targets do not degrade to a non-interactive state
- And multiple plays do not accumulate wear that affects interaction.

### SSVR-0378: Visual wear marks persistence (optional)
- **Status:** 💡 Proposed
- **Priority:** ☁️ P5 - Dreams
- Given a target may accumulate visible wear marks or holes during a single run
- When the run completes
- Then wear marks reset or fade when the stage resets
- And targets begin clean for the next run.

## Stage Integration

### SSVR-0379: Target population from stage definition
- **Status:** 🔧 Implemented
- Given a `.stage` file specifies target positions, sizes, and distances
- When `StageBuilder` consumes the definition
- Then steel targets are instantiated at the correct locations with correct parameters
- And no manual placement is required.

### SSVR-0380: Stop Plate as stage terminator
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- Given a stage has a designated Stop Plate
- When the player hits the Stop Plate
- Then the stage run concludes immediately
- And time and score are finalized and recorded.

### SSVR-0381: Target reset between runs
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given a stage is replayed or restarted
- When the stage resets
- Then all targets (including partial hits and wear) are reset to initial state
- And the player begins a clean run.

## Gameplay Semantics

### SSVR-0382: Target-scored splits
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- Given a stage progresses through multiple targets
- When shots are recorded
- Then each shot is tagged with the target ID (T1, T2, etc.) or `MISS`
- And split records allow post-run analysis and replay drilldown.

### SSVR-0383: Target feedback in telemetry
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- Given telemetry and replay systems track shots
- When a shot is recorded
- Then target ID, hit position, and ballistic offset are logged
- And shot analysis can be replayed and cross-referenced with target geometry.

### SSVR-0384: Impact-position linkage for replay drilldown
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- Given a shot hits a steel target during a recorded string
- When replay/telemetry drilldown is requested
- Then each hit can be resolved to a concrete impact position on that target
- And impact-position linkage remains available for scorecard/replay analysis views.
