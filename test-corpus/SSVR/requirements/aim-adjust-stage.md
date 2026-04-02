# Aim-Adjust Stage 

Scope: ephemeral firearm calibration stages, playable/scorable aim-adjust modes, and easter-egg stage behavior.

<!-- acceptance-status-summary:start -->
Summary: 10💡 0🔧 0💻 0🎮 2✅ 0⚠️ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->




## Stage Behavior

### SSVR-0007: Ephemeral stage generation
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given a player enters Adjust Aim mode from the pause menu
- When the temporary calibration bay is loaded
- Then the stage is generated as a temporary, in-memory-only instance
- And is discarded when Adjust Aim mode exits (not persisted to disk).

### SSVR-0008: Playable stage layout
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given the aim-adjust stage is active
- When the player views the bay
- Then the layout is a functional shooting stage with targets at multiple distances and heights
- And all targets are shootable with standard firearm mechanics (ballistics, zeroing).
- And telemetry and scores are recorded like a normal stage run where appropriate.

### SSVR-0009: Stage reset on exit
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given a player is in Adjust Aim mode
- When they exit back to the pause menu
- Then the temporary stage instance is destroyed
- And all state changes (target hits, shots fired) are discarded.

## Scoring and Feedback

### SSVR-0010: Shot tracking during calibration
- **Status:** 💡 Proposed
- **Priority:** 🔵 P4 - Eventually
- Given the player fires shots during an Adjust Aim session
- When shots are resolved against targets
- Then each shot is logged for immediate ballistic feedback (hit position, offset from aim point)
- And feedback is displayed live on the stage LED or HUD.

### SSVR-0011: Provisional scoring (optional)
- **Status:** 💡 Proposed
- **Priority:** ☁️ P5 - Dreams
- Given the Adjust Aim stage is playable with real targets
- When the player completes the session
- Then basic scoring may be calculated for feedback purposes
- And provisional scores are not recorded to permanent leaderboards.

## Calibration Workflow

### SSVR-0012: Firearm adjustment during session
- **Status:** ✅ Done
- **Priority:** 🟠 P1 - High
- Given the player is in Adjust Aim mode
- When they perform aim-hold calibration adjustments (pitch, roll, offset tweaks)
- Then adjustments are applied immediately to firearm state
- And subsequent shots reflect the new calibration without requiring mode restart.

### SSVR-0013: Calibration data preservation
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- Given calibration adjustments are made during an Adjust Aim session
- When the player exits back to gameplay
- Then calibration state is written back to the firearm controller
- And adjustments persist in subsequent game sessions.

> **See also:** [Firearm – SSVR-0098](firearm.md#ssvr-0098-red-dot-trust-requirement) — red-dot trust must hold after calibration changes.  
> **See also:** [Save System – SSVR-0221](save-system.md#ssvr-0221-firearm-calibration-persists-across-sessions) — calibration persisted to save slot.

### SSVR-0014: Cancellation option
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given a player has made adjustments in Adjust Aim mode
- When they press the cancel/return action
- Then adjustments are offered for confirmation before commitment
- And users may revert to pre-session calibration if desired.

## Integration with Pause Menu

### SSVR-0015: Pause menu entry point
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given the pause menu is visible during gameplay
- When the player selects Adjust Aim
- Then the pause menu hides
- And the temporary calibration stage appears centered and ready for interaction.

> **See also:** [Pause Menu – SSVR-0184](pause-menu.md#ssvr-0184-entering-adjust-aim-opens-temporary-calibration-bay) — pause-menu side of the entry contract.

### SSVR-0016: Return-to-gameplay path
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given the player is in Adjust Aim mode
- When they activate return-home or confirm adjustments
- Then the temporary stage is closed
- And the player is returned to their latest recorded gameplay location before or during the transition into Adjust Aim
- And that return location should come from the same teleport-history or undo-stack mechanism used for gameplay position restoration when available
- And the restored return point preserves the player's facing, bay context, and immediate gameplay continuity rather than sending them to a fixed home position.

> **See also:** [Teleport Undo/Redo – SSVR-0207](teleport-undo-redo.md#ssvr-0207-teleport-position-stack-contract) — return-location stack contract.
> **See also:** [Teleport Undo/Redo – SSVR-0209](teleport-undo-redo.md#ssvr-0209-teleport-position-restoration-precision) — precision requirements for restored position and facing.

### SSVR-0017: No state pollution
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- Given a player is in an active stage with targets and scores
- When they enter Adjust Aim mode
- Then the active stage is paused and hidden (not modified)
- And no shots or adjustments made in Adjust Aim are reflected in the paused stage's score or state.

### SSVR-0018: Aim-adjust actions use centered gong-array placement
- **Status:** ✅ Done
- **Priority:** 🔵 P4 - Eventually
- Given the aim-adjust stage exposes interactive gong-button actions such as return, confirm, cancel, or calibration presets
- When those actions are presented in the calibration bay
- Then they are organized through one or more gong arrays centered relative to the calibration interaction area
- And the aim-adjust stage defines the placement slot while the gong array owns button spacing and row layout.
