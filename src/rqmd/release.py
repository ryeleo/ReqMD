"""Release readiness checks for rqmd-managed projects.

Implements RQMD-CORE-052: `rqmd release --preflight` — machine-readable
release readiness check (wired as `--release-preflight` until the CLI
gains a subcommand architecture).
"""

from __future__ import annotations

import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Well-known version-source file patterns (Phase 1 of RQMD-CORE-054)
# ---------------------------------------------------------------------------

_WELL_KNOWN_FILES: list[dict[str, Any]] = [
    {
        "glob": "pyproject.toml",
        "pattern": re.compile(r'^version\s*=\s*"([^"]+)"', re.MULTILINE),
    },
    {
        "glob": "package.json",
        "pattern": re.compile(r'"version"\s*:\s*"([^"]+)"'),
    },
    {
        "glob": "Cargo.toml",
        "pattern": re.compile(r'^version\s*=\s*"([^"]+)"', re.MULTILINE),
    },
    {
        "glob": "setup.cfg",
        "pattern": re.compile(r'^version\s*=\s*(.+)$', re.MULTILINE),
    },
    {
        "glob": "version.txt",
        "pattern": re.compile(r'^(\S+)'),
    },
]

# ---------------------------------------------------------------------------
# Version extraction
# ---------------------------------------------------------------------------


def _extract_version_from_file(
    path: Path, pattern: re.Pattern[str]
) -> str | None:
    """Extract version string from a file using the given regex."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    m = pattern.search(text)
    return m.group(1).strip() if m else None


def discover_version_sources(
    repo_root: Path,
    configured_sources: list[dict[str, str]] | None = None,
) -> list[dict[str, Any]]:
    """Discover version-source files and extract their version strings.

    If *configured_sources* is provided (from rqmd.yml ``version_sources``),
    those are used.  Otherwise falls back to well-known file scanning.

    Returns a list of dicts: ``{"file": <relative>, "version": <str|None>, "source": "config"|"well-known"}``.
    """
    sources: list[dict[str, Any]] = []

    if configured_sources:
        for entry in configured_sources:
            rel_path = entry.get("file", "")
            full_path = repo_root / rel_path
            version: str | None = None
            if full_path.is_file():
                # Try well-known patterns first, fall back to generic version line
                for wk in _WELL_KNOWN_FILES:
                    if full_path.name == wk["glob"]:
                        version = _extract_version_from_file(full_path, wk["pattern"])
                        break
                if version is None:
                    # Generic: try common patterns
                    for wk in _WELL_KNOWN_FILES:
                        v = _extract_version_from_file(full_path, wk["pattern"])
                        if v:
                            version = v
                            break
            sources.append({
                "file": rel_path,
                "version": version,
                "source": "config",
                "exists": full_path.is_file(),
            })
        return sources

    # Phase 1: scan well-known files
    for wk in _WELL_KNOWN_FILES:
        candidate = repo_root / wk["glob"]
        if candidate.is_file():
            version = _extract_version_from_file(candidate, wk["pattern"])
            if version is not None:
                sources.append({
                    "file": wk["glob"],
                    "version": version,
                    "source": "well-known",
                    "exists": True,
                })
    return sources


# ---------------------------------------------------------------------------
# CHANGELOG check
# ---------------------------------------------------------------------------

_CHANGELOG_HEADER_RE = re.compile(
    r'^##\s+\[(\d+\.\d+\.\d+(?:[a-zA-Z0-9._+-]*)?)\]', re.MULTILINE
)


def check_changelog_stamp(
    repo_root: Path,
    expected_version: str,
    changelog_name: str = "CHANGELOG.md",
) -> dict[str, Any]:
    """Check that CHANGELOG.md has a ``## [x.y.z]`` header matching *expected_version*.

    Returns a check-result dict with ``ok``, ``message``, and ``details``.
    """
    changelog_path = repo_root / changelog_name
    if not changelog_path.is_file():
        return {
            "check": "changelog_stamp",
            "ok": False,
            "message": f"{changelog_name} not found",
            "details": {"path": changelog_name},
        }

    text = changelog_path.read_text(encoding="utf-8")
    found_versions: list[str] = _CHANGELOG_HEADER_RE.findall(text)

    if expected_version in found_versions:
        return {
            "check": "changelog_stamp",
            "ok": True,
            "message": f"CHANGELOG contains [{ expected_version}] entry",
            "details": {"path": changelog_name, "version": expected_version},
        }

    return {
        "check": "changelog_stamp",
        "ok": False,
        "message": f"CHANGELOG missing [{ expected_version}] entry",
        "details": {
            "path": changelog_name,
            "expected": expected_version,
            "found_versions": found_versions[:5],
        },
    }


# ---------------------------------------------------------------------------
# Version agreement check
# ---------------------------------------------------------------------------


def check_version_agreement(
    sources: list[dict[str, Any]],
) -> dict[str, Any]:
    """Check that all discovered version-source files contain the same version string.

    Returns a check-result dict.
    """
    if not sources:
        return {
            "check": "version_agreement",
            "ok": False,
            "message": "No version-source files found",
            "details": {"sources": []},
        }

    versions = {s["version"] for s in sources if s.get("version")}
    missing = [s for s in sources if not s.get("version")]
    source_details = [
        {"file": s["file"], "version": s.get("version"), "source": s.get("source")}
        for s in sources
    ]

    if len(versions) == 1 and not missing:
        return {
            "check": "version_agreement",
            "ok": True,
            "message": f"All {len(sources)} version source(s) agree: {versions.pop()}",
            "details": {"sources": source_details},
        }

    if len(versions) > 1:
        return {
            "check": "version_agreement",
            "ok": False,
            "message": f"Version mismatch across sources: {', '.join(sorted(versions))}",
            "details": {"sources": source_details, "distinct_versions": sorted(versions)},
        }

    if missing:
        return {
            "check": "version_agreement",
            "ok": False,
            "message": f"{len(missing)} source(s) could not be read or have no version",
            "details": {"sources": source_details},
        }

    # Should not reach here, but handle gracefully
    return {
        "check": "version_agreement",
        "ok": True,
        "message": "Version sources checked",
        "details": {"sources": source_details},
    }


# ---------------------------------------------------------------------------
# Git working tree check
# ---------------------------------------------------------------------------


def _run_git(args: list[str], cwd: Path) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.stdout if result.returncode == 0 else ""
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return ""


def check_clean_working_tree(repo_root: Path) -> dict[str, Any]:
    """Check whether the git working tree is clean.

    Returns a check-result dict.
    """
    status_output = _run_git(["status", "--porcelain"], repo_root)

    if status_output == "":
        # Could be clean OR not a git repo — verify
        is_git = _run_git(["rev-parse", "--is-inside-work-tree"], repo_root).strip()
        if is_git != "true":
            return {
                "check": "clean_working_tree",
                "ok": False,
                "message": "Not a git repository",
                "details": {},
            }
        return {
            "check": "clean_working_tree",
            "ok": True,
            "message": "Working tree is clean",
            "details": {},
        }

    dirty_files = [
        line.strip() for line in status_output.splitlines() if line.strip()
    ]
    return {
        "check": "clean_working_tree",
        "ok": False,
        "message": f"{len(dirty_files)} uncommitted change(s)",
        "details": {"dirty_file_count": len(dirty_files), "dirty_files": dirty_files[:20]},
    }


# ---------------------------------------------------------------------------
# Preflight orchestrator
# ---------------------------------------------------------------------------


def run_preflight(
    repo_root: Path,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run all release preflight checks and return a structured result.

    Returns::

        {
            "mode": "release-preflight",
            "ok": True/False,
            "version": "<detected>",
            "checks": [ ... per-check dicts ... ]
        }
    """
    config = config or {}
    configured_sources = config.get("version_sources")
    if configured_sources is not None and not isinstance(configured_sources, list):
        configured_sources = None

    sources = discover_version_sources(repo_root, configured_sources)

    # Determine the authoritative version from the first source
    detected_version: str | None = None
    for s in sources:
        if s.get("version"):
            detected_version = s["version"]
            break

    checks: list[dict[str, Any]] = []

    # 1. Version agreement
    checks.append(check_version_agreement(sources))

    # 2. CHANGELOG stamp (only if we have a version to check)
    if detected_version:
        checks.append(check_changelog_stamp(repo_root, detected_version))
    else:
        checks.append({
            "check": "changelog_stamp",
            "ok": False,
            "message": "No version detected — cannot verify CHANGELOG",
            "details": {},
        })

    # 3. Clean working tree
    checks.append(check_clean_working_tree(repo_root))

    overall_ok = all(c["ok"] for c in checks)

    return {
        "mode": "release-preflight",
        "ok": overall_ok,
        "version": detected_version,
        "checks": checks,
    }


# ---------------------------------------------------------------------------
# Human-readable output
# ---------------------------------------------------------------------------


def format_preflight_table(result: dict[str, Any]) -> str:
    """Format preflight result as a human-readable summary."""
    lines: list[str] = []
    version = result.get("version") or "unknown"
    overall = "PASS" if result["ok"] else "FAIL"
    lines.append(f"Release preflight ({version}): {overall}")
    lines.append("-" * 50)

    for check in result.get("checks", []):
        icon = "✓" if check["ok"] else "✗"
        lines.append(f"  {icon} {check['check']}: {check['message']}")

        # Show dirty files if present
        details = check.get("details", {})
        if not check["ok"] and "dirty_files" in details:
            for f in details["dirty_files"][:10]:
                lines.append(f"      {f}")
            if details.get("dirty_file_count", 0) > 10:
                lines.append(f"      ... and {details['dirty_file_count'] - 10} more")

        # Show version source details on mismatch
        if not check["ok"] and "sources" in details:
            for src in details["sources"]:
                lines.append(f"      {src['file']}: {src.get('version', '—')}")

    return "\n".join(lines)
