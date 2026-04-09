"""Tests for RQMD-PACKAGING-014: rqmd-ai query flags folded into the rqmd CLI."""

from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from rqmd import cli


def _setup_repo(tmp_path: Path) -> Path:
    """Create a minimal repo with a domain file containing mixed requirements."""
    repo = tmp_path / "repo"
    domain_dir = repo / "docs" / "requirements"
    domain_dir.mkdir(parents=True)
    (domain_dir / "README.md").write_text("# Index\n- [demo](demo.md)\n")
    (domain_dir / "demo.md").write_text(
        """\
# Demo Domain

### RQMD-DEMO-001: Feature alpha
- **Status:** 💡 Proposed
- **Priority:** 🟠 P1 - High

### RQMD-DEMO-002: Bug beta
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- **Type:** bug
- **Affects:** RQMD-DEMO-001

### RQMD-DEMO-003: Implemented gamma
- **Status:** 🔧 Implemented
- **Priority:** 🟢 P3 - Low
""",
        encoding="utf-8",
    )
    return repo


_BASE_ARGS = ["--project-root", "{repo}", "--docs-dir", "docs/requirements", "--id-namespace", "RQMD"]


def _invoke(repo: Path, *extra_args: str) -> CliRunner.Result:  # type: ignore[name-defined]
    runner = CliRunner()
    args = [a.format(repo=str(repo)) for a in _BASE_ARGS] + list(extra_args)
    return runner.invoke(cli.main, args, catch_exceptions=False)


# --- dump-status tests ---


def test_dump_status_proposed_returns_matching_requirements(tmp_path: Path) -> None:
    repo = _setup_repo(tmp_path)
    result = _invoke(repo, "--dump-status", "proposed")
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["mode"] == "export-context"
    assert payload["read_only"] is True
    assert payload["total"] == 2
    ids = [r["id"] for f in payload["files"] for r in f["requirements"]]
    assert "RQMD-DEMO-001" in ids
    assert "RQMD-DEMO-002" in ids
    assert "RQMD-DEMO-003" not in ids


def test_dump_status_implemented_returns_matching(tmp_path: Path) -> None:
    repo = _setup_repo(tmp_path)
    result = _invoke(repo, "--dump-status", "implemented")
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["total"] == 1
    reqs = payload["files"][0]["requirements"]
    assert reqs[0]["id"] == "RQMD-DEMO-003"


# --- dump-type tests ---


def test_dump_type_bug_returns_only_bugs(tmp_path: Path) -> None:
    repo = _setup_repo(tmp_path)
    result = _invoke(repo, "--dump-type", "bug")
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["total"] == 1
    reqs = payload["files"][0]["requirements"]
    assert reqs[0]["id"] == "RQMD-DEMO-002"
    assert reqs[0]["type"] == "bug"
    assert reqs[0]["affects"] == "RQMD-DEMO-001"


def test_dump_type_feature_returns_features_including_implicit(tmp_path: Path) -> None:
    repo = _setup_repo(tmp_path)
    result = _invoke(repo, "--dump-type", "feature")
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["total"] == 2
    ids = [r["id"] for f in payload["files"] for r in f["requirements"]]
    assert "RQMD-DEMO-001" in ids
    assert "RQMD-DEMO-003" in ids


def test_dump_type_composable_with_status(tmp_path: Path) -> None:
    """--dump-type bug --dump-status proposed should compose."""
    repo = _setup_repo(tmp_path)
    result = _invoke(repo, "--dump-type", "bug", "--dump-status", "proposed")
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["total"] == 1
    reqs = payload["files"][0]["requirements"]
    assert reqs[0]["id"] == "RQMD-DEMO-002"


# --- dump-id tests ---


def test_dump_id_returns_specific_requirement(tmp_path: Path) -> None:
    repo = _setup_repo(tmp_path)
    result = _invoke(repo, "--dump-id", "RQMD-DEMO-002")
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["total"] == 1
    reqs = payload["files"][0]["requirements"]
    assert reqs[0]["id"] == "RQMD-DEMO-002"
    assert reqs[0]["title"] == "Bug beta"


def test_dump_id_includes_body_by_default(tmp_path: Path) -> None:
    repo = _setup_repo(tmp_path)
    result = _invoke(repo, "--dump-id", "RQMD-DEMO-001")
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    reqs = payload["files"][0]["requirements"]
    assert "body" in reqs[0]
    assert "Feature alpha" in reqs[0]["body"]["markdown"]


def test_dump_id_no_body_excludes_body(tmp_path: Path) -> None:
    repo = _setup_repo(tmp_path)
    result = _invoke(repo, "--dump-id", "RQMD-DEMO-001", "--no-requirement-body")
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    reqs = payload["files"][0]["requirements"]
    assert "body" not in reqs[0]


def test_dump_id_multiple(tmp_path: Path) -> None:
    repo = _setup_repo(tmp_path)
    result = _invoke(repo, "--dump-id", "RQMD-DEMO-001", "--dump-id", "RQMD-DEMO-003")
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["total"] == 2


# --- dump-file tests ---


def test_dump_file_filters_by_domain(tmp_path: Path) -> None:
    repo = _setup_repo(tmp_path)
    # Add a second domain file
    domain_dir = repo / "docs" / "requirements"
    (domain_dir / "README.md").write_text(
        "# Index\n- [demo](demo.md)\n- [extra](extra.md)\n"
    )
    (domain_dir / "extra.md").write_text(
        """\
# Extra
### RQMD-EXTRA-001: Extra req
- **Status:** 💡 Proposed
""",
        encoding="utf-8",
    )
    result = _invoke(repo, "--dump-file", "docs/requirements/extra.md")
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["total"] == 1
    assert payload["files"][0]["requirements"][0]["id"] == "RQMD-EXTRA-001"


# --- next_id in export ---


def test_dump_status_includes_next_id(tmp_path: Path) -> None:
    repo = _setup_repo(tmp_path)
    result = _invoke(repo, "--dump-status", "proposed", "--no-requirement-body")
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert "next_id" in payload["files"][0]


# --- schema_version ---


def test_dump_output_includes_schema_version(tmp_path: Path) -> None:
    repo = _setup_repo(tmp_path)
    result = _invoke(repo, "--dump-status", "proposed", "--no-requirement-body")
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert "schema_version" in payload


# --- dump flags imply --json (no noise) ---


def test_dump_flags_suppress_auto_discovery_messages(tmp_path: Path) -> None:
    """Dump flags should produce clean JSON without auto-discovery noise on stdout."""
    repo = _setup_repo(tmp_path)
    result = _invoke(repo, "--dump-status", "proposed", "--no-requirement-body")
    assert result.exit_code == 0
    # The entire stdout should be valid JSON
    payload = json.loads(result.output)
    assert isinstance(payload, dict)


# --- --write + --update tests ---


def test_write_update_plan_mode(tmp_path: Path) -> None:
    """--write --update --dry-run should produce a plan (mode=plan, read_only=true)."""
    repo = _setup_repo(tmp_path)
    result = _invoke(
        repo, "--json", "--update", "RQMD-DEMO-001=implemented", "--write", "--dry-run"
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["mode"] == "plan"
    assert payload["read_only"] is True
    assert payload["update_count"] == 1
    assert payload["updates"][0]["id"] == "RQMD-DEMO-001"
    assert payload["updates"][0]["status"] == "🔧 Implemented"
    assert payload["updates"][0]["changed"] is False


def test_write_update_apply_mode(tmp_path: Path) -> None:
    """--write --update (no --dry-run) should apply changes (mode=apply)."""
    repo = _setup_repo(tmp_path)
    result = _invoke(
        repo, "--json", "--update", "RQMD-DEMO-001=implemented", "--write"
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["mode"] == "apply"
    assert payload["read_only"] is False
    assert payload["changed_count"] == 1

    # Verify the file was actually changed
    domain = repo / "docs" / "requirements" / "demo.md"
    text = domain.read_text(encoding="utf-8")
    assert "🔧 Implemented" in text


def test_write_without_update_raises_error(tmp_path: Path) -> None:
    """--write without --update should error."""
    repo = _setup_repo(tmp_path)
    result = _invoke(repo, "--json", "--write")
    assert result.exit_code != 0
    assert "--write requires" in result.output


# --- --batch tests ---


def test_batch_mode_multiple_queries(tmp_path: Path) -> None:
    repo = _setup_repo(tmp_path)
    queries = json.dumps([
        {"query": "dump-id", "ids": ["RQMD-DEMO-001"]},
        {"query": "dump-status", "status": "implemented"},
    ])
    runner = CliRunner()
    args = [
        "--project-root", str(repo),
        "--docs-dir", "docs/requirements",
        "--id-namespace", "RQMD",
        "--batch",
        "--no-requirement-body",
    ]
    result = runner.invoke(cli.main, args, input=queries, catch_exceptions=False)
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["mode"] == "batch"
    assert payload["total_queries"] == 2
    assert len(payload["results"]) == 2

    # First result: dump-id should find RQMD-DEMO-001
    r1 = payload["results"][0]["result"]
    assert r1["total"] == 1

    # Second result: dump-status implemented should find RQMD-DEMO-003
    r2 = payload["results"][1]["result"]
    assert r2["total"] == 1


def test_batch_mode_dump_type_query(tmp_path: Path) -> None:
    repo = _setup_repo(tmp_path)
    queries = json.dumps([
        {"query": "dump-type", "type": "bug"},
    ])
    runner = CliRunner()
    args = [
        "--project-root", str(repo),
        "--docs-dir", "docs/requirements",
        "--id-namespace", "RQMD",
        "--batch",
        "--no-requirement-body",
    ]
    result = runner.invoke(cli.main, args, input=queries, catch_exceptions=False)
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["results"][0]["result"]["total"] == 1


# --- include-domain-markdown tests ---


def test_include_domain_markdown_adds_body(tmp_path: Path) -> None:
    repo = _setup_repo(tmp_path)
    result = _invoke(
        repo,
        "--dump-status", "proposed",
        "--include-domain-markdown",
        "--no-requirement-body",
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    file_entry = payload["files"][0]
    assert "domain_body" in file_entry
