# Bay 

Scope: bay layout, surface theming, target arrangement, and bay-level procedural variations.

<!-- acceptance-status-summary:start -->
Summary: 9💡 0🔧 0💻 0🎮 0✅ 0⚠️ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->




## Bay Structure

### SSVR-0030: Bay grid layout
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given a bay is created at a specific level in a stage
- When procedural layout is generated
- Then bay consists of a rectangular grid area with defined ground and berm boundaries
- And dimensions scale appropriately for the stage difficulty level.

### SSVR-0031: Target arrangement
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given a bay is populated with targets
- When target positions are randomized according to stage parameters
- Then no two targets occupy the same location
- And all targets remain within bay boundaries.

## Surface Theming

### SSVR-0032: Ground material variation
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given a bay is created
- When StageBuilder inspector assigns level-based overrides
- Then ground material is selected based on bay level or index range
- And material persists consistently through all bays at that level.

### SSVR-0033: Berm and safe-area theming
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given berms and safe areas are rendered
- When level-based theming is applied
- Then berm color/material and safe-area visual treatment match the level's theme
- And contrast with ground and targets remains sufficient for visual clarity.

### SSVR-0034: Lighting and atmosphere
- **Status:** 💡 Proposed
- **Priority:** 🔵 P4 - Eventually
- Given a bay is active
- When ambient lighting is applied
- Then lighting tone matches the stage theme (indoor/outdoor, dawn/dusk, etc.)
- And target visibility and sight-picture clarity are maintained.

## Bay Population

### SSVR-0035: Target density
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given a bay is generated at a specific difficulty level
- When targets are placed
- Then target count scales with difficulty (easier levels have fewer targets, harder levels have more)
- And density remains within playable bounds (shootable in reasonable time).

### SSVR-0036: Obstacle and hazard placement
- **Status:** 💡 Proposed
- **Priority:** ☁️ P5 - Dreams
- Given a bay includes dynamic obstacles or hazards (if any)
- When positions are randomized
- Then obstacles do not spawn on top of targets or within player safe zones
- And hazards are telegraphed visually and audibly.

## Bay Transitions

### SSVR-0037: Bay entry positioning
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given a player completes a bay and advances to the next
- When the next bay loads
- Then the player is positioned safely outside the bay's shooting zone
- And camera/orientation is set for clear visibility of the bay layout.

### SSVR-0038: Bay reset between runs
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given a bay is played through again (after restart)
- When the bay resets
- Then all targets, obstacles, and environmental state return to initial state
- And no stale data from the previous run persists.
