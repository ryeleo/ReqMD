# Requirements

This document is the source-of-truth index for reqmd requirements.

## How To Use

- Keep requirement IDs stable and unique.
- Keep one status line directly below each requirement heading.
- Use Given/When/Then when a requirement needs explicit acceptance detail.
- Simple one-line requirements with only a title and status are also valid.
- Keep domain docs under docs/acceptance-criteria/.

Status workflow:
- 💡 Proposed -> 🔧 Implemented -> 💻 Desktop-Verified -> 🎮 VR-Verified -> ✅ Done
- Use ⛔ Blocked or 🗑️ Deprecated when needed.

## Domain Documents

### AC CLI
- [Core Engine](docs/acceptance-criteria/core-engine.md) - parsing, normalization, summaries, criteria extraction
- [Interactive UX](docs/acceptance-criteria/interactive-ux.md) - keyboard-driven status update flows
- [Automation API](docs/acceptance-criteria/automation-api.md) - non-interactive set/set-file/filter behavior
- [Portability](docs/acceptance-criteria/portability.md) - repo root, criteria directory, cross-project assumptions
- [Packaging](docs/acceptance-criteria/packaging.md) - package layout, entrypoints, install/run behavior

## Verification

- [Testing](docs/testing.md) - pytest suite coverage map for implemented requirements

## ID Prefixes

| Prefix | Domain |
|---|---|
| REQMD-CORE-* | Core Engine |
| REQMD-INTERACTIVE-* | Interactive UX |
| REQMD-AUTOMATION-* | Automation API |
| REQMD-PORTABILITY-* | Portability |
| REQMD-PACKAGING-* | Packaging |

## Tracking Rule

- Run reqmd --check to validate summaries.
- Run reqmd to update summaries and optionally edit requirement statuses interactively.
- Use --id-prefix to limit or expand which header prefixes are recognized. Default: AC and R.
