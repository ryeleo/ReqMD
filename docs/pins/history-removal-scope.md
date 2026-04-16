# History/Undo Feature Removal Scope

Status: active

## Why this is pinned

The old undo/redo/history feature (RQMD-UNDO-*, RQMD-TIME-*) was fully deprecated and its requirements archived to `docs/requirements/archived/`. The **code** is still live and deeply integrated. This pin documents the exact removal scope so `/tech-debt-sweep` can plan the cleanup without re-discovering everything.

## Removal inventory

### Source files

| File | Lines | What to remove |
|---|---|---|
| `src/rqmd/history.py` | 975 | **Entire file.** HistoryManager, retention policies, git-backed snapshot system. |
| `src/rqmd/cli.py` | ~15 refs | Import of `HistoryManager`/`merge_retention_policies`, `_resolve_effective_retention_policy()`, snapshot materialization, historical diff rendering. |
| `src/rqmd/workflows.py` | ~40 refs | History browser UI (`_show_history_browser`, `_build_history_browser_state`, `_prompt_for_history_entry_action`), undo/redo keybindings (z/y/h), branch checkout/label/discard/cherry-pick/replay/gc flows. |
| `src/rqmd/status_update.py` | ~8 refs | History snapshot capture on status changes (`history_manager.capture()`). |

### Test files

| File | What to remove |
|---|---|
| `tests/test_interactive.py` | ~10 test functions: `test_RQMD_interactive_021c` (history shortcuts), `test_RQMD_interactive_021d` (history browser), `021d2` (branch checkout), `021e` (cherry-pick), `021f` (replay), `021g` (gc), `021g2` (label before gc), `021h` (immediate prune), plus ~10 `StubHistoryManager` classes. |
| `tests/test_core_engine.py` | `test_RQMD_core_037_history_flags_removed_in_simplification_mode` — tests that `--history`/`--undo` CLI flags are absent. Can be removed once the code is gone. |

### Danger zones

- **`status_update.py` captures history on every status change.** Removing HistoryManager without updating `apply_status_changes()` will crash interactive mode. The capture calls need to be deleted, not just the import.
- **`workflows.py` undo/redo keybindings** are wired into the interactive requirement menu. The `z`/`y`/`h` keys and their help text need to be removed from `extra_keys` and `extra_keys_help` dicts.
- **Do NOT confuse with `rqmd --staleness` (CORE-045).** The new staleness feature uses `git blame`/`git log` on *requirement files* — it does NOT use HistoryManager's git-backed snapshot repo at all. No code from `history.py` should be reused.

## Guidance

- Difficulty: **surgical** — 5 files, ~130 reference sites, test coverage changes
- Approach: delete `history.py` first, then fix imports/references file-by-file, then delete orphaned tests
- Run full test suite (`uv run --extra dev pytest -q`) after each file is cleaned — don't batch
- The `# keep(reason)` annotation is NOT applicable here — nothing should be kept

## Links

- Archived requirements: `docs/requirements/archived/undo.md`, `docs/requirements/archived/time-machine.md`
- Related inbox item: `docs/inbox.md` — `[tech-debt]` entry
- Related requirements: RQMD-EXT-079 (`/tech-debt-sweep`), RQMD-CORE-045 (`--staleness`)

## Update notes

- 2026-04-16: Created during archival of RQMD-UNDO-* and RQMD-TIME-* requirements.
