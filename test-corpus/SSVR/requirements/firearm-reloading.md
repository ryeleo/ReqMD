# Firearm Reloading 

Scope: reload-state machine, magazine/chamber behavior, user input handling, audiovisual feedback, and failure/recovery flows.

<!-- acceptance-status-summary:start -->
Summary: 6💡 8🔧 0💻 0🎮 0✅ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->




## Reload State Machine

### SSVR-0077: Reload state machine has explicit phases
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- Given firearm reloading is active gameplay behavior
- When reload logic is executed
- Then reload progression follows explicit, named phases (for example idle, eject, insert, chamber, ready)
- And transitions are deterministic.

### SSVR-0078: Invalid phase transitions are rejected safely
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- Given reload input arrives out of order
- When the current state does not allow that transition
- Then the invalid transition is ignored or rejected
- And gameplay remains stable without soft-lock.

## Magazine And Chamber Contract

### SSVR-0079: Magazine capacity contract is enforced
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- Given the firearm has a configured magazine capacity
- When rounds are inserted or consumed
- Then ammo counts never exceed configured limits
- And underflow below zero is prevented.

### SSVR-0080: Chambered round behavior is explicit
- **Status:** 🔧 Implemented
- **Priority:** 🟡 Medium
- Given a round may or may not be chambered during reload actions
- When magazine ejection, insertion, or chamber actions occur
- Then chamber state updates follow explicit rules
- And resulting available-shot count is consistent with that state.

### SSVR-0081: Empty-mag and empty-chamber dry-fire behavior is consistent
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- Given the player attempts to fire with insufficient ammo state
- When trigger input is processed
- Then dry-fire behavior is consistent and repeatable
- And no shot is scored until ammo/chamber state is valid.

## Input And Timing

### SSVR-0082: Reload action mapping is explicit and stable
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- Given reload controls are mapped by scheme
- When a reload-related input is triggered
- Then the intended reload sub-action is invoked consistently.

### SSVR-0083: Held input and repeat input are debounced
- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- Given reload actions can be hold-driven or repeatedly pressed
- When input polling runs across frames
- Then duplicate unintended triggers are suppressed
- And intended repeated actions still work as designed.

### SSVR-0084: Reload timing windows are deterministic
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- Given reload operations have timing gates or animation windows
- When the same sequence is repeated under equivalent conditions
- Then accepted/rejected timing outcomes remain deterministic.

## Player Feedback

### SSVR-0085: Reload phase feedback is visible/audible
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- Given the player performs reload actions
- When reload phase changes occur
- Then at least one clear cue confirms progression (audio, visual, or haptic).

### SSVR-0086: Failure feedback is explicit
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- Given reload input fails due to invalid state or timing
- When the action is rejected
- Then failure feedback indicates why no progression occurred.

## Error Recovery And Edge Cases

### SSVR-0087: Reload recovers after interrupted actions
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- Given reload actions are interrupted (pause, state reset, or conflicting input)
- When gameplay resumes
- Then firearm state recovers to a valid reload or ready state without corruption.

### SSVR-0088: Reload and stage transitions do not corrupt ammo state
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- Given stage resets, retries, or transitions occur
- When firearm/runtime state is rebuilt
- Then ammo and reload state are initialized consistently for the new run.

### SSVR-0089: Reload logic remains replay-compatible
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High
- Given string replay capture/playback is enabled
- When reload-relevant events occur during a run
- Then replay data preserves enough signal to reconstruct shot validity and ammo outcomes.

## Diagnostics

### SSVR-0090: Reload debug instrumentation supports troubleshooting
- **Status:** 🔧 Implemented
- **Priority:** 🟡 P2 - Medium
- Given reload bugs are investigated
- When diagnostics are enabled
- Then logs or debug overlays expose current reload phase and ammo/chamber state transitions clearly.
