# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Added a project changelog following the Keep a Changelog format.
- Added README-index portability tests for automatic requirements discovery.
- Added deep scratch pagination corpus pages through page 23 for e2e coverage.
- Added first-class `--json` output for non-interactive summary/check/set/filter workflows to support machine-readable automation and AI triage.
- Added `schema_version` to JSON payload contracts across `rqmd` and `rqmd-ai`, with coverage tests for both CLIs.
- Added shell-completion activation and troubleshooting guidance for zsh, bash, and fish in README.
- Added requirement-level tests for status value-prefix resolution and ambiguous option-prefix candidate reporting.
- Added `rqmd-ai --install-agent-bundle` with minimal/full presets, dry-run preview, idempotent reruns, and optional overwrite behavior for existing instruction files.
- Added unknown-status compatibility tests and machine-readable JSON error payload coverage.

### Changed

- Switched requirements index layout from sibling requirements.md files to in-directory README.md files.
- Updated rqmd auto-detection to use docs/requirements/README.md and requirements/README.md.
- Updated scaffold generation to create README.md inside the requirements directory.
- Updated portability, core-engine, and README documentation to match the new requirements index contract.
- Updated bootstrap/index messaging with branded RDD tagline and direct GitHub/PyPI links.
- Updated README and requirements index status workflow documentation to the new ordered status catalog.
- Updated requirement statuses to mark `RQMD-CORE-017` and `RQMD-PACKAGING-010` as Implemented.
- Updated requirement status to mark `RQMD-AI-012` as Implemented.
- Updated requirement status to mark `RQMD-PORTABILITY-017` as Implemented.

## [0.1.0] - 2026-03-26

### Added

- Initial rqmd package release with interactive and automation-friendly requirements status workflows.