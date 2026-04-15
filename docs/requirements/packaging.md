# Packaging Requirements

Scope: package layout, installability, module entrypoints, and publication readiness.

<!-- acceptance-status-summary:start -->
Summary: 0💡 5🔧 10✅ 0⚠️ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->


### RQMD-PACKAGING-001: src-layout package structure

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** To inspect it so that Python package code lives under `src/rqmd`.


### RQMD-PACKAGING-002: Console entrypoint

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** To run `rqmd` so that command invokes package main CLI handler.


### RQMD-PACKAGING-003: Module entrypoint

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** To run `python -m rqmd` so that CLI starts successfully.


### RQMD-PACKAGING-004: Runtime dependencies declared

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** To install the package so that required dependencies include click and tabulate.


### RQMD-PACKAGING-005: Readme-backed usage docs

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** To read README so that install and command examples are present.


### RQMD-PACKAGING-006: PyPI metadata hardening

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** To finalize metadata so that author/license/classifiers/urls are complete.


### RQMD-PACKAGING-007: Semantic versioning policy

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** To tag versions so that backward-compatible changes use minor/patch bumps.


### RQMD-PACKAGING-008: Publish to PyPI on stable release or rc tag

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** To run the release workflow so that the tagged package version is published to pypi.org automatically.


### RQMD-PACKAGING-009: Keep a Changelog maintained

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Summary:** To prepare release and pre-release updates so that repository contains a root-level `CHANGELOG.md` following Keep a Changelog structure.


### RQMD-PACKAGING-010: Shell completion distribution and activation guidance

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** Shell completion support to be available for zsh (and documented for bash/fish where supported) so that users can enable completion using standard shell-init patterns without hand-maintaining completion scripts.


### RQMD-PACKAGING-011: Shell completion for positional filter tokens

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** Completion candidates for status and priority filter values to appear alongside requirement IDs, domain identifiers, and subsection names so that workflows such as `rqmd Pro<TAB>` or `rqmd P1 core<TAB>` remain discoverable and fast without requiring me to remember whether a token is accepted positionally.


### RQMD-PACKAGING-012: Pre-release ReqMD rename and alias plan

- **Status:** 🔧 Implemented
- **Priority:** 🟢 P3 - Low
- **Summary:** Packaging and entrypoint behavior to support an explicit rename/alias plan so that the project can adopt `reqmd` branding or a dual-command transition without breaking existing installs, docs, or automation unexpectedly.


### RQMD-PACKAGING-014: Fold rqmd-ai query flags into rqmd CLI

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Summary:** The structured JSON export and query flags currently on `rqmd-ai` (e.g., `--json`, `--dump-status`, `--dump-type`, `--dump-id`, `--dump-file`, `--include-requirement-body`, `--include-domain-markdown`, batch mode) folded into the `rqmd` CLI itself so that querying requirements in JSON is just a standard `rqmd` feature, not something that requires a separate AI-specific entrypoint.
- Given a user who runs `rqmd --json --dump-status proposed`
- When the command executes
- Then the output is identical to what `rqmd-ai --json --dump-status proposed` produces today.
- And `rqmd --json` includes `next_id` per domain file, the same schema version, and all existing export fields.


### RQMD-PACKAGING-015: Deprecate and remove rqmd-ai CLI entrypoint

- **Status:** ✅ Verified
- **Priority:** 🟡 P2 - Medium
- **Blocked by:** RQMD-EXT-051
- As the rqmd maintainer after the VS Code extension ships and query flags are folded into `rqmd`
- **Summary:** To deprecate and eventually remove the `rqmd-ai` console-script entrypoint so that there is one CLI command (`rqmd`) and one IDE integration point (the VS Code extension), not a confusing split between `rqmd` and `rqmd-ai`.
- Given a user who runs `rqmd-ai --json`
- When the deprecation period is active
- Then the command still works but prints a stderr warning: "rqmd-ai is deprecated. Use `rqmd --json` instead."
- And after the removal version, the `rqmd-ai` entrypoint is no longer registered in the package.


### RQMD-PACKAGING-017: Register @rqmd chat participant for unified command surface

- **Status:** 🔧 Implemented
- **Priority:** 🟠 P1 - High
- **Blocked by:** RQMD-PACKAGING-013
- As a user invoking rqmd workflows in Copilot Chat
- **Summary:** `@rqmd` chat participant registered in the VS Code extension with subcommands `brainstorm`, `triage`, `go`, `next`, `refine`, `commit`, `verify`, `pin`, `feedback`, and `docs`. Each subcommand loads its skill or prompt file as system instructions and forwards the request to the Copilot-selected model. Users see `@rqmd` in autocomplete like `@terminal`.
- Given a user who types `@rqmd ` in Copilot Chat
- When autocomplete appears
- Then subcommands like `brainstorm`, `go`, `next`, `commit`, `refine` are shown.
- And invoking `@rqmd brainstorm` loads the `rqmd-brainstorm` skill internally and runs the workflow.


