# Controls 

Scope: player control schemes, input mappings, locomotion controls, and platform-specific control behavior for desktop and VR play.

<!-- acceptance-status-summary:start -->
Summary: 6💡 0🔧 0💻 1🎮 1✅ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->




## Control Scheme Definitions

### SSVR-0056: Named control schemes are documented and stable
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given the game supports multiple play contexts
- When controls are presented in docs or UI
- Then each scheme has a stable name (for example `Desktop Debug`, `VR Motion Controller`)
- And mappings do not silently change between releases.

### SSVR-0057: Control scheme selection follows active runtime context
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given the player enters gameplay in desktop or VR context
- When input systems initialize
- Then the appropriate control scheme is selected for that context
- And unsupported bindings are ignored without breaking core play.

## Core Gameplay Controls

### SSVR-0058: Fire action mapping is explicit per scheme
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- Given a control scheme is active
- When the player performs fire input
- Then fire input mapping is explicitly defined for that scheme
- And the mapping is reflected in player-facing control references.

### SSVR-0059: Reload action mapping is explicit per scheme
- **Status:** ✅ Done
- **Priority:** 🟠 P1 - High
- Given a control scheme is active
- When the player performs reload input
- Then reload behavior is consistently mapped for that scheme
- And unavailable reload interactions fail gracefully.

## Locomotion And View Controls

### SSVR-0060: Teleport mode entry and cancel mappings are defined
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given teleport locomotion is enabled for a scheme
- When the player enters or cancels teleport mode
- Then both actions have explicit mappings
- And both mappings are discoverable in controls documentation.

### SSVR-0061: Turn mapping is defined per scheme
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given turning is available in gameplay
- When the player uses turn input
- Then turn mapping is explicitly defined per scheme
- And the mapping is consistent with active input source expectations.

## UI And Menu Controls

### SSVR-0062: All interactions are through Gong Buttons
- **Status:** 🎮 VR-Verified
- **Priority:** 🟠 P1 - High
- Given a player wants to move through the game,
- When player input is evaluated for those panels
- Then the interaction controls are clearly specified and consistent per scheme,
- All required locomotion in the game can happen based on are shot-driven teleportation, by shooting gong buttons or stage elements etc that teleport the player 'forward'/'backward' through this world.

## Validation And Regression Safety

### SSVR-0063: Control mapping regressions are detectable
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given control mappings evolve over time
- When a release candidate is validated
- Then there is a repeatable check that verifies core control actions per scheme
- And mapping regressions are surfaced before release.
