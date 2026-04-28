"""Tests for rqmd.staleness module (RQMD-CORE-045)."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from rqmd.staleness import (DEFAULT_WEIGHTS, build_staleness_report,
                            compute_staleness, format_deprecated_report,
                            format_explain_text, format_staleness_table,
                            grep_xrefs, staleness_flags)

# ---------------------------------------------------------------------------
# Unit tests for scoring functions
# ---------------------------------------------------------------------------


class TestComputeStaleness:
    def test_default_weights_sum_to_one(self) -> None:
        total = sum(DEFAULT_WEIGHTS.values())
        assert abs(total - 1.0) < 1e-9

    def test_zero_inputs(self) -> None:
        score, breakdown = compute_staleness(0, 10, 0, "✅ Verified")
        # status_age=0, xref=0(10refs), freshness=0, but flag=50 → 50*0.2=10
        assert score == 10.0

    def test_high_staleness(self) -> None:
        score, _breakdown = compute_staleness(
            status_age_days=400,
            xref_count=0,
            code_freshness_days=400,
            status="🗑️ Deprecated",
        )
        # All signals near 100, but xref_count=0 for deprecated → status_flag ≠ 95
        # Actually: deprecated + 0 refs means no "deprecated-but-alive" flag → flag_score=50
        assert score > 70

    def test_deprecated_but_alive_boost(self) -> None:
        score, _breakdown = compute_staleness(
            status_age_days=365,
            xref_count=5,
            code_freshness_days=365,
            status="🗑️ Deprecated",
        )
        # deprecated + refs → status_flag_score=95
        assert score > 60

    def test_implemented_but_unreferenced(self) -> None:
        score, _breakdown = compute_staleness(
            status_age_days=180,
            xref_count=0,
            code_freshness_days=None,
            status="🔧 Implemented",
        )
        # xref_count=0 → 100, code_freshness=None → 80, implemented+0refs → 80
        assert score > 50

    def test_custom_weights(self) -> None:
        custom = {"status_age_weight": 1.0, "xref_count_weight": 0.0,
                  "code_freshness_weight": 0.0, "status_flag_weight": 0.0}
        score, _ = compute_staleness(365, 0, 0, "💡 Proposed", weights=custom)
        assert score == 100.0

    def test_score_clamped(self) -> None:
        score, _ = compute_staleness(9999, 0, 9999, "🗑️ Deprecated")
        assert score <= 100.0


class TestStalenessFlags:
    def test_deprecated_but_alive(self) -> None:
        flags = staleness_flags("🗑️ Deprecated", xref_count=3)
        assert "deprecated-but-alive" in flags

    def test_implemented_but_unreferenced(self) -> None:
        flags = staleness_flags("🔧 Implemented", xref_count=0)
        assert "implemented-but-unreferenced" in flags

    def test_no_flags_for_verified_with_refs(self) -> None:
        flags = staleness_flags("✅ Verified", xref_count=5)
        assert flags == []

    def test_none_status(self) -> None:
        flags = staleness_flags(None, xref_count=0)
        assert flags == []


# ---------------------------------------------------------------------------
# Format tests
# ---------------------------------------------------------------------------


class TestFormatExplainText:
    def test_contains_weights(self) -> None:
        text = format_explain_text()
        assert "status_age_weight" in text
        assert "xref_count_weight" in text
        assert "0.30" in text

    def test_custom_weights(self) -> None:
        text = format_explain_text({"status_age_weight": 0.5})
        assert "0.50" in text


class TestFormatStalenessTable:
    def test_empty(self) -> None:
        assert "No requirements matched" in format_staleness_table([])

    def test_one_row(self) -> None:
        rows = [{
            "id": "REQ-001",
            "title": "Test",
            "status": "🔧 Implemented",
            "staleness_score": 42.5,
            "status_age_days": 100,
            "xref_count": 3,
            "code_freshness_days": 50,
            "flags": [],
        }]
        text = format_staleness_table(rows)
        assert "REQ-001" in text
        assert "42.5" in text


class TestFormatDeprecatedReport:
    def test_empty(self) -> None:
        text = format_deprecated_report([], Path("/repo"))
        assert "No deprecated" in text

    def test_one_row(self) -> None:
        rows = [{
            "id": "REQ-002",
            "status": "🗑️ Deprecated",
            "xrefs": [{"path": "src/main.py", "line": 10, "content": "# REQ-002"}],
        }]
        text = format_deprecated_report(rows, Path("/repo"))
        assert "REQ-002" in text
        assert "src/main.py" in text


# ---------------------------------------------------------------------------
# Integration tests with a real git repo
# ---------------------------------------------------------------------------


def _init_git_repo(repo: Path) -> None:
    """Create a minimal git repo with an initial commit."""
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


@pytest.fixture
def git_repo_with_reqs(tmp_path: Path) -> Path:
    """Create a git repo with domain files and source code referencing a requirement."""
    repo = tmp_path / "repo"
    domain_dir = repo / "docs" / "requirements"
    domain_dir.mkdir(parents=True)

    domain_text = """\
# Test Domain

Scope: test requirements.

### TST-001: Verified requirement
- **Status:** ✅ Verified

### TST-002: Deprecated requirement
- **Status:** 🗑️ Deprecated

### TST-003: Implemented requirement
- **Status:** 🔧 Implemented
"""
    (domain_dir / "test-domain.md").write_text(domain_text, encoding="utf-8")

    # Source file referencing TST-001 and TST-002
    src_dir = repo / "src"
    src_dir.mkdir()
    (src_dir / "main.py").write_text(
        "# TST-001: referenced here\n# TST-002: also referenced\n",
        encoding="utf-8",
    )

    _init_git_repo(repo)
    _git_add_commit(repo, "initial commit")
    return repo


class TestBuildStalenessReport:
    def test_basic_report(self, git_repo_with_reqs: Path) -> None:
        domain_dir = git_repo_with_reqs / "docs" / "requirements"
        domain_files = sorted(domain_dir.glob("*.md"))
        rows = build_staleness_report(
            git_repo_with_reqs,
            domain_files,
            id_prefixes=("TST",),
        )
        assert len(rows) == 3
        ids = [r["id"] for r in rows]
        assert "TST-001" in ids
        assert "TST-002" in ids
        assert "TST-003" in ids
        # Sorted descending by score
        scores = [r["staleness_score"] for r in rows]
        assert scores == sorted(scores, reverse=True)

    def test_deprecated_only(self, git_repo_with_reqs: Path) -> None:
        domain_dir = git_repo_with_reqs / "docs" / "requirements"
        domain_files = sorted(domain_dir.glob("*.md"))
        rows = build_staleness_report(
            git_repo_with_reqs,
            domain_files,
            id_prefixes=("TST",),
            deprecated_only=True,
        )
        # TST-002 is deprecated with xrefs in src/main.py
        assert len(rows) == 1
        assert rows[0]["id"] == "TST-002"
        assert rows[0].get("xrefs")
        assert rows[0]["flags"] == ["deprecated-but-alive"]

    def test_xref_count(self, git_repo_with_reqs: Path) -> None:
        domain_dir = git_repo_with_reqs / "docs" / "requirements"
        domain_files = sorted(domain_dir.glob("*.md"))
        rows = build_staleness_report(
            git_repo_with_reqs,
            domain_files,
            id_prefixes=("TST",),
        )
        row_map = {r["id"]: r for r in rows}
        # TST-001 and TST-002 have xrefs in src/main.py (1 each, after filtering out docs/requirements)
        assert row_map["TST-001"]["xref_count"] >= 1
        assert row_map["TST-002"]["xref_count"] >= 1
        # TST-003 has no xrefs
        assert row_map["TST-003"]["xref_count"] == 0

    def test_implemented_unreferenced_flag(self, git_repo_with_reqs: Path) -> None:
        domain_dir = git_repo_with_reqs / "docs" / "requirements"
        domain_files = sorted(domain_dir.glob("*.md"))
        rows = build_staleness_report(
            git_repo_with_reqs,
            domain_files,
            id_prefixes=("TST",),
        )
        row_map = {r["id"]: r for r in rows}
        assert "implemented-but-unreferenced" in row_map["TST-003"]["flags"]

    def test_not_git_repo(self, tmp_path: Path) -> None:
        domain_dir = tmp_path / "docs" / "requirements"
        domain_dir.mkdir(parents=True)
        (domain_dir / "test.md").write_text(
            "# T\n\n### REQ-001: X\n- **Status:** 💡 Proposed\n",
            encoding="utf-8",
        )
        with pytest.raises(RuntimeError, match="git repository"):
            build_staleness_report(
                tmp_path,
                [domain_dir / "test.md"],
                id_prefixes=("REQ",),
            )


class TestGrepXrefs:
    def test_finds_references(self, git_repo_with_reqs: Path) -> None:
        xrefs = grep_xrefs("TST-001", git_repo_with_reqs)
        # Should find in src/main.py AND docs/requirements/test-domain.md
        paths = [x["path"] for x in xrefs]
        assert any("src/main.py" in p for p in paths)

    def test_no_matches(self, git_repo_with_reqs: Path) -> None:
        xrefs = grep_xrefs("NONEXIST-999", git_repo_with_reqs)
        assert xrefs == []
