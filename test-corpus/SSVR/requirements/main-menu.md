# Main Menu 

Scope: startup menu, Practice menu flows, mode selection, and menu interaction behavior.

<!-- acceptance-status-summary:start -->
Summary: 1💡 20🔧 1💻 0🎮 0✅ 0⚠️ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->





## Practice Mode

### SSVR-0154: Back action from Practice menu
- **Status:** 💻 Desktop-Verified
- Given the player is at `Main Menu > Practice`
- When they select `Back`
- Then the game returns to the previous main-menu level without loading or mutating any Practice save state.

### SSVR-0155: Start creates a fresh Practice flow
- **Status:** 🔧 Implemented
- Given the player is at `Main Menu > Practice` and they do not have an existing save slot with a Practice world, there should be a `Start` option available
- When they select `Start`
- Then the game presents the normal `Select a stage` menu
- And selecting a stage generates Stage 1 and begins Practice in a fresh run context.

### SSVR-0156: Reset requires confirmation before deleting existing Practice world
- **Status:** 🔧 Implemented
- Given the player is at `Main Menu > Practice` and has an existing save slot with a Practice world
- When they select `Reset`
- Then the game enters a reset confirmation state and does not yet delete the existing Practice world
- And the player must land one additional shot on the reset confirmation target to confirm reset
- And only after that second shot does the game delete the existing Practice world and continue to the normal `Select a stage` flow.

### SSVR-0157: Continue loads existing Practice world
- **Status:** 🔧 Implemented
- Given the player has an existing Practice save slot
- When they select `Continue`
- Then the save slot is loaded into the existing Practice world.

### SSVR-0158: Practice menu only shows applicable continuation actions
- **Status:** 🔧 Implemented
- Given the player opens the Practice menu from the main menu bay
- When the game evaluates whether a continuable Practice world exists
- Then `Continue` and `Reset` is shown only when there is an existing Practice world to continue
- And when no Practice world exists, `Continue` is not shown and `Start` and is shown instead.

### SSVR-0159: Continue shows dual stage-selection options
- **Status:** 🔧 Implemented
- Given the player selected `Continue` and the Practice world is loaded
- When the main-menu bay UI is shown
- Then the normal `Select a stage` flow appears in the normal menu position
- And an `existing stages` gong array appears 7 yards behind that normal menu.

### SSVR-0160: Existing-stage quick-pick behavior
- **Status:** 🔧 Implemented
- Given the `existing stages` gong array is visible
- When the player selects an existing stage from that array
- Then the game teleports or loads directly into that already-generated stage
- And no new stage is generated as part of that selection.

### SSVR-0161: Experienced-player fallback behavior
- **Status:** 🔧 Implemented
- Given the player has completed the new-stage offer path and no new level or stage offers remain
- When the Practice menu is shown after `Continue`
- Then only the `existing stages` gong array is shown
- And the normal `Select a stage` new-stage offer UI is not shown.

### SSVR-0162: Main-menu bay persistence after leaving
- **Status:** 🔧 Implemented
- Given the player used `Continue` and then teleported away from the main-menu bay into their Practice world
- When they later return to the main-menu bay in that same Practice world session or save
- Then the `existing stages` gong array persists
- And it is the only remaining menu element in the main-menu bay going forward for that world state.

### SSVR-0163: Existing stages array refreshes after new stage creation
- **Status:** 🔧 Implemented
- Given the player creates a new stage via the normal `Select a stage` flow
- When stage generation and save registration completes
- Then the `existing stages` gong array is refreshed to include that newly created stage
- And the new stage is selectable from the `existing stages` gong array without requiring a scene reload.

## Startup Mode Selection

### SSVR-0164: Startup menu exposes Practice and Rogue modes
- **Status:** 🔧 Implemented
- Given the game has loaded to the startup bay
- When the startup menu is shown
- Then the player can see both `PRACTICE` and `ROGUE` mode options.

### SSVR-0165: Practice mode tap sequence
- **Status:** 🔧 Implemented
- Given the startup menu is visible
- When the player shoots `PRACTICE` once
- Then `PRACTICE` is selected and visually highlighted
- And when the player shoots `PRACTICE` a second time, Practice mode starts.

### SSVR-0166: Rogue mode tap sequence
- **Status:** 🔧 Implemented
- Given the startup menu is visible
- When the player shoots `ROGUE` once
- Then `ROGUE` is selected and visually highlighted
- And when the player shoots `ROGUE` a second time, Rogue mode starts.

### SSVR-0167: Practice mode restores world then shows stage selector
- **Status:** 🔧 Implemented
- Given the player confirms `PRACTICE`
- When Practice mode enters
- Then the game restores an existing Practice world when one exists
- And the stage selector grid is shown so the player can choose the next stage to add or play.

### SSVR-0168: Main menu survives world progression
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given the player advances to later bays and stages in the same world
- When they return to the main-menu bay
- Then the main menu remains available according to current world-state rules.

## Menu Interaction Contract

### SSVR-0169: Multi-tap menu action contract
- **Status:** 🔧 Implemented
- Given a menu gong action requires confirmation
- When the player lands the first shot
- Then the gong enters selected state immediately
- And the action does not execute until the required additional shot count is met.

### SSVR-0170: Stage selection tap sequence
- **Status:** 🔧 Implemented
- Given stage-selection gongs are visible
- When the player shoots a stage gong once
- Then that stage is selected and highlighted
- And when they shoot it a second time, the stage is built or loaded
- And when they shoot it a third time, the player teleports to that stage.

### SSVR-0171: Menu depth consistency
- **Status:** 🔧 Implemented
- Given main menu and stage-selection gongs are spawned
- When the player views the menu in the bay
- Then interactive menu gongs are placed at the Ready Spot forward depth so interactions occur at a consistent distance.

### SSVR-0172: Stage buttons are gong buttons, not placeholder cubes
- **Status:** 🔧 Implemented
- Given mode and stage selection UI is built
- When the player sees menu targets
- Then those targets are rendered as gong-button visuals
- And not as raw unit-cube placeholders.

### SSVR-0173: First-shot visual feedback for confirm actions
- **Status:** 🔧 Implemented
- Given a menu action requires additional confirmation shots
- When the first shot is landed
- Then the selected gong immediately reflects selected state feedback.

### SSVR-0174: Gong arrays default to horizontal target-height layout
- **Status:** 🔧 Implemented
- Given startup or submenu gong arrays are built with default menu settings
- When those arrays are spawned in the main-menu bay
- Then buttons are arranged horizontally first (multi-column before stacking)
- And each array is anchored at normal menu target height by default
- And the main menu provides the array placement anchor while the gong array owns the internal button layout.

### SSVR-0175: Main menu defines array slots instead of per-button placement
- **Status:** 🔧 Implemented
- Given the main menu may show one or more gong-button groups at once
- When startup, stage-selection, or existing-stage UI is assembled
- Then the main menu defines centered placement slots for each array relative to the bay
- And each gong array lays out its own buttons within that slot rather than the main menu hard-coding individual button transforms.
