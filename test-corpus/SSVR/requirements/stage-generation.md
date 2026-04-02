# Stage Generation 

Scope: stage build lifecycle, stage definitions, difficulty, generated scene setup, and selection behavior.

<!-- acceptance-status-summary:start -->
Summary: 1💡 12🔧 0💻 0🎮 1✅ 0⚠️ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->





## Build Lifecycle

### SSVR-0327: Stage build is tool-driven
- **Status:** ✅ Done
- Given runtime gameplay starts
- When `StageBuilder` initializes
- Then stage generation does not auto-run from `Start()`
- And stage build is performed by scene tools or explicit build actions.

### SSVR-0328: Stage definitions parse from stage files
- **Status:** 🔧 Implemented
- Given `.stage` files exist in the stage resources path
- When stage content is loaded
- Then stage definitions are parsed from those files through the stage parser.

### SSVR-0329: Bay theming is builder-controlled
- **Status:** 🔧 Implemented
- Given bay surface theming settings are configured
- When a stage is built
- Then bay-level overrides in stage builder control ground and berm theming
- And theming is not defined by the `.stage` schema.

> **See also:** [Bay – SSVR-0032](bay.md#ssvr-0032-ground-material-variation) — bay ground material variation contract.

## Stage Selection And Offers

### SSVR-0330: Built-stage exclusion in new offers
- **Status:** 🔧 Implemented
- Given one or more stages are already built in the current world
- When new stage offers are generated
- Then offers exclude stages already built in the scene
- And if every available stage is already built, exclusion is lifted so offers are not empty.

### SSVR-0331: Existing-stage selection does not regenerate
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- Given an existing built stage is selected from existing-stage options
- When the selection is confirmed
- Then the player is sent directly to that stage
- And no duplicate stage generation occurs for that selection.

## Difficulty Model

### SSVR-0332: Parser computes stage difficulty rating
- **Status:** 🔧 Implemented
- Given a valid parsed stage definition
- When difficulty is evaluated
- Then a difficulty rating is computed using the parser's geometry-based model.

### SSVR-0333: Difficulty uses shooter-perspective angular metrics
- **Status:** 🔧 Implemented
- Given stage geometry with target positions and sizes
- When difficulty components are calculated
- Then target apparent size and spacing are evaluated using shooter-perspective angular measurements
- And variability in those measurements contributes to final difficulty.

### SSVR-0334: Difficulty logging output is available
- **Status:** 🔧 Implemented
- Given a stage is built
- When diagnostics logging is enabled
- Then stage difficulty breakdown logs include per-target angular metrics and weighted component summaries.

## Scene Tool Output

### SSVR-0335: Layout-authored shooter-box nodes can define the canonical bay reference origin
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given a next-version layout document authors a shooter-box placement node for a bay or menu composition
- When stage-generation or menu-generation code consumes that document
- Then the generated shooter box uses that authored transform as its canonical reference origin
- And other layout-authored displays, arrays, or helper placements may anchor relative to that shooter-box node.

### SSVR-0336: Generated scenes include locomotion stack
- **Status:** 🔧 Implemented
- Given a new scene is generated with scene tools
- When generation completes
- Then XR teleport locomotion and snap-turn components are present in the generated runtime setup.

### SSVR-0337: Startup menu scene generation path exists
- **Status:** 🔧 Implemented
- Given the user executes the start-menu scene tool action
- When scene generation completes
- Then a fresh startup scene is created with runtime systems and startup menu content.

### SSVR-0338: Scene tool replace/add safety prompt
- **Status:** 🔧 Implemented
- Given a runtime root already exists in the current scene
- When the stage scene tool is executed again
- Then the user is prompted to replace, add another, or cancel.

### SSVR-0339: Generated rig includes camera tracking guard
- **Status:** 🔧 Implemented
- Given a scene is created through scene tools
- When setup completes
- Then generated XR rig includes camera tracking guard configuration for stable XR tracking ownership.

### SSVR-0340: Build-and-run picks latest Game scene
- **Status:** 🔧 Implemented
- Given multiple `Game*.unity` scenes exist
- When build-and-run resolves the target scene
- Then the newest scene by numeric suffix is selected automatically.
