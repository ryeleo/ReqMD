# Acceptance Criteria

This document is a core product-behavior spec for Speed Steel VR.

Use it to define exactly how game features should behave in a testable format.

## How To Use This Document

- Keep criteria in Given/When/Then format.
- Prefer stable IDs so criteria can be referenced in code reviews, commits, and QA notes.
- Add criteria here when behavior is agreed upon.
- If behavior changes, update the existing criterion instead of creating contradictory duplicates.
- Keep brainstorm notes in `docs/brainstorm.md`, but treat this file as the acceptance source of truth.
- Treat this file as the index. Domain criteria live under `docs/acceptance-criteria/`.

## Organization

Use heading levels to organize criteria by feature area:

- H2: Feature domain document link
- H3: Sub-feature or flow
- H4: Individual criterion ID and title

Criterion template:

- Given <starting state>
- When <player/system action>
- Then <required outcome>
- And <additional required outcome(s)>

Status metadata template:

- **Status:** `💡 Proposed`, `🔧 Implemented`, or `✅ Verified`

Status meanings:

- `💡 Proposed`: Desired behavior is agreed enough to document, but is not yet fully implemented.
- `🔧 Implemented`: Behavior exists in code/docs, but has not yet been explicitly verified in dedicated QA.
- `✅ Verified`: Behavior has been explicitly validated in testing or other strong confirmation.

Optional future statuses:

- `⛔ Blocked`: Work is understood but currently blocked by another dependency or decision.
- `🗑️ Deprecated`: Criterion is kept for historical context but should no longer drive new implementation.

---

## Domain Documents

### Gameplay Core
- [Main Menu](docs/acceptance-criteria/main-menu.md) — startup menu, Practice/Rogue mode selection, stage-select flows
- [Pause Menu](docs/acceptance-criteria/pause-menu.md) — in-game pause, slow motion, Adjust Aim entry
- [Shot Timer](docs/acceptance-criteria/shot-timer.md) — string timing contract, start/stop triggers, display, precision
- [Scorecards](docs/acceptance-criteria/scorecards.md) — scorecard presentation, retry/attempt history, review flow
- [Leaderboards](docs/acceptance-criteria/leaderboards.md) — per-stage ranking, pause-menu panel, drilldown to scorecard
- [Rogue](docs/acceptance-criteria/rogue.md) — Rogue mode start/load flow, world-state persistence, duel progression
- [Boss AI](docs/acceptance-criteria/boss-ai.md) — boss placement, concurrent duel behavior, AI parameters, replay-backed bosses

### Firearm And Input
- [Firearm](docs/acceptance-criteria/firearm.md) — firing contract, bullet trace, ballistic origin, reflex sight trust
- [Firearm Reloading](docs/acceptance-criteria/firearm-reloading.md) — reload state machine, magazine contract, feedback, edge cases
- [Aim-Adjust Stage](docs/acceptance-criteria/aim-adjust-stage.md) — ephemeral calibration bay, playable aim-adjust modes
- [Controls](docs/acceptance-criteria/controls.md) — control schemes, input mappings, platform-specific behavior
- [Locomotion](docs/acceptance-criteria/locomotion.md) — teleport, snap-turn, suppression rules, desktop camera, XR rig
- [Teleport Undo/Redo](docs/acceptance-criteria/teleport-undo-redo.md) — teleport position history, undo/redo stack, pause menu controls

### World And Stages
- [Stage Generation](docs/acceptance-criteria/stage-generation.md) — stage build lifecycle, difficulty model, scene tool output
- [Stage Descriptions](docs/acceptance-criteria/stage-descriptions.md) — `.stage` file format, parser behavior, runtime consumption
- [Bay](docs/acceptance-criteria/bay.md) — bay layout, surface theming, target arrangement, transitions
- [Steel Target](docs/acceptance-criteria/steel-target.md) — target types, hit detection, audio/physics response, stage integration

### Menu UI Components
- [Gong Button](docs/acceptance-criteria/gong-button.md) — individual gong-button rendering, state feedback, hit detection
- [Gong Button Array](docs/acceptance-criteria/gong-array.md) — multi-button grid layout, dynamic population, refresh behavior

### Data And Persistence
- [String Replays](docs/acceptance-criteria/string-replays.md) — capture contract, schema semantics, telemetry upload, scorecard parent contract
- [Save System](docs/acceptance-criteria/save-system.md) — save slot model, auto-save, world-state and calibration persistence
- [Telemetry](docs/acceptance-criteria/telemetry.md) — event logging, replay recording, data integrity

### Polish And Platform
- [Audio Design](docs/acceptance-criteria/audio-design.md) — audio resource organization, random sampling, dB level standards, procedural fallback
- [Visual Effects](docs/acceptance-criteria/visual-effects.md) — splatters, brass ejection, spray cleaning, muzzle flash, hit particles
- [Accessibility](docs/acceptance-criteria/accessibility.md) — assistive features, input accommodations, sensory options
- [Performance](docs/acceptance-criteria/performance.md) — frame rate targets, rendering budgets, memory management
- [Development Tools](docs/acceptance-criteria/devtools.md) — editor tooling, debugging utilities, logging infrastructure


## ID Prefixes

| Prefix | Domain |
|---|---|
| `AC-MM-*` | Main Menu |
| `AC-PM-*` | Pause Menu |
| `AC-TIMER-*` | Shot Timer |
| `AC-SCORECARD-*` | Scorecards |
| `AC-LEADERBOARD-*` | Leaderboards |
| `AC-ROGUE-*` | Rogue |
| `AC-BOSS-*` | Boss AI |
| `AC-FIREARM-*` | Firearm |
| `AC-FIREARM-RELOAD-*` | Firearm Reloading |
| `AC-AIMADJUST-*` | Aim-Adjust Stage |
| `AC-CONTROLS-*` | Controls |
| `AC-LOCO-*` | Locomotion |
| `AC-TELEPORT-*` | Teleport Undo/Redo |
| `AC-STAGE-*` | Stage Generation |
| `AC-STAGEDESC-*` | Stage Descriptions |
| `AC-BAY-*` | Bay |
| `AC-STEELTARGET-*` | Steel Target |
| `AC-GONGBUTTON-*` | Gong Button |
| `AC-GONGARRAY-*` | Gong Button Array |
| `AC-REPLAY-*` | String Replays |
| `AC-SAVE-*` | Save System |
| `AC-TELEMETRY-*` | Telemetry |
| `AC-AUDIO-*` | Audio Design |
| `AC-VFX-*` | Visual Effects |
| `AC-ACCESSIBILITY-*` | Accessibility |
| `AC-PERFORMANCE-*` | Performance |
| `AC-DEVTOOLS-*` | Development Tools |

## Tracking Rule

- Every acceptance criterion should include exactly one bold `**Status:**` line directly below its heading.
- Prefer moving `💡 Proposed` -> `🔧 Implemented` -> `✅ Verified` as confidence increases.
- If implementation regresses, lower the status instead of deleting the criterion.
- Run `./scripts/update_acceptance_status_summaries.py` to regenerate per-file summary blocks from the real criterion statuses.
- Run `./scripts/update_acceptance_status_summaries.py --check` to verify summaries are in sync.
