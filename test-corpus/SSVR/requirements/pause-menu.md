# Pause Menu 

Scope: pause menu visibility, controls, locomotion suppression, and pause-menu specific actions.

<!-- acceptance-status-summary:start -->
Summary: 1💡 9🔧 1💻 0🎮 1✅ 0⚠️ 0⛔ 1🗑️
<!-- acceptance-status-summary:end -->





## Visibility And Placement

### SSVR-0176: Pause menu appears in front of player
- **Status:** 💻 Desktop-Verified
- Given gameplay is active and the pause menu is opened
- When the menu becomes visible
- Then the pause menu appears in front of the player at a fixed usable distance
- And it is not anchored to stage geometry in a way that makes it drift out of reach.

### SSVR-0177: Pause toggle key in desktop mode
- **Status:** ✅ Done
- Given desktop keyboard controls are active
- When the player presses `F`
- Then the pause menu toggles visible state.

### SSVR-0178: Shooting outside menu closes menu in desktop flow
- **Status:** 💡 Proposed
- **Priority:** 🔵 P4 - Eventually
- Given the pause menu is open in desktop mode
- When the player shoots the LED display or a steel target that is not part of the pause menu
- Then the pause menu closes.

### SSVR-0179: Pause actions use a centered gong-array slot
- **Status:** 🔧 Implemented
- Given the pause menu is shown in front of the player
- When pause-menu gong actions are placed
- Then the pause menu exposes a centered placement slot for its interactive gong array
- And the gong array owns button spacing, row growth, and centering within that slot rather than the pause menu positioning buttons one by one.

## Input And Locomotion Behavior

### SSVR-0180: Locomotion suppression while menu is open
- **Status:** 🔧 Implemented
- Given the pause menu is open
- When the player attempts snap-turn or teleport-ray activation
- Then snap-turn and teleport-ray activation are suppressed until the pause menu closes.

### SSVR-0181: Thumbstick ownership while menu is open
- **Status:** 🗑️ Deprecated
- Given the pause menu is open
- When the player moves the right thumbstick
- Then that input is reserved for pause-menu related firearm calibration behavior rather than locomotion.

## Slow Motion

### SSVR-0182: Slow Motion toggle exists
- **Status:** 🔧 Implemented
- Given the pause menu is visible
- When the player views pause-menu actions
- Then a `Slow Motion` toggle action is available.

### SSVR-0183: Slow Motion speed behavior
- **Status:** 🔧 Implemented
- Given `Slow Motion` is enabled
- When gameplay time advances
- Then game time is reduced to one quarter of normal speed
- And player control responsiveness remains functionally unaffected by the toggle intent.

## Adjust Aim Flow

### SSVR-0184: Entering Adjust Aim opens temporary calibration bay
- **Status:** 🔧 Implemented
- Given the pause menu is visible
- When the player activates `Adjust Aim`
- Then the player is moved into a temporary calibration bay
- And the pause menu is hidden while calibration is active.

> **See also:** [Aim-Adjust Stage – SSVR-0015](aim-adjust-stage.md#ssvr-0015-pause-menu-entry-point) — full entry-point contract for the calibration bay.

### SSVR-0185: Calibration readout appears on LED
- **Status:** 🔧 Implemented
- Given the player is in Adjust Aim mode
- When the calibration bay is active
- Then the stage LED presents live firearm calibration values for pitch, roll, and offsets.

### SSVR-0186: Return path from Adjust Aim
- **Status:** 🔧 Implemented
- Given the player is in Adjust Aim mode
- When they activate the return-home action for that flow
- Then temporary Adjust Aim state is cleaned up
- And the player is returned to their prior gameplay context.

> **See also:** [Aim-Adjust Stage – SSVR-0016](aim-adjust-stage.md#ssvr-0016-return-to-gameplay-path) — return-to-gameplay path contract.

## Pause Gong Tap Behavior

### SSVR-0187: Pause menu single-tap exceptions
- **Status:** 🔧 Implemented
- Given pause menu offer-tuning buttons are visible
- When the player shoots `Offers Easier` or `Offers Harder`
- Then each action executes on a single shot.

### SSVR-0188: Pause menu double-tap confirmations
- **Status:** 🔧 Implemented
- Given `Home` or `Hard Reset` is visible in pause menu
- When the player shoots one of those buttons once
- Then the button enters selected state
- And the action executes only on the required confirmation shot.
