---
name: release
description: Repository-specific release workflow — validates, tags, and publishes paired GitHub Releases for rqmd-cli and rqmd-vscode.
argument-hint: Provide the version to release (e.g. 0.2.5). Omit to get the release checklist only.
user-invocable: true
metadata:
  guide:
    summary: Run full validation, push tags, then create paired GitHub Releases using the canonical release script.
    workflow:
      - Confirm version strings match across pyproject.toml, rqmd-vscode/package.json, and both CHANGELOG [Unreleased] → [x.y.z] entries before starting.
      - Run `bash ./agent-workflow.sh validate --profile quick` to confirm clean green state.
      - Commit any final changes, then push and tag both repos.
      - Create paired GitHub Releases with `./scripts/gh-release-both.sh <version>`.
    examples:
      - Release 0.2.5: confirm versions, run quick validate, push tags in both repos, run gh-release-both.sh 0.2.5
---

Use this skill when it is time to cut a release. Both rqmd-cli and rqmd-vscode must be committed, pushed, and tagged before creating GitHub Releases.

## Preflight

1. Confirm version strings match:
   - `pyproject.toml` (rqmd-cli)
   - `package.json` (rqmd-vscode)
   - `CHANGELOG.md` — `[Unreleased]` renamed to `[x.y.z] - YYYY-MM-DD` in both repos
2. Bump prompt description versions in rqmd-vscode:
   ```
   bash rqmd-vscode/scripts/bump-prompt-versions.sh <version>
   ```
3. Run validation: `bash ./agent-workflow.sh validate --profile quick`
4. Confirm both repos are on `main` with a clean `git status`

## Tag and push

Run in **both** rqmd-cli and rqmd-vscode:

```
git push
git tag v<version>
git push --tags
```

## Create GitHub Releases

```
./scripts/gh-release-both.sh <version>
```

Creates paired releases on `ryeleo/rqmd` and `ryeleo/rqmd-vscode` with links to the canonical CHANGELOG entries. Requires `gh` CLI authenticated (`gh auth login`).

## Notes

- Paired release contract: rqmd-cli and rqmd-vscode share a version number and are always released together. Never tag one without the other.
- Pre-1.0.0 policy: agent may cut a release autonomously when validation is green and the CHANGELOG is ready. Keep `gh-release-both.sh` usable without manual intervention.
- Keep `./scripts/gh-release-both.sh` as the single canonical release command — do not use `gh release create` directly.
