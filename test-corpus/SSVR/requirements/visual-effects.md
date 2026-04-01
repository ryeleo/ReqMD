# Visual Effects 

Scope: bullet-impact splatters, brass ejection, spray-paint target cleaning, muzzle flash, and hit particle effects.

<!-- acceptance-status-summary:start -->
Summary: 15💡 0🔧 0💻 0🎮 0✅ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->





## Bullet Splatters

### SSVR-0385: Bullet splatter appears at impact point on target hit
- **Status:** 💡 Proposed
- **Priority:** ☁️ P5 - Dreams
- Given the player fires a shot that hits a steel target
- When the hit is resolved
- Then a lead-splatter decal appears at the exact impact point on the target surface.

> **See also:** [SSVR-0364](steel-target.md#ssvr-0364-target-wear-and-bullet-holes) — Target wear and bullet holes.

### SSVR-0386: Splatters persist through the entire stage run
- **Status:** 💡 Proposed
- **Priority:** ☁️ P5 - Dreams
- Given splatters have accumulated on targets during a run
- When subsequent strings start in the same stage session
- Then prior splatters remain visible on the target surface
- And targets show a cumulative shot history for the session.

### SSVR-0387: Splatters reset when stage resets
- **Status:** 💡 Proposed
- **Priority:** ☁️ P5 - Dreams
- Given the stage is reset via Retry or explicit stage reset
- When reset completes
- Then all splatter decals are cleared
- And targets appear clean at the start of the fresh run.

> **See also:** [SSVR-0378](steel-target.md#ssvr-0378-visual-wear-marks-persistence-optional) — Visual wear marks persistence.

### SSVR-0388: Replay splatters appear at recorded impact positions
- **Status:** 💡 Proposed
- **Priority:** ☁️ P5 - Dreams
- Given a string replay includes bullet impact location data
- When the replay is visualized
- Then splatter decals are reproduced at the recorded positions
- And splatter placement is deterministic across repeated playback.

> **See also:** [SSVR-0365](steel-target.md#ssvr-0365-replay-splatter-appears-at-recorded-impact-points) — Replay splatter on targets.  
> **See also:** [SSVR-0317](telemetry.md#ssvr-0317-bullet-impact-location-capture) — Bullet impact location capture.


## Brass Ejection

### SSVR-0389: Brass casing ejects on each shot fired
- **Status:** 💡 Proposed
- **Priority:** ☁️ P5 - Dreams
- Given the player fires a shot
- When the shot fires
- Then a brass casing is ejected from the firearm's ejection port
- And the casing follows a physically plausible arc.

### SSVR-0390: Brass casings persist on the floor during the session
- **Status:** 💡 Proposed
- **Priority:** ☁️ P5 - Dreams
- Given one or more shots have been fired in a stage
- When casings land on the floor
- Then they remain visible for the remainder of the session
- And accumulate naturally over multiple strings.

### SSVR-0391: Brass casings do not affect gameplay or scoring
- **Status:** 💡 Proposed
- **Priority:** ☁️ P5 - Dreams
- Given brass casings are present on the floor or in the air
- When ballistic or scoring resolution occurs
- Then casings have no effect on bullet hit detection, target scoring, or timer behavior
- And are purely visual/cosmetic objects.


## Spray Paint — Target Cleaning

### SSVR-0392: Spray gong button exists in each stage bay
- **Status:** 💡 Proposed
- **Priority:** ☁️ P5 - Dreams
- Given a stage bay has been generated and is active
- When the player views the bay
- Then a `Spray` gong button is present in the bay.

### SSVR-0393: Spray requires double-tap to execute
- **Status:** 💡 Proposed
- **Priority:** ☁️ P5 - Dreams
- Given the `Spray` button is visible
- When the player shoots it once
- Then it enters selected state but splatters are not yet cleared
- And when shot a second time, the cleaning action executes.

### SSVR-0394: Spray clears all lead splatters from all targets
- **Status:** 💡 Proposed
- **Priority:** ☁️ P5 - Dreams
- Given the cleaning action executes
- When spray completes
- Then all splatter decals across all targets in the bay are removed
- And targets appear clean as if freshly placed.

### SSVR-0395: Spray has a particle effect and sound
- **Status:** 💡 Proposed
- **Priority:** ☁️ P5 - Dreams
- Given the spray cleaning action executes
- When the action runs
- Then a white-paint particle spray effect plays on each target
- And a satisfying spray-can sound accompanies the effect.

> **See also:** [SSVR-0387](visual-effects.md#ssvr-0387-splatters-reset-when-stage-resets) — Splatters also clear on stage reset.


## Muzzle Flash

### SSVR-0396: Muzzle flash plays on each shot
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given the player fires a shot
- When the shot fires
- Then a brief muzzle flash particle effect plays at the cosmetic muzzle position
- And the flash duration is sub-frame short (< 1 frame visible hold).

> **See also:** [SSVR-0099](firearm.md#ssvr-0099-cosmetic-muzzle-effects-separation) — Cosmetic muzzle effects use weapon-specific muzzle transform, not the shared ballistic origin.

### SSVR-0397: Muzzle flash uses cosmetic muzzle position, not ballistic origin
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given the cosmetic muzzle transform differs from the shared ballistic origin
- When the muzzle flash effect plays
- Then it originates from the weapon-model cosmetic muzzle transform
- And it does not alter or expose the shared ballistic-origin contract.


## Hit Particle Effects

### SSVR-0398: Steel target impact particle plays on hit
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given a bullet hits a steel target
- When the hit is resolved
- Then a brief metallic particle/ricochet effect plays at the impact point
- And the particle effect does not linger long enough to obscure the target face.

### SSVR-0399: Miss hit particle plays on environment impact
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given the player fires a shot that misses all targets
- When the round impacts a berm or floor surface
- Then a dust/impact particle plays at the miss impact point
- And the miss impact is visually distinct from a target hit.
