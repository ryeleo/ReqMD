# Locomotion 

Scope: teleport locomotion, snap-turn, locomotion suppression during strings and pause menus, desktop debug camera, and XR rig stability.

<!-- acceptance-status-summary:start -->
Summary: 5💡 9🔧 0💻 0🎮 0✅ 0⚠️ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->





## Teleport Locomotion

### SSVR-0189: Player teleports to shooter boxes via gong buttons
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- Given a stage has one or more shooter boxes
- When the player shoots a shooter-box teleport gong button
- Then the player is teleported to that shooter box
- And the player is oriented toward the stage targets on arrival.

> **See also:** [SSVR-0170](main-menu.md#ssvr-0170-stage-selection-tap-sequence) — Stage select teleport on third tap.

### SSVR-0190: Teleport ray activation requires controller trigger hold
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- Given teleport locomotion is enabled
- When the player holds the teleport ray trigger
- Then a teleport arc is displayed from the controller
- And releasing the trigger while a valid landing zone is targeted executes the teleport.

### SSVR-0191: Teleport ray activation is suppressed during active strings
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- Given the player is in an active timed string
- When the player attempts to activate the teleport ray
- Then teleport ray activation is suppressed
- And no teleport occurs while timing is live.

> **See also:** [SSVR-0180](pause-menu.md#ssvr-0180-locomotion-suppression-while-menu-is-open) — Locomotion suppression while pause menu is open.

### SSVR-0192: Valid teleport landing zones are defined per stage context
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given the player activates the teleport ray
- When the arc points at a surface
- Then only designated valid landing zones accept teleport targets
- And the arc visually distinguishes valid from invalid zones.


## Snap-Turn

### SSVR-0193: Right thumbstick provides snap-turn in VR mode
- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- Given the player is in VR mode and snap-turn is enabled
- When the player flicks the right thumbstick left or right
- Then the player's view snaps by the configured turn angle increment
- And snap-turn is the only active turn behavior (smooth-turn is not used by default).

> **See also:** [SSVR-0180](pause-menu.md#ssvr-0180-locomotion-suppression-while-menu-is-open) — Snap-turn is suppressed while pause menu is open.

### SSVR-0194: Snap-turn angle is configurable
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given snap-turn is enabled
- When the turn angle is adjusted in settings
- Then snap increments scale to the configured value
- And the setting persists across sessions.

### SSVR-0195: Snap-turn is suppressed during active strings
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given the player is in an active timed string
- When the player attempts snap-turn input
- Then snap-turn does not execute
- And the turn input is ignored until the string ends.


## Locomotion Suppression

### SSVR-0196: All locomotion suppressed during active string
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- Given a timed string is live
- When the player provides teleport or turn input
- Then both teleport and snap-turn are suppressed for the duration of the string.

### SSVR-0197: All locomotion suppressed while pause menu is open
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- Given the pause menu is open
- When the player provides teleport or turn input
- Then both teleport and snap-turn are suppressed until the pause menu closes.

> **See also:** [SSVR-0180](pause-menu.md#ssvr-0180-locomotion-suppression-while-menu-is-open) — Pause menu locomotion suppression.


## Desktop Debug Camera

### SSVR-0198: Desktop mode uses first-person mouse-look camera
- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- Given the game is running in desktop/editor mode without a VR headset
- When the player moves the mouse
- Then the camera orientation follows mouse movement as first-person look
- And left-click fires the firearm.

### SSVR-0199: Desktop camera rig does not interfere with XR tracking
- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- Given both desktop rig and XR rig systems may exist in a scene
- When the game starts in desktop mode
- Then the desktop camera rig is active and XR rig tracking is disabled or disregarded
- And no tracking guard or XR system conflicts arise.


## XR Rig Stability

### SSVR-0200: VR camera floors to tracked floor level
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- Given the XR rig is active in VR mode
- When floor-level calibration is complete
- Then the player's view origin is aligned to the tracked floor
- And standing gameplay positions the player at a natural real-world height.

### SSVR-0201: Camera tracking guard prevents ownership conflicts
- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- Given multiple XR tracking setups may exist in a scene
- When the scene initializes
- Then the camera tracking guard ensures only one system holds tracking ownership
- And conflicting tracking behaviors are suppressed.

### SSVR-0202: XR rig diagnostics are available for troubleshooting
- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- Given XR rig anomalies occur (tracking loss, orientation jumps, etc.)
- When diagnostics reporting is enabled
- Then XR rig state and anomalies are logged via the diagnostics reporter
- And log entries include context sufficient to identify tracking issues.
