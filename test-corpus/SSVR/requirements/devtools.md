# Development Tools 

Scope: editor tooling, debugging utilities, logging infrastructure, and development-only features.

<!-- acceptance-status-summary:start -->
Summary: 5💡 4🔧 0💻 0🎮 4✅ 0⛔ 1🗑️
<!-- acceptance-status-summary:end -->




## Editor Tools

### SSVR-0064: Scene creation from menu
- **Status:** ✅ Done
- Given the Unity editor is open
- When Tools > Create Scene: Start Menu is invoked
- Then a fresh start menu scene is generated with correct setup and all dependencies
- And scene is ready for immediate play testing.

### SSVR-0065: Stage editor tooling
- **Status:** 🗑️ Deprecated
**Deprecated:** I haven't used this in forever
- Given a `.stage` file exists
- When Tools > Edit Scene: Test a Stage is invoked
- Then a stage scene is generated from the file definition
- And the StageBuilder can be re-run to iterate on procedural generation without scene save.

### SSVR-0066: Build and deploy scripting
- **Status:** ✅ Done
- Given source code and Unity project are up to date
- When `./scripts/build-and-run.sh` is executed
- Then project is built (if needed), packaged as APK, and deployed to connected Quest device
- And build errors are reported clearly.

## Logging and Debugging

### SSVR-0067: Developer panel accessible from pause menu
- **Status:** 🔧 Implemented
- Given the game is paused
- When a developer mode is enabled
- Then a developer panel button appears in the pause menu
- And selecting it opens an overlay panel with organized settings and debugging controls.
- **Implementation notes:** First pass is a dedicated `Debug Menu` pause-menu entry that opens a compact mini-gong developer submenu. It now includes `Overview`, `Logs`, `Telemetry`, and `Replay` tabs, plus contextual actions for XR diagnostics, manual XR snapshots, replay/diagnostics endpoint probes, replay upload toggling, desktop drone-view toggling, log filtering, and latest-replay re-upload.

### SSVR-0068: Developer panel uses tab-based organization
- **Status:** 🔧 Implemented
- Given the developer panel is open
- When tabs are displayed (e.g., "Logging", "Settings", "Replay", "Telemetry")
- Then each tab groups related settings and controls
- And users can switch between tabs without closing the panel
- And tab selection state persists during the session.
- **Implementation notes:** First pass provides `Overview`, `Logs`, `Telemetry`, and `Replay` tabs in the pause-menu developer submenu. Tab selection persists while the pause menu stays open during the session.

### SSVR-0069: Logging tab shows recent debug output
- **Status:** 🔧 Implemented
- Given the developer panel Logging tab is active
- When debug logs are generated during gameplay
- Then recent log entries are displayed in a scrollable view
- And log level filtering (Debug, Info, Warning, Error) is available
- And logs can be cleared without interrupting gameplay.
- **Implementation notes:** First pass uses an in-memory recent-log buffer shown in the `Logs` tab. It supports filter cycling (`All`, `Warn+Err`, `Errors`) and clear-log actions from mini gong buttons. The current presentation is text-panel based rather than a dedicated scroll widget.

### SSVR-0070: Settings tab allows runtime configuration
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given the developer panel Settings tab is active
- When development toggles exist (e.g., verbose logging, frame rate cap, replay inspection)
- Then each setting is presented as a toggle or dropdown within the tab
- And changes apply immediately to the running game.

### SSVR-0071: Replay tab provides quick inspection
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given the developer panel Replay tab is active
- When a replay file has just been recorded
- Then metadata, keyframe count, and basic integrity checks are displayed
- And the developer can choose to export, (re-)upload to telemetry, or delete the replay.
- **Implementation notes:** First pass now displays latest-replay metadata, keyframe counts, target-hit counts, origin/relative-keyframe integrity checks, on-disk file name, and tracked upload state, and it exposes a `Replay Send` action to re-upload the latest replay. Export/delete flows are still pending.

### SSVR-0072: Telemetry tab shows submission status
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given the developer panel Telemetry tab is active
- When telemetry events are queued or submitted
- Then submission status, queue depth, and endpoint health are visible
- And developers can manually trigger a submission or clear the queue.
- **Implementation notes:** First pass now shows replay and diagnostics endpoint summaries, latest upload status, tracked upload counts, replay-endpoint and diagnostics-endpoint probes, and a `Telem Upload` toggle plus `Replay Send` action. Queue depth and queue-clearing are still pending because the current telemetry client is best-effort rather than queue-backed.

## Telemetry Developer Access

### SSVR-0073: Local replay inspection
- **Status:** ✅ Done
- Given a replay file exists locally
- When a developer tool is run to inspect it
- Then replay events, waypoints, and metadata are readable in a human-friendly format
- And replay integrity can be verified before submission.
- **Verification:** Ran `python scripts/inspect_replay.py --dir ShooterReplays --latest 1 --show-waypoints 5` and confirmed metadata, waypoints, target hits, and integrity checks are printed.

### SSVR-0074: Offline development capability
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given development is happening locally
- When the telemetry server is unavailable or offline
- Then the game degrades gracefully without crashing
- And events are queued or logged locally for later submission.

## Validation and Linting

### SSVR-0075: Stage file schema validation
- **Status:** ✅ Done
- Given a `.stage` file is created or modified
- When a validation tool is run
- Then the file is checked against the schema in `docs/stage-format.md`
- And validation errors are reported with line numbers and suggested fixes.

Verification notes:
- Added `scripts/validate_stage_file.py` to validate one file (`--file`) or all files in a directory (`--dir`).
- Verified with `python scripts/validate_stage_file.py --dir Assets/Resources/Stages` and all current stage files pass.

### SSVR-0076: Code style checking
- **Status:** 💡 Proposed
- **Priority:** 🔵 P4 - Eventually
- Given C# source changes are made
- When a linter is run (or integrated into build)
- Then namespace conventions, naming patterns, and code structure are validated
- And violations are reported without blocking compilation.

### AC-DEVTOOLS-TEST-001: VS Code tasks expose Unity test entry points
- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- Given a developer is working in VS Code
- When they run `Tasks: Run Task` from the Command Palette
- Then workspace tasks exist for Unity EditMode tests, Unity PlayMode tests, and the combined Unity test pass
- And those tasks invoke the canonical repository scripts without requiring the developer to remember the shell commands.
- **Implementation notes:** Workspace tasks now live in `.vscode/tasks.json` and favor the reliable open-editor test paths by default for EditMode, PlayMode, and combined runs, while explicit `(Batchmode)` variants remain available. Prompt-based filtered open-editor tasks are included for fast single-class NUnit runs. `Unity Compile Check` is the default VS Code build task and runs the headless compile wrapper so `Cmd+Shift+B` works without a pre-opened Unity editor, while `Unity Compile Check (Open Editor)` remains available for the faster in-editor refresh path. The headless test shell wrappers now clear stale XML files before each run and emit a specific diagnosis when Unity exits successfully but fails to export a results XML file.
