# Performance 

Scope: frame rate targets, rendering budgets, memory management, and optimization thresholds.

<!-- acceptance-status-summary:start -->
Summary: 7💡 0🔧 0💻 0🎮 0✅ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->




## Frame Rate Targets

### SSVR-0400: VR frame rate minimum
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given the game is running on Meta Quest 3
- When a stage is active and fully rendered
- Then frame rate is maintained at 72 FPS or higher under normal gameplay conditions
- And frame drops are logged and investigated if persistent.

### SSVR-0401: Desktop frame rate target
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given the game is running on desktop with an average gaming GPU (RTX 3060 or equivalent)
- When a stage is active
- Then frame rate is maintained at 60 FPS or higher under normal conditions
- And may exceed this target on higher-end hardware.

## Rendering Budget

### SSVR-0402: Draw call budget
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given a stage is active
- When rendering occurs each frame
- Then draw call count is maintained below 200 per frame under normal conditions
- And batching/instancing is used to consolidate geometry.

### SSVR-0403: Triangle budget
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given a stage is fully populated and rendered
- When the scene is evaluated for complexity
- Then visible triangle count stays below 500k triangles per frame on VR target hardware
- And LOD systems are used for distant geometry.

## Memory Management

### SSVR-0404: Stage memory baseline
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given a procedurally generated stage is loaded
- When stage data structures are built and populated
- Then memory footprint for stage geometry, entities, and metadata stays below 256 MB
- And memory is released when the stage is unloaded.

### SSVR-0405: Replay memory efficiency
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given a replay is recorded during a single successful stage run
- When the replay is stored in memory or on disk
- Then the replay data size is less than 5 MB
- And compression or delta encoding is used if baseline size exceeds this threshold.

## Load Times

### SSVR-0406: Stage load time
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given a stage is selected and load begins
- When stage generation, asset loading, and initialization complete
- Then time from selection to gameplay-ready state is less than 3 seconds on average Quest hardware
- And longer loads show a progress indicator.
