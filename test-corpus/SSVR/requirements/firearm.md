# Firearm 

Scope: firing contract, bullet behavior, visual trace behavior, calibration, and sight trust.

<!-- acceptance-status-summary:start -->
Summary: 1💡 2🔧 0💻 0🎮 7✅ 0⚠️ 0⛔ 2🗑️
<!-- acceptance-status-summary:end -->





## Shot And Trigger Contract

### SSVR-0091: Trigger reset threshold before next shot
- **Status:** ✅ Done
- Given the player has fired one shot
- When the trigger is not yet released past the reset threshold
- Then another shot cannot fire
- And once the trigger is released past threshold, firing is re-armed.

### SSVR-0092: Ready Spot safety during active stage
- **Status:** ✅ Done
- Given a stage is already armed, running, or has partial scorecard progress
- When the player shoots the Ready Spot
- Then the shot is treated as a no-op for stage reset and teleport behavior.

### SSVR-0093: Ready Spot shot retries stage after scorecard is complete
- **Status:** ✅ Done
- Given the stage scorecard is fully complete (all strings finished)
- When the player shoots the Ready Spot again
- Then the effect is identical to shooting the Retry gong button for the stage
- And a new scorecard is started
- And if the player is already dwelling on the ready spot at the moment of the shot, the shot timer arms and starts immediately on ready-spot departure.

> **See also:** [SSVR-0092](#ssvr-0092-ready-spot-safety-during-active-stage) — no-op behavior while stage is in progress.

## Bullet And Bullet Trace

### SSVR-0094: Gameplay shot resolution uses bullet hit logic
- **Status:** ✅ Done
- Given the player fires
- When bullet hit resolution occurs
- Then the gameplay hit result is resolved deterministically for scoring and interactions
- And the visual bullet trace does not alter scoring outcomes.

### SSVR-0095: Bullet body debug visibility toggle
- **Status:** 🗑️ Deprecated
**Deprecated:** We don't need this at all anymore.
- Given bullet trace visuals are enabled
- When bullet body debug visibility is toggled on
- Then the bullet body is visible during trace playback for diagnostics
- And when toggled off, only the normal trace presentation is shown.

### SSVR-0096: Bullet and bullet trace terminology contract
- **Status:** 🔧 Implemented
- Given gameplay and diagnostics language for shots
- When documenting or exposing runtime labels
- Then the gameplay hit object is referred to as `bullet`
- And the moving visual tracer is referred to as `bullet trace`.

## Ballistic Origin And Sight Trust

### SSVR-0097: Shared ballistic-origin contract
- **Status:** 🔧 Implemented
- Given supported firearms in the game
- When gameplay bullet origin is configured
- Then bullet emission uses a stable gameplay ballistic-origin contract
- And weapon model muzzle differences do not silently break replay or ghost alignment.

### SSVR-0098: Red-dot trust requirement
- **Status:** ✅ Done
- Given the red dot appears to be on target
- When a shot is fired under normal gameplay conditions
- Then the bullet result aligns with the red-dot sight picture expectation.

> **See also:** [Aim-Adjust Stage – SSVR-0012](aim-adjust-stage.md#ssvr-0012-firearm-adjustment-during-session) — calibration adjustments that affect red-dot alignment.

### SSVR-0099: Cosmetic muzzle effects separation
- **Status:** ✅ Done
- Given a firearm has visual muzzle effects
- When muzzle effect transforms differ from gameplay origin
- Then cosmetic visuals may use the weapon-specific muzzle transform
- And gameplay bullet origin remains on the shared ballistic-origin contract unless explicitly redesigned project-wide.

## Reflex Sight

### SSVR-0100: Reflex lens remains transparent
- **Status:** ✅ Done
- Given desktop or VR rendering mode
- When the reflex sight lens is presented
- Then the lens remains fully transparent for aiming visibility.

### SSVR-0101: Lens mesh visibility safety contract
- **Status:** 🗑️ Deprecated
**Deprecated:** Duplicate of SSVR-0100.
- Given runtime reflex lens setup is generated
- When lens rendering is configured
- Then the lens collider remains available for projection behavior
- And opaque lens mesh behavior is not reintroduced.

## Controller Contract

### SSVR-0102: Single-controller baseline compatibility
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given standard gameplay firearm control
- When the player uses either left- or right-hand single-controller setup
- Then core firearm control remains operable without requiring dual-controller dependency.
