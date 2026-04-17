"""Tests for rqmd.release module (RQMD-CORE-052)."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from rqmd.release import (
    check_changelog_stamp,
    check_clean_working_tree,
    check_version_agreement,
    discover_version_sources,
    format_preflight_table,
    run_preflight,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _init_git_repo(repo: Path) -> None:
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@test.com"],
        cwd=repo, check=True, capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=repo, check=True, capture_output=True,
    )


def _git_add_commit(repo: Path, message: str = "commit") -> None:
    subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", message, "--allow-empty"],
        cwd=repo, check=True, capture_output=True,
    )


# ---------------------------------------------------------------------------
# discover_version_sources
# ---------------------------------------------------------------------------


class TestDiscoverVersionSources:
    def test_discovers_pyproject_toml(self, tmp_path: Path) -> None:
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "test"\nversion = "1.2.3"\n'
        )
        sources = discover_version_sources(tmp_path)
        assert len(sources) == 1
        assert sources[0]["file"] == "pyproject.toml"
        assert sources[0]["version"] == "1.2.3"
        assert sources[0]["source"] == "well-known"

    def test_discovers_package_json(self, tmp_path: Path) -> None:
        (tmp_path / "package.json").write_text(
            '{"name": "test", "version": "2.0.0"}\n'
        )
        sources = discover_version_sources(tmp_path)
        assert len(sources) == 1
        assert sources[0]["version"] == "2.0.0"

    def test_discovers_multiple_files(self, tmp_path: Path) -> None:
        (tmp_path / "pyproject.toml").write_text('version = "1.0.0"\n')
        (tmp_path / "package.json").write_text('{"version": "1.0.0"}\n')
        sources = discover_version_sources(tmp_path)
        assert len(sources) == 2

    def test_empty_dir(self, tmp_path: Path) -> None:
        sources = discover_version_sources(tmp_path)
        assert sources == []

    def test_configured_sources(self, tmp_path: Path) -> None:
        (tmp_path / "pyproject.toml").write_text('version = "3.0.0"\n')
        configured = [{"file": "pyproject.toml"}]
        sources = discover_version_sources(tmp_path, configured)
        assert len(sources) == 1
        assert sources[0]["version"] == "3.0.0"
        assert sources[0]["source"] == "config"

    def test_configured_missing_file(self, tmp_path: Path) -> None:
        configured = [{"file": "nonexistent.toml"}]
        sources = discover_version_sources(tmp_path, configured)
        assert len(sources) == 1
        assert sources[0]["version"] is None
        assert sources[0]["exists"] is False


# ---------------------------------------------------------------------------
# check_changelog_stamp
# ---------------------------------------------------------------------------


class TestCheckChangelogStamp:
    def test_stamp_present(self, tmp_path: Path) -> None:
        (tmp_path / "CHANGELOG.md").write_text(
            "# Changelog\n\n## [Unreleased]\n\n## [1.2.3] - 2026-01-01\n\n### Added\n- stuff\n"
        )
        result = check_changelog_stamp(tmp_path, "1.2.3")
        assert result["ok"] is True
        assert "1.2.3" in result["message"]

    def test_stamp_missing(self, tmp_path: Path) -> None:
        (tmp_path / "CHANGELOG.md").write_text(
            "# Changelog\n\n## [Unreleased]\n\n## [1.0.0] - 2025-01-01\n"
        )
        result = check_changelog_stamp(tmp_path, "2.0.0")
        assert result["ok"] is False
        assert "missing" in result["message"].lower()

    def test_no_changelog(self, tmp_path: Path) -> None:
        result = check_changelog_stamp(tmp_path, "1.0.0")
        assert result["ok"] is False
        assert "not found" in result["message"].lower()


# ---------------------------------------------------------------------------
# check_version_agreement
# ---------------------------------------------------------------------------


class TestCheckVersionAgreement:
    def test_all_agree(self) -> None:
        sources = [
            {"file": "a.toml", "version": "1.0.0", "source": "well-known"},
            {"file": "b.json", "version": "1.0.0", "source": "well-known"},
        ]
        result = check_version_agreement(sources)
        assert result["ok"] is True

    def test_mismatch(self) -> None:
        sources = [
            {"file": "a.toml", "version": "1.0.0", "source": "well-known"},
            {"file": "b.json", "version": "2.0.0", "source": "well-known"},
        ]
        result = check_version_agreement(sources)
        assert result["ok"] is False
        assert "mismatch" in result["message"].lower()

    def test_no_sources(self) -> None:
        result = check_version_agreement([])
        assert result["ok"] is False

    def test_missing_version(self) -> None:
        sources = [
            {"file": "a.toml", "version": "1.0.0", "source": "well-known"},
            {"file": "b.json", "version": None, "source": "config"},
        ]
        result = check_version_agreement(sources)
        assert result["ok"] is False


# ---------------------------------------------------------------------------
# check_clean_working_tree
# ---------------------------------------------------------------------------


class TestCheckCleanWorkingTree:
    def test_clean_repo(self, tmp_path: Path) -> None:
        _init_git_repo(tmp_path)
        (tmp_path / "file.txt").write_text("hello")
        _git_add_commit(tmp_path, "init")
        result = check_clean_working_tree(tmp_path)
        assert result["ok"] is True

    def test_dirty_repo(self, tmp_path: Path) -> None:
        _init_git_repo(tmp_path)
        (tmp_path / "file.txt").write_text("hello")
        _git_add_commit(tmp_path, "init")
        (tmp_path / "file.txt").write_text("changed")
        result = check_clean_working_tree(tmp_path)
        assert result["ok"] is False
        assert result["details"]["dirty_file_count"] >= 1

    def test_not_git_repo(self, tmp_path: Path) -> None:
        result = check_clean_working_tree(tmp_path)
        assert result["ok"] is False
        assert "git" in result["message"].lower()


# ---------------------------------------------------------------------------
# run_preflight (integration)
# ---------------------------------------------------------------------------


class TestRunPreflight:
    def test_all_pass(self, tmp_path: Path) -> None:
        _init_git_repo(tmp_path)
        (tmp_path / "pyproject.toml").write_text('version = "1.0.0"\n')
        (tmp_path / "CHANGELOG.md").write_text(
            "# Changelog\n\n## [1.0.0] - 2026-01-01\n\n### Added\n- init\n"
        )
        _git_add_commit(tmp_path, "release 1.0.0")
        result = run_preflight(tmp_path)
        assert result["ok"] is True
        assert result["version"] == "1.0.0"
        assert len(result["checks"]) == 3

    def test_changelog_missing_stamp(self, tmp_path: Path) -> None:
        _init_git_repo(tmp_path)
        (tmp_path / "pyproject.toml").write_text('version = "2.0.0"\n')
        (tmp_path / "CHANGELOG.md").write_text("# Changelog\n\n## [Unreleased]\n")
        _git_add_commit(tmp_path, "init")
        result = run_preflight(tmp_path)
        assert result["ok"] is False
        # Version agreement passes, changelog fails
        checks_by_name = {c["check"]: c for c in result["checks"]}
        assert checks_by_name["version_agreement"]["ok"] is True
        assert checks_by_name["changelog_stamp"]["ok"] is False

    def test_dirty_tree_fails(self, tmp_path: Path) -> None:
        _init_git_repo(tmp_path)
        (tmp_path / "pyproject.toml").write_text('version = "1.0.0"\n')
        (tmp_path / "CHANGELOG.md").write_text("# Changelog\n\n## [1.0.0] - 2026-01-01\n")
        _git_add_commit(tmp_path, "init")
        (tmp_path / "dirty.txt").write_text("uncommitted")
        result = run_preflight(tmp_path)
        assert result["ok"] is False
        checks_by_name = {c["check"]: c for c in result["checks"]}
        assert checks_by_name["clean_working_tree"]["ok"] is False

    def test_no_version_sources(self, tmp_path: Path) -> None:
        _init_git_repo(tmp_path)
        _git_add_commit(tmp_path, "init")
        result = run_preflight(tmp_path)
        assert result["ok"] is False
        assert result["version"] is None

    def test_configured_version_sources(self, tmp_path: Path) -> None:
        _init_git_repo(tmp_path)
        (tmp_path / "pyproject.toml").write_text('version = "3.0.0"\n')
        (tmp_path / "CHANGELOG.md").write_text("# Changelog\n\n## [3.0.0] - 2026-01-01\n")
        _git_add_commit(tmp_path, "init")
        config = {"version_sources": [{"file": "pyproject.toml"}]}
        result = run_preflight(tmp_path, config)
        assert result["ok"] is True
        assert result["version"] == "3.0.0"


# ---------------------------------------------------------------------------
# format_preflight_table
# ---------------------------------------------------------------------------


class TestFormatPreflightTable:
    def test_pass_output(self) -> None:
        result = {
            "ok": True,
            "version": "1.0.0",
            "checks": [
                {"check": "version_agreement", "ok": True, "message": "All agree", "details": {}},
                {"check": "changelog_stamp", "ok": True, "message": "Present", "details": {}},
                {"check": "clean_working_tree", "ok": True, "message": "Clean", "details": {}},
            ],
        }
        text = format_preflight_table(result)
        assert "PASS" in text
        assert "1.0.0" in text

    def test_fail_output(self) -> None:
        result = {
            "ok": False,
            "version": "1.0.0",
            "checks": [
                {"check": "clean_working_tree", "ok": False, "message": "1 uncommitted change(s)",
                 "details": {"dirty_file_count": 1, "dirty_files": ["M foo.txt"]}},
            ],
        }
        text = format_preflight_table(result)
        assert "FAIL" in text
        assert "foo.txt" in text
