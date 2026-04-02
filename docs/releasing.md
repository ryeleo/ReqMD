# Releasing rqmd

This repository publishes rqmd to PyPI through GitHub Actions trusted publishing.

## Pre-release checklist

Before cutting a stable release or release candidate:

1. Ensure `project.version` in `pyproject.toml` matches the version you intend to ship.
2. Move the relevant items from `CHANGELOG.md` `Unreleased` into a versioned release section if you are cutting a formal release note.
3. Run the repository smoke path and targeted tests:
   - `bash scripts/local-smoke.sh`
   - `uv run --extra dev pytest`
4. Confirm the package metadata still points at the intended public URLs and package name.
5. Confirm the GitHub repository `pypi` environment is configured for PyPI trusted publishing for the `rqmd` project.

## Release steps

1. Choose a tag that matches `project.version`, such as `v0.1.0` for a stable release or `v0.1.0rc1` for a release candidate.
2. Ensure that tag exactly matches `project.version` after removing the optional leading `v`.
3. Push the release commit and create a GitHub Release with that tag.
4. Publish the GitHub Release.
5. Wait for `.github/workflows/publish-pypi.yml` to finish successfully.
6. Verify the new version appears on PyPI and that `pip install rqmd==<version>` succeeds.

## Notes

- The publish workflow accepts stable releases and PEP 440 `rc` prereleases such as `0.1.0rc1`.
- The publish workflow rejects tags that do not match `project.version` in `pyproject.toml`.
- Publication uses GitHub Actions trusted publishing via the `pypi` environment instead of a repository-stored `PYPI_API_TOKEN`.