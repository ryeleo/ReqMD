# Main Menu Acceptance Criteria

Scope: startup menu, Practice menu flows, mode selection, and menu interaction behavior.

<!-- acceptance-status-summary:start -->
Summary: 1💡 19🔧 1💻 0🎮 0✅ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->


## Practice Mode

### AC-MM-PRACTICE-001: Back action from Practice menu
- **Status:** 💻 Desktop-Verified
- Given the player is at `Main Menu > Practice`
- When they select `Back`
- Then the game returns to the previous main-menu level without loading or mutating any Practice save state.

### AC-MM-PRACTICE-002: Start creates a fresh Practice flow
- **Status:** 🔧 Implemented
- Given the player is at `Main Menu > Practice` and they do not have an existing save slot with a Practice world, there should be a `Start` option available
- When they select `Start`
- Then the game presents the normal `Select a stage` menu
- And selecting a stage generates Stage 1 and begins Practice in a fresh run context.

### AC-MM-PRACTICE-003: Reset requires confirmation before deleting existing Practice world
- **Status:** 🔧 Implemented
- Given the player is at `Main Menu > Practice` and has an existing save slot with a Practice world
- When they select `Reset`
- Then the game enters a reset confirmation state and does not yet delete the existing Practice world
- And the player must land one additional shot on the reset confirmation target to confirm reset
- And only after that second shot does the game delete the existing Practice world and continue to the normal `Select a stage` flow.

### AC-MM-PRACTICE-004: Continue loads existing Practice world
- **Status:** 🔧 Implemented
- Given the player has an existing Practice save slot
- When they select `Continue`
- Then the save slot is loaded into the existing Practice world.

### AC-MM-PRACTICE-005: Practice menu only shows applicable continuation actions
- **Status:** 🔧 Implemented
- Given the player opens the Practice menu from the main menu bay
- When the game evaluates whether a continuable Practice world exists
- Then `Continue` and `Reset` is shown only when there is an existing Practice world to continue
- And when no Practice world exists, `Continue` is not shown and `Start` and is shown instead.

### AC-MM-PRACTICE-006: Continue shows dual stage-selection options
- **Status:** 🔧 Implemented
- Given the player selected `Continue` and the Practice world is loaded
- When the main-menu bay UI is shown
- Then the normal `Select a stage` flow appears in the normal menu position
- And an `existing stages` gong array appears 7 yards behind that normal menu.

### AC-MM-PRACTICE-007: Existing-stage quick-pick behavior
- **Status:** 🔧 Implemented
- Given the `existing stages` gong array is visible
- When the player selects an existing stage from that array
- Then the game teleports or loads directly into that already-generated stage
- And no new stage is generated as part of that selection.

### AC-MM-PRACTICE-008: Experienced-player fallback behavior
- **Status:** 🔧 Implemented
- Given the player has completed the new-stage offer path and no new level or stage offers remain
- When the Practice menu is shown after `Continue`
- Then only the `existing stages` gong array is shown
- And the normal `Select a stage` new-stage offer UI is not shown.

### AC-MM-PRACTICE-009: Main-menu bay persistence after leaving
- **Status:** 🔧 Implemented
- Given the player used `Continue` and then teleported away from the main-menu bay into their Practice world
- When they later return to the main-menu bay in that same Practice world session or save
- Then the `existing stages` gong array persists
- And it is the only remaining menu element in the main-menu bay going forward for that world state.

### AC-MM-PRACTICE-010: Existing stages array refreshes after new stage creation
- **Status:** 🔧 Implemented
- Given the player creates a new stage via the normal `Select a stage` flow
- When stage generation and save registration completes
- Then the `existing stages` gong array is refreshed to include that newly created stage
- And the new stage is selectable from the `existing stages` gong array without requiring a scene reload.

## Startup Mode Selection

### AC-MM-MODES-001: Startup menu exposes Practice and Rogue modes
- **Status:** 🔧 Implemented
- Given the game has loaded to the startup bay
- When the startup menu is shown
- Then the player can see both `PRACTICE` and `ROGUE` mode options.

### AC-MM-MODES-002: Practice mode tap sequence
- **Status:** 🔧 Implemented
- Given the startup menu is visible
- When the player shoots `PRACTICE` once
- Then `PRACTICE` is selected and visually highlighted
- And when the player shoots `PRACTICE` a second time, Practice mode starts.

### AC-MM-MODES-003: Rogue mode tap sequence
- **Status:** 🔧 Implemented
- Given the startup menu is visible
- When the player shoots `ROGUE` once
- Then `ROGUE` is selected and visually highlighted
- And when the player shoots `ROGUE` a second time, Rogue mode starts.

### AC-MM-MODES-004: Practice mode restores world then shows stage selector
- **Status:** 🔧 Implemented
- Given the player confirms `PRACTICE`
- When Practice mode enters
- Then the game restores an existing Practice world when one exists
- And the stage selector grid is shown so the player can choose the next stage to add or play.

### AC-MM-MODES-005: Main menu survives world progression
- **Status:** 💡 Proposed
- Given the player advances to later bays and stages in the same world
- When they return to the main-menu bay
- Then the main menu remains available according to current world-state rules.

## Menu Interaction Contract

### AC-MM-INTERACT-001: Multi-tap menu action contract
- **Status:** 🔧 Implemented
- Given a menu gong action requires confirmation
- When the player lands the first shot
- Then the gong enters selected state immediately
- And the action does not execute until the required additional shot count is met.

### AC-MM-INTERACT-002: Stage selection tap sequence
- **Status:** 🔧 Implemented
- Given stage-selection gongs are visible
- When the player shoots a stage gong once
- Then that stage is selected and highlighted
- And when they shoot it a second time, the stage is built or loaded
- And when they shoot it a third time, the player teleports to that stage.

### AC-MM-INTERACT-003: Menu depth consistency
- **Status:** 🔧 Implemented
- Given main menu and stage-selection gongs are spawned
- When the player views the menu in the bay
- Then interactive menu gongs are placed at the Ready Spot forward depth so interactions occur at a consistent distance.

### AC-MM-INTERACT-004: Stage buttons are gong buttons, not placeholder cubes
- **Status:** 🔧 Implemented
- Given mode and stage selection UI is built
- When the player sees menu targets
- Then those targets are rendered as gong-button visuals
- And not as raw unit-cube placeholders.

### AC-MM-INTERACT-005: First-shot visual feedback for confirm actions
- **Status:** 🔧 Implemented
- Given a menu action requires additional confirmation shots
- When the first shot is landed
- Then the selected gong immediately reflects selected state feedback.

### AC-MM-INTERACT-006: Gong arrays default to horizontal target-height layout
- **Status:** 🔧 Implemented
- Given startup or submenu gong arrays are built with default menu settings
- When those arrays are spawned in the main-menu bay
- Then buttons are arranged horizontally first (multi-column before stacking)
- And each array is anchored at normal menu target height by default.
