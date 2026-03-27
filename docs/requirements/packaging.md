# Packaging Requirements

Scope: package layout, installability, module entrypoints, and publication readiness.

<!-- acceptance-status-summary:start -->
Summary: 0💡 0🔧 9✅ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->

### RQMD-PACKAGING-001: src-layout package structure
- **Status:** ✅ Verified
- Given the package source tree
- When inspected
- Then Python package code lives under `src/rqmd`
- And project metadata is defined in `pyproject.toml`.

### RQMD-PACKAGING-002: Console entrypoint
- **Status:** ✅ Verified
- Given package is installed
- When user runs `rqmd`
- Then command invokes package main CLI handler
- And matches module behavior.

### RQMD-PACKAGING-003: Module entrypoint
- **Status:** ✅ Verified
- Given package source is available
- When user runs `python -m rqmd`
- Then CLI starts successfully
- And exposes same command options as console script.

### RQMD-PACKAGING-004: Runtime dependencies declared
- **Status:** ✅ Verified
- Given project metadata in pyproject
- When package is installed
- Then required dependencies include click and tabulate
- And missing dependency crashes are avoided at runtime.

### RQMD-PACKAGING-005: Readme-backed usage docs
- **Status:** ✅ Verified
- Given package folder is copied to a new project
- When user reads README
- Then install and command examples are present
- And portability plus ID-prefix flags are documented.

### RQMD-PACKAGING-006: PyPI metadata hardening
- **Status:** ✅ Verified
- Given package is prepared for public release
- When metadata is finalized
- Then author/license/classifiers/urls are complete
- And build+upload instructions remain valid.

### RQMD-PACKAGING-007: Semantic versioning policy
- **Status:** ✅ Verified
- Given package evolves across projects
- When versions are tagged
- Then backward-compatible changes use minor/patch bumps
- And breaking CLI changes trigger major version bumps.

### RQMD-PACKAGING-008: Publish to PyPI on GitHub release
- **Status:** ✅ Verified
- Given a GitHub release is created for this repository
- When the release workflow runs
- Then the tagged package version is published to pypi.org automatically
- And publication uses repository automation rather than a manual local upload.

### RQMD-PACKAGING-009: Keep a Changelog maintained
- **Status:** ✅ Verified
- Given contributors ship notable changes
- When release and pre-release updates are prepared
- Then repository contains a root-level `CHANGELOG.md` following Keep a Changelog structure
- And updates are recorded under an `Unreleased` section before version cut.
