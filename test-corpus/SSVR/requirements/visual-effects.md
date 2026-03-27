# Visual Effects Acceptance Criteria

Scope: bullet-impact splatters, brass ejection, spray-paint target cleaning, muzzle flash, and hit particle effects.

<!-- acceptance-status-summary:start -->
Summary: 15💡 0🔧 0💻 0🎮 0✅ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->


## Bullet Splatters

### AC-VFX-SPLATTER-001: Bullet splatter appears at impact point on target hit
- **Status:** 💡 Proposed
- Given the player fires a shot that hits a steel target
- When the hit is resolved
- Then a lead-splatter decal appears at the exact impact point on the target surface.

> **See also:** [AC-STEELTARGET-VIS-003](steel-target.md#ac-steeltarget-vis-003-target-wear-and-bullet-holes) — Target wear and bullet holes.

### AC-VFX-SPLATTER-002: Splatters persist through the entire stage run
- **Status:** 💡 Proposed
- Given splatters have accumulated on targets during a run
- When subsequent strings start in the same stage session
- Then prior splatters remain visible on the target surface
- And targets show a cumulative shot history for the session.

### AC-VFX-SPLATTER-003: Splatters reset when stage resets
- **Status:** 💡 Proposed
- Given the stage is reset via Retry or explicit stage reset
- When reset completes
- Then all splatter decals are cleared
- And targets appear clean at the start of the fresh run.

> **See also:** [AC-STEELTARGET-DURABILITY-002](steel-target.md#ac-steeltarget-durability-002-visual-wear-marks-persistence-optional) — Visual wear marks persistence.

### AC-VFX-SPLATTER-004: Replay splatters appear at recorded impact positions
- **Status:** 💡 Proposed
- Given a string replay includes bullet impact location data
- When the replay is visualized
- Then splatter decals are reproduced at the recorded positions
- And splatter placement is deterministic across repeated playback.

> **See also:** [AC-STEELTARGET-VIS-004](steel-target.md#ac-steeltarget-vis-004-replay-splatter-appears-at-recorded-impact-points) — Replay splatter on targets.  
> **See also:** [AC-TELEMETRY-LOG-010](telemetry.md#ac-telemetry-log-010-bullet-impact-location-capture) — Bullet impact location capture.


## Brass Ejection

### AC-VFX-BRASS-001: Brass casing ejects on each shot fired
- **Status:** 💡 Proposed
- Given the player fires a shot
- When the shot fires
- Then a brass casing is ejected from the firearm's ejection port
- And the casing follows a physically plausible arc.

### AC-VFX-BRASS-002: Brass casings persist on the floor during the session
- **Status:** 💡 Proposed
- Given one or more shots have been fired in a stage
- When casings land on the floor
- Then they remain visible for the remainder of the session
- And accumulate naturally over multiple strings.

### AC-VFX-BRASS-003: Brass casings do not affect gameplay or scoring
- **Status:** 💡 Proposed
- Given brass casings are present on the floor or in the air
- When ballistic or scoring resolution occurs
- Then casings have no effect on bullet hit detection, target scoring, or timer behavior
- And are purely visual/cosmetic objects.


## Spray Paint — Target Cleaning

### AC-VFX-SPRAY-001: Spray gong button exists in each stage bay
- **Status:** 💡 Proposed
- Given a stage bay has been generated and is active
- When the player views the bay
- Then a `Spray` gong button is present in the bay.

### AC-VFX-SPRAY-002: Spray requires double-tap to execute
- **Status:** 💡 Proposed
- Given the `Spray` button is visible
- When the player shoots it once
- Then it enters selected state but splatters are not yet cleared
- And when shot a second time, the cleaning action executes.

### AC-VFX-SPRAY-003: Spray clears all lead splatters from all targets
- **Status:** 💡 Proposed
- Given the cleaning action executes
- When spray completes
- Then all splatter decals across all targets in the bay are removed
- And targets appear clean as if freshly placed.

### AC-VFX-SPRAY-004: Spray has a particle effect and sound
- **Status:** 💡 Proposed
- Given the spray cleaning action executes
- When the action runs
- Then a white-paint particle spray effect plays on each target
- And a satisfying spray-can sound accompanies the effect.

> **See also:** [AC-VFX-SPLATTER-003](visual-effects.md#ac-vfx-splatter-003-splatters-reset-when-stage-resets) — Splatters also clear on stage reset.


## Muzzle Flash

### AC-VFX-MUZZLE-001: Muzzle flash plays on each shot
- **Status:** 💡 Proposed
- Given the player fires a shot
- When the shot fires
- Then a brief muzzle flash particle effect plays at the cosmetic muzzle position
- And the flash duration is sub-frame short (< 1 frame visible hold).

> **See also:** [AC-FIREARM-ORIGIN-003](firearm.md#ac-firearm-origin-003-cosmetic-muzzle-effects-separation) — Cosmetic muzzle effects use weapon-specific muzzle transform, not the shared ballistic origin.

### AC-VFX-MUZZLE-002: Muzzle flash uses cosmetic muzzle position, not ballistic origin
- **Status:** 💡 Proposed
- Given the cosmetic muzzle transform differs from the shared ballistic origin
- When the muzzle flash effect plays
- Then it originates from the weapon-model cosmetic muzzle transform
- And it does not alter or expose the shared ballistic-origin contract.


## Hit Particle Effects

### AC-VFX-HIT-001: Steel target impact particle plays on hit
- **Status:** 💡 Proposed
- Given a bullet hits a steel target
- When the hit is resolved
- Then a brief metallic particle/ricochet effect plays at the impact point
- And the particle effect does not linger long enough to obscure the target face.

### AC-VFX-HIT-002: Miss hit particle plays on environment impact
- **Status:** 💡 Proposed
- Given the player fires a shot that misses all targets
- When the round impacts a berm or floor surface
- Then a dust/impact particle plays at the miss impact point
- And the miss impact is visually distinct from a target hit.
