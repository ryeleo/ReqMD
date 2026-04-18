---
name: release
description: Repository-specific release workflow — validates, tags, and publishes paired GitHub Releases for rqmd-cli and rqmd-vscode.
argument-hint: Provide the version to release (e.g. 0.2.5). Omit to get the release checklist only.
user-invocable: true
metadata:
  guide:
    summary: Stamp changelogs, validate, commit and push, then tag and create paired GitHub Releases.
    workflow:
      - Stamp [Unreleased] → [x.y.z] - YYYY-MM-DD in both CHANGELOGs and commit before tagging.
      - Confirm version strings match across pyproject.toml and rqmd-vscode/package.json.
      - Bump prompt description versions with rqmd-vscode/scripts/bump-prompt-versions.sh.
      - Run `bash ./agent-workflow.sh validate --profile quick` to confirm green state.
      - Commit all changes, tag both repos, then push.
      - Create paired GitHub Releases with `./scripts/gh-release-both.sh <version>`.
    examples:
      - Release 0.2.5: stamp changelogs, confirm versions, run quick validate, commit+push both repos, tag v0.2.5 in both, run gh-release-both.sh 0.2.5
---

Use this skill when it is time to cut a release. Both rqmd-cli and rqmd-vscode must be committed, pushed, and tagged before creating GitHub Releases.

> **🚨 Warning:** The tag must land on the commit that contains the stamped CHANGELOG entry. Always tag after committing the stamped changelog — never tag a commit that doesn't include it.

## Step 1 — Stamp CHANGELOGs

In **both** repos, rename `[Unreleased]` to `[x.y.z] - YYYY-MM-DD`:

```md
## [0.2.9] - 2026-04-16   ← was [Unreleased]
```

`scripts/ensure_release_tag.py` (run by CI) will hard-fail if `## [x.y.z]` is absent. Stamping must happen in the same commit that gets tagged.

## Step 2 — Confirm version strings

- `pyproject.toml` `version = "x.y.z"` (rqmd-cli)
- `package.json` `"version": "x.y.z"` (rqmd-vscode)

## Step 3 — Bump prompt description versions

```bash
bash rqmd-vscode/scripts/bump-prompt-versions.sh <version>
```

## Step 4 — Validate

```bash
bash ./agent-workflow.sh validate --profile quick
```

## Step 5 — Commit, tag, and push both repos

```bash
# rqmd-cli
cd rqmd-cli && git add -A && git commit -m "release: x.y.z"
git tag v<version>
git push && git push --tags

# rqmd-vscode
cd rqmd-vscode && git add -A && git commit -m "release: x.y.z"
git tag v<version>
git push && git push --tags
```

Confirm `git status` is clean and `git log --oneline -1` shows the release commit at HEAD in both repos.

## Step 6 — Create GitHub Releases

```bash
./scripts/gh-release-both.sh <version>
```

Creates paired releases on `ryeleo/rqmd` and `ryeleo/rqmd-vscode` with links to the canonical CHANGELOG entries. Requires `gh` CLI authenticated (`gh auth login`).

## Step 7 — Playtest (dogfood)

After the release is live, install from local source and verify the new version works end-to-end:

```bash
./scripts/playtest.sh
```

Confirm `rqmd --version` reports the released version.

## Notes

- Paired release contract: rqmd-cli and rqmd-vscode share a version number and are always released together. Never tag one without the other.
- Pre-1.0.0 policy: agent may cut a release autonomously when validation is green and the CHANGELOG is ready. Keep `gh-release-both.sh` usable without manual intervention.
- Keep `./scripts/gh-release-both.sh` as the single canonical release command — do not use `gh release create` directly.
