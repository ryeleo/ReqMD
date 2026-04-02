# Gong Button Array 

Scope: multi-button grid/array layout, dynamic population, refresh behavior, and array-level performance.

<!-- acceptance-status-summary:start -->
Summary: 9💡 21🔧 0💻 0🎮 0✅ 0⚠️ 0⛔ 4🗑️
<!-- acceptance-status-summary:end -->

## Array Layout and Organization

### AC-GONGARRAY-LAYOUT-001: Grid-based array positioning
- **Status:** 🔧 Implemented
- Given a gong button array is created for menu selection (stages, offers, etc.)
- When buttons are positioned
- Then they are arranged in a logical grid pattern (rows × columns) on an arc curving around the shooter.
- And spacing is uniform and ergonomic for VR aiming
- And the arc is centered on a provided transform (shooter-box, panel, etc.), or auto-resolves to nearby shooter-box/player-camera
- And each button's rotation is adjusted so it faces toward the center point
- And button spacing respects the configured gridding (columns, rows, button-spacing distance)
- Arc positioning can be toggled on/off via `useArcLayout` boolean (default: enabled)
- Arc positioning is configured via:
  - `arcRadiusMeters`: distance from arc center to buttons (default 2m)
  - `arcAngularSpanDegrees`: total angle span left-to-right (default 110°)
  - `arcHeightOffsetMeters`: vertical offset of arc from center (default 0m)
  - `arcCenterTransform`: explicit reference to the arc center point; if null, auto-resolves
- Flat grid layout can be enabled by setting `useArcLayout = false`
- Arc layout works for arrays positioned around shooter boxes, panels, or any other central point



### AC-GONGARRAY-LAYOUT-002: Array positioning
- **Status:** 💡 Proposed
- Given multiple gong button arrays may be visible in the same bay
- When arrays are presented
- Then visual grouping or framing makes array boundaries clear to the player
- And arrays do not visually merge into a single undifferentiated mass.

### AC-GONGARRAY-LAYOUT-003: Center or focal-point anchoring
- **Status:** 🗑️ Deprecated
- **Deprecation:** This is more complicated than it needs to be. Placement should be anchored based on shooter box or shooters current position.
- Given a gong button array is placed in a bay
- When the array is positioned relative to the shooter's Ready Spot
- Then the array is anchored to a clear focal point (center, top-left, etc.)
- And all buttons remain visible within the player's comfortable aiming range.

### AC-GONGARRAY-LAYOUT-004: Incomplete-row centering
- **Status:** 🔧 Implemented
- Given a gong button array uses a configured fixed column count
- When the final row has fewer items than that column count
- Then that incomplete row is horizontally centered within the array
- And partial menu rows do not appear visually drifted left or right.

### AC-GONGARRAY-LAYOUT-005: Stage-selection array bay-midline centering
- **Status:** 🔧 Implemented
- Given a stage-selection gong array is shown in the main-menu bay
- When the array root is positioned
- Then its local X offset is reset to the bay midline
- And the array does not sit arbitrarily off to the left or right of the bay.

### AC-GONGARRAY-LAYOUT-006: One `.garray` resource can bundle multiple named layouts
- **Status:** 🔧 Implemented
- Given related menu arrays or display companions belong to the same authored resource family
- When the layouts are stored in a `.garray` file
- Then the file may contain multiple named layout documents separated by `---`
- And runtime/editor consumers can load a specific named layout from that shared resource.

### AC-GONGARRAY-LAYOUT-007: Display-only layout metadata can live beside array definitions
- **Status:** 🔧 Implemented
- Given a resource family needs both a gong array and a display-surface companion
- When the display document is authored in `.garray`
- Then it may omit `rows` and button-slot data entirely
- And it may still provide display-local position, rotation, width, and height metadata for the consuming system.

### AC-GONGARRAY-LAYOUT-008: Sparse shorthand blank cells preserve empty slots
- **Status:** 🔧 Implemented
- Given a `.garray` row uses sparse shorthand such as blank comma-separated cells
- When the row is parsed
- Then blank cells behave the same as `null`, `_`, `~`, or `empty`
- And the resulting ordered slot list preserves those empty gaps for sparse array layout.

### AC-GONGARRAY-LAYOUT-009: `.garray` documents may carry additive schema identity metadata
- **Status:** 🔧 Implemented
- Given a `.garray` document is authored for a shared layout resource
- When optional schema fields such as `version`, `id`, `kind`, or `anchor` are present
- Then the parser accepts them without breaking current name-based layout loading
- And bundle lookup may resolve a layout by either legacy `name` or stable `id`
- And existing `.garray` consumers remain backward-compatible if those fields are absent.

### AC-GONGARRAY-LAYOUT-010: Display-surface anchor metadata can drive runtime placement
- **Status:** 🔧 Implemented
- Given a display-surface layout declares an `anchor` such as `bay-root`, `shooter-box`, or `ready-spot`
- When a runtime display consumer resolves that layout
- Then authored display position and rotation are interpreted relative to that declared anchor frame
- And if the requested anchor is unavailable, the consumer falls back safely instead of breaking layout resolution.

### AC-GONGARRAY-LAYOUT-011: Next-version anchors may resolve by stable authored node id
- **Status:** 💡 Proposed
- Given a next-version layout document declares an anchor relationship
- When that anchor targets another authored node inside the same layout document
- Then the reference resolves by stable node `id` instead of fragile Unity transform name
- And built-in semantic anchors such as `bay-root`, `shooter-box`, `ready-spot`, `menu-root`, or `player` remain supported.

### AC-GONGARRAY-LAYOUT-012: Next-version layout families may live in one YAML document
- **Status:** 🔧 Implemented
- Given a menu or bay layout family needs arrays, displays, anchor-point nodes, and reference anchors together
- When the family is authored in the next layout-file version
- Then the whole family may live in one YAML document instead of many `---`-separated mini-documents
- And each authored node in that document still has a stable `id`, a declared `kind`, and explicit transform/anchor semantics.

> **Implementation notes:** First pass is additive rather than a full migration. `LayoutSceneParser` and `LayoutSceneDefinition` now support a single `layout-scene` YAML document, and the editor main-menu showcase consumes a `LayoutScenes/MainMenuShowcase` resource authored this way.

### AC-GONGARRAY-LAYOUT-013: Next-version YAML structure may mirror intended Unity parenting
- **Status:** 🔧 Implemented
- Given a layout author wants the file structure to match the intended Unity transform hierarchy
- When the next layout-file version is authored
- Then parent-child relationships can be expressed directly in YAML
- And child transforms are interpreted relative to their YAML parent unless an explicit non-parent anchor override is declared.

> **Implementation notes:** First-pass `layout-scene` parsing supports hierarchical `children` and preserves node identity throughout the parsed document tree. This is currently proven through parser coverage and additive editor/showcase adoption rather than a full runtime replacement of `.garray` consumers.

### AC-GONGARRAY-LAYOUT-014: Next-version layout documents may be centered on an authored shooter-box node
- **Status:** 💡 Proposed
- Given a layout family is meant to be composed around a central player reference
- When the next layout-file version authors a shooter-box node in that document
- Then sibling displays, gong arrays, and helper placements may anchor relative to that shooter-box node id
- And the author can reason about the whole composition from one central origin instead of spreading offsets across unrelated resources.

### AC-GONGARRAY-LAYOUT-015: Next-version semantic `player` anchor may drive player-front utility layouts
- **Status:** 💡 Proposed
- Given a next-version layout family is intended to appear in front of the player instead of at a bay-authored world location
- When a root node or major subtree anchors to semantic `player`
- Then the runtime resolves that anchor from a player-relative frame captured when the composition is shown or refreshed
- And the resulting composition stays world-stable after placement unless it is explicitly rebuilt or repositioned.

### AC-GONGARRAY-LAYOUT-016: Editor showcase may consume next-version `layout-scene` resources with v1 fallback
- **Status:** 🔧 Implemented
- Given a gong-array showcase context is being built in editor tooling
- When a matching next-version `layout-scene` resource is available
- Then the showcase may load gong-array node definitions from that v2 resource instead of only loading v1 `.garray` layouts
- And authored slot keys and sparse rows drive button population order for the showcase array
- And if the v2 resource is missing or cannot be parsed, the showcase falls back safely to the existing v1 `.garray` resource path.

## Dynamic Population

### AC-GONGARRAY-POPULATE-001: Stage list array population
- **Status:** 🗑️ Deprecated
**Deprecated:** There are actually multiple arrays planned now rather than one large array.
- Given the player enters stage selection from the main menu
- When the stage list is populated
- Then available stages are rendered as gong buttons in an array
- And the array includes only stages that are valid for the current context (new stages, existing stages, etc.).

### AC-GONGARRAY-POPULATE-002: Array refresh after stage creation
- **Status:** 🔧 Implemented
- Given the player creates a new stage
- When stage creation and registration completes
- Then the "existing stages" gong button array at the main menu bay is automatically refreshed
- And the newly created stage is immediately selectable without scene reload.

### AC-GONGARRAY-POPULATE-003: Conditional array visibility
- **Status:** 🔧 Implemented
- Given multiple gong arrays may exist in the same bay (e.g., Practice mode: new stages vs. existing stages)
- When visibility conditions change (e.g., no new stages available)
- Then arrays are shown or hidden based on context rules
- And hidden arrays do not consume interaction bandwidth or create visual clutter.

### AC-GONGARRAY-POPULATE-004: Array configuration is declarative
- **Status:** 🔧 Implemented
- Given gameplay systems create or reuse gong arrays in menus, scorecards, or utility views
- When array roots are configured
- Then layout settings such as columns, spacing, placement offset, presentation mode, and collapse rules are defined through a declarative array spec
- And callers do not each hand-author ad hoc chains of per-array configuration calls.

### AC-GONGARRAY-POPULATE-005: Array-backed button population is declarative
- **Status:** 🔧 Implemented
- Given gameplay systems populate gong arrays with menu, stage-select, or utility buttons
- When those buttons are created
- Then button properties such as action identity, labels, subtitles, tap behavior, and visual defaults are defined through declarative button specs
- And callers do not each hand-author repeated primitive creation and label-setup code for array-backed gongs.

### AC-GONGARRAY-POPULATE-006: Authored slot order drives populated button order
- **Status:** 🔧 Implemented
- Given a consumer loads a named gong-array layout with authored slot IDs
- When the array is populated from that layout
- Then buttons are created in the authored slot order from the document
- And layout-driven menu flows do not silently substitute their own hard-coded button order.

## Selection and Navigation

### AC-GONGARRAY-SELECT-001: Single-element selection within array
- **Status:** 🔧 Implemented
- Given a player shoots a gong button within an array
- When the first shot lands
- Then that specific button is selected and highlighted
- And only that button is marked as selected (no multi-select).

### AC-GONGARRAY-SELECT-002: Array action confirmation
- **Status:** 🔧 Implemented
- Given a gong button is selected within an array
- When a confirmation shot is fired at that button
- Then the array-level action (e.g., "load this stage") executes
- And the player transitions to the appropriate next state or scene.

### AC-GONGARRAY-NAV-001: No wrapping within array
- **Status:** 🗑️ Deprecated
- **Deprecation:** This doesn't make sense to me...
- Given gong arrays are interacted with via direct shot selection
- When reviewing historical navigation requirements
- Then index-based previous/next traversal is not part of the current gong-array interaction model
- And wraparound semantics are intentionally out of scope for this domain.

## Scaling and Performance

### AC-GONGARRAY-PERF-001: Array rendering pagination
- **Status:** 💡 Proposed
- Given a gong button array contains enough buttons that showing all of them at once would materially hurt usability or performance
- When the array is rendered
- Then gong buttons can be rendered in paginated or otherwise windowed subsets (for example 20 buttons per page)
- And frame rate is not materially impacted by gong array rendering.


### AC-GONGARRAY-PERF-002: Large array memory footprint
- **Status:** 💡 Proposed
- Given an array may grow to contain many stage options (10+ stages)
- When memory and render cost are evaluated
- Then the array implementation scales gracefully
- And memory usage remains proportional to button count (no exponential overhead).

## Persistence and State

### AC-GONGARRAY-STATE-001: Array state persistence across menu transitions
- **Status:** 🗑️ Deprecated
**Deprecated:** We do not want this behavior!
- Given a player navigates away from a gong button array and returns
- When they come back to that array in the same session
- Then the array retains its previous state (selections, scroll position if applicable)
- And the transition is seamless.

### AC-GONGARRAY-STATE-002: Array reset on mode change
- **Status:** 💡 Proposed
- Given a player is exploring an array in Practice mode
- When they switch between Practice and Rogue modes
- Then the Practice array state is not carried over
- And the new array starts in a clean, context-appropriate state.

## Contextual Variants

### AC-GONGARRAY-CONTEXT-STAGES-001: Stage selection array behavior
- **Status:** 🔧 Implemented
- Given a stage-selection gong array is visible
- When a stage button is shot once
- Then that stage is selected and highlighted
- And when shot again, the stage is loaded/generated
- And when shot a third time, the player is teleported to that stage.

### AC-GONGARRAY-CONTEXT-OFFERS-001: Offer selection array behavior
- **Status:** 🔧 Implemented
- Given an "offers" gong array presents difficulty/skill adjustments
- When the player shoots an offer button once
- Then that offer is selected
- And when shot again, the offer is confirmed and applied.

### AC-GONGARRAY-CONTEXT-PRACTICE-001: Existing-stages array behavior
- **Status:** 🔧 Implemented
- Given the "existing stages" gong array is shown after Continue in Practice
- When a player shoots an existing stage button
- Then that stage loads directly (no new generation, no generator UI)
- And the player is teleported into the already-existing stage.

## Accessibility

### AC-GONGARRAY-A11Y-001: Array navigation via verbal callouts
- **Status:** 💡 Proposed
- Given a gong button array is displayed
- When accessibility audio is enabled
- Then each button or group can be announced with descriptive labels
- And auditory feedback helps players navigate without perfect aiming.

## Tooling And Evaluation

### AC-GONGARRAY-TOOL-001: Editor scene can spawn representative array-width comparisons
- **Status:** 💡 Proposed
- Given gong-array sizing and row behavior still need iterative tuning
- When a developer wants to compare common menu-array configurations
- Then an editor tool can create a scene that spawns representative array layouts such as 10, 12, 14, 16, 18, and 20 columns
- And the scene makes incomplete-row centering and spacing tradeoffs visible without requiring trial-and-error inside live gameplay flows.
