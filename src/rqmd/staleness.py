"""Per-requirement staleness scoring based on git history and code cross-references.

Implements RQMD-CORE-045: `rqmd --staleness` — composite staleness report
driven by git blame, grep cross-refs, and configurable signal weights.
"""

from __future__ import annotations

import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

from .constants import DEFAULT_ID_PREFIXES
from .markdown_io import format_path_display
from .req_parser import parse_requirements

# ---------------------------------------------------------------------------
# Default signal weights (overridable via config [staleness] section)
# ---------------------------------------------------------------------------

DEFAULT_WEIGHTS: dict[str, float] = {
    "status_age_weight": 0.3,
    "xref_count_weight": 0.3,
    "code_freshness_weight": 0.2,
    "status_flag_weight": 0.2,
}


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

_BLAME_DATE_RE = re.compile(
    r"^[0-9a-f]+\s.*?\s(\d{4}-\d{2}-\d{2})\s", re.MULTILINE
)


def _run_git(args: list[str], cwd: Path) -> str:
    """Run a git command and return stdout (empty string on failure)."""
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.stdout if result.returncode == 0 else ""
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return ""


def _is_git_repo(repo_root: Path) -> bool:
    return bool(_run_git(["rev-parse", "--is-inside-work-tree"], repo_root).strip())


def git_blame_line_date(path: Path, line_number: int, repo_root: Path) -> str | None:
    """Return the ISO date (YYYY-MM-DD) of the last commit that touched *line_number* in *path*."""
    out = _run_git(
        ["blame", "-p", "-L", f"{line_number},{line_number}", "--", str(path)],
        repo_root,
    )
    for raw_line in out.splitlines():
        if raw_line.startswith("committer-time "):
            ts = int(raw_line.split()[1])
            return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
    return None


def _days_since(date_str: str | None) -> int | None:
    """Return number of days between *date_str* (YYYY-MM-DD) and today (UTC)."""
    if not date_str:
        return None
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        return (datetime.now(tz=timezone.utc) - dt).days
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Cross-reference helpers
# ---------------------------------------------------------------------------

_BINARY_EXTENSIONS = frozenset({
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".webp",
    ".pdf", ".zip", ".gz", ".tar", ".whl", ".egg", ".so", ".dylib",
    ".dll", ".exe", ".pyc", ".pyo", ".class", ".o", ".a",
})


def grep_xrefs(
    requirement_id: str,
    repo_root: Path,
) -> list[dict[str, str | int]]:
    """Find source files referencing *requirement_id* via git grep.

    Returns list of dicts with keys: path, line, content.
    Skips the requirements directory itself.
    """
    out = _run_git(["grep", "-n", "--fixed-strings", requirement_id], repo_root)
    if not out:
        return []

    matches: list[dict[str, str | int]] = []
    for raw_line in out.splitlines():
        # Format: <path>:<lineno>:<content>
        parts = raw_line.split(":", 2)
        if len(parts) < 3:
            continue
        file_path = parts[0]
        try:
            line_no = int(parts[1])
        except ValueError:
            continue
        content = parts[2]

        # Skip binary extensions
        if Path(file_path).suffix.lower() in _BINARY_EXTENSIONS:
            continue

        matches.append({"path": file_path, "line": line_no, "content": content.strip()})
    return matches


def _latest_commit_date_for_files(
    file_paths: Sequence[str],
    repo_root: Path,
) -> str | None:
    """Return the most recent commit date (YYYY-MM-DD) touching any of *file_paths*."""
    if not file_paths:
        return None
    out = _run_git(
        ["log", "-1", "--format=%aI", "--"] + list(file_paths),
        repo_root,
    )
    date_part = out.strip()[:10] if out.strip() else None
    return date_part


# ---------------------------------------------------------------------------
# Staleness computation
# ---------------------------------------------------------------------------


def _clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, value))


def _age_score(days: int | None, max_days: int = 365) -> float:
    """Map age in days to 0-100.  0 days → 0, ≥max_days → 100."""
    if days is None:
        return 50.0  # unknown → mid-range
    return _clamp(days / max_days * 100)


def _xref_inverse_score(xref_count: int) -> float:
    """More cross-refs → lower staleness.  0 refs → 100, ≥10 → 0."""
    if xref_count >= 10:
        return 0.0
    return _clamp((10 - xref_count) / 10 * 100)


def _freshness_score(days: int | None, max_days: int = 365) -> float:
    """Map code freshness age to 0-100.  Recently touched → 0, old → 100."""
    if days is None:
        return 80.0  # no referencing code → fairly stale
    return _clamp(days / max_days * 100)


def _status_flag_score(status: str | None, xref_count: int) -> float:
    """Semantic boosting based on status + cross-ref combination."""
    if status is None:
        return 50.0
    status_lower = status.lower()
    # Deprecated but still referenced in code → near-100
    if "deprecated" in status_lower and xref_count > 0:
        return 95.0
    # Implemented but unreferenced → possible orphan
    if "implemented" in status_lower and xref_count == 0:
        return 80.0
    # Verified with no refs → probably fine
    if "verified" in status_lower and xref_count == 0:
        return 30.0
    # Proposed → neutral
    if "proposed" in status_lower:
        return 40.0
    return 50.0


def compute_staleness(
    status_age_days: int | None,
    xref_count: int,
    code_freshness_days: int | None,
    status: str | None,
    weights: dict[str, float] | None = None,
) -> tuple[float, dict[str, float]]:
    """Compute composite staleness score.

    Returns (composite_score, signal_breakdown) where signal_breakdown
    maps signal names to their weighted contribution.
    """
    w = {**DEFAULT_WEIGHTS, **(weights or {})}

    signals = {
        "status_age": _age_score(status_age_days),
        "xref_count": _xref_inverse_score(xref_count),
        "code_freshness": _freshness_score(code_freshness_days),
        "status_flag": _status_flag_score(status, xref_count),
    }

    composite = (
        signals["status_age"] * w["status_age_weight"]
        + signals["xref_count"] * w["xref_count_weight"]
        + signals["code_freshness"] * w["code_freshness_weight"]
        + signals["status_flag"] * w["status_flag_weight"]
    )

    breakdown = {
        "status_age": round(signals["status_age"] * w["status_age_weight"], 1),
        "xref_count": round(signals["xref_count"] * w["xref_count_weight"], 1),
        "code_freshness": round(signals["code_freshness"] * w["code_freshness_weight"], 1),
        "status_flag": round(signals["status_flag"] * w["status_flag_weight"], 1),
    }

    return round(_clamp(composite), 1), breakdown


# ---------------------------------------------------------------------------
# Staleness flags / annotations
# ---------------------------------------------------------------------------


def staleness_flags(status: str | None, xref_count: int) -> list[str]:
    """Return semantic flag labels for the requirement."""
    flags: list[str] = []
    if status is None:
        return flags
    status_lower = status.lower()
    if "deprecated" in status_lower and xref_count > 0:
        flags.append("deprecated-but-alive")
    if "implemented" in status_lower and xref_count == 0:
        flags.append("implemented-but-unreferenced")
    return flags


# ---------------------------------------------------------------------------
# High-level report builder
# ---------------------------------------------------------------------------


def build_staleness_report(
    repo_root: Path,
    domain_files: list[Path],
    id_prefixes: tuple[str, ...] = DEFAULT_ID_PREFIXES,
    weights: dict[str, float] | None = None,
    deprecated_only: bool = False,
    requirements_dir: str | None = None,
) -> list[dict[str, object]]:
    """Build a staleness report for all requirements across *domain_files*.

    Returns a list of dicts sorted by staleness score descending.
    """
    if not _is_git_repo(repo_root):
        raise RuntimeError("staleness scoring requires a git repository")

    rows: list[dict[str, object]] = []

    for path in domain_files:
        reqs = parse_requirements(path, id_prefixes=id_prefixes)
        for req in reqs:
            req_id = str(req["id"])
            status = str(req["status"]) if req.get("status") else None
            title = str(req.get("title", ""))

            # Skip requirements dir files from xref search
            xrefs_raw = grep_xrefs(req_id, repo_root)
            # Filter out matches within the requirements directory itself.
            # git grep returns repo-relative paths, so normalize req_dir
            # to a relative POSIX prefix.
            raw_req_dir = requirements_dir or "docs/requirements"
            try:
                req_dir_prefix = Path(raw_req_dir).relative_to(repo_root).as_posix()
            except ValueError:
                req_dir_prefix = raw_req_dir
            xrefs = [
                m for m in xrefs_raw
                if not str(m["path"]).startswith(req_dir_prefix)
            ]

            if deprecated_only:
                if not (status and "deprecated" in status.lower() and len(xrefs) > 0):
                    continue

            # Status age from git blame
            status_line = req.get("status_line")
            status_date: str | None = None
            if status_line is not None:
                # status_line is 0-indexed, git blame is 1-indexed
                status_date = git_blame_line_date(
                    path, int(status_line) + 1, repo_root
                )
            status_age_days = _days_since(status_date)

            # Code freshness — most recent commit touching referencing files
            ref_files = list({str(m["path"]) for m in xrefs})
            code_freshness_date = _latest_commit_date_for_files(ref_files, repo_root)
            code_freshness_days = _days_since(code_freshness_date)

            score, breakdown = compute_staleness(
                status_age_days, len(xrefs), code_freshness_days, status, weights
            )
            flags = staleness_flags(status, len(xrefs))

            row: dict[str, object] = {
                "id": req_id,
                "title": title,
                "status": status,
                "file": format_path_display(path, repo_root),
                "last_status_change": status_date,
                "status_age_days": status_age_days,
                "xref_count": len(xrefs),
                "code_freshness": code_freshness_date,
                "code_freshness_days": code_freshness_days,
                "staleness_score": score,
                "breakdown": breakdown,
                "flags": flags,
            }

            if deprecated_only:
                row["xrefs"] = xrefs

            rows.append(row)

    rows.sort(key=lambda r: float(r["staleness_score"]), reverse=True)  # type: ignore[arg-type]
    return rows


# ---------------------------------------------------------------------------
# Explain output
# ---------------------------------------------------------------------------


def format_explain_text(weights: dict[str, float] | None = None) -> str:
    """Return human-readable description of staleness scoring signals and weights."""
    w = {**DEFAULT_WEIGHTS, **(weights or {})}
    lines = [
        "Staleness scoring — signal weights and descriptions",
        "=" * 55,
        "",
        f"  status_age_weight    = {w['status_age_weight']:.2f}",
        "    Days since the status line was last changed (git blame).",
        "    0 days → score 0, ≥365 days → score 100.",
        "",
        f"  xref_count_weight    = {w['xref_count_weight']:.2f}",
        "    Inverse of code cross-reference count (git grep).",
        "    ≥10 refs → score 0, 0 refs → score 100.",
        "",
        f"  code_freshness_weight = {w['code_freshness_weight']:.2f}",
        "    Days since the most recent commit touching referencing files.",
        "    0 days → score 0, ≥365 days → score 100.",
        "",
        f"  status_flag_weight   = {w['status_flag_weight']:.2f}",
        "    Semantic boost based on status + cross-ref combination:",
        '    - "deprecated-but-alive" (deprecated + refs > 0) → 95',
        '    - "implemented-but-unreferenced" (implemented + 0 refs) → 80',
        "    - verified + 0 refs → 30, proposed → 40, other → 50",
        "",
        "Composite = Σ(signal_score × weight), clamped to [0, 100].",
        "Higher score = more stale / more likely tech debt.",
        "",
        "Override weights in rqmd.yml under a [staleness] section:",
        "  staleness:",
        "    status_age_weight: 0.4",
        "    xref_count_weight: 0.2",
        "    code_freshness_weight: 0.2",
        "    status_flag_weight: 0.2",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Table formatting (human-readable output)
# ---------------------------------------------------------------------------


def format_staleness_table(rows: list[dict[str, object]]) -> str:
    """Format staleness report as a human-readable table."""
    if not rows:
        return "No requirements matched."

    lines: list[str] = []
    # Header
    lines.append(
        f"{'Score':>5}  {'ID':<20} {'Status':<22} {'Age':>5} {'Refs':>4} {'Fresh':>5}  {'Flags'}"
    )
    lines.append("-" * 90)

    for row in rows:
        score = row["staleness_score"]
        req_id = str(row["id"])[:20]
        status = str(row["status"] or "—")[:22]
        age = str(row["status_age_days"]) if row["status_age_days"] is not None else "—"
        refs = str(row["xref_count"])
        fresh = str(row["code_freshness_days"]) if row["code_freshness_days"] is not None else "—"
        flags_list = row.get("flags", [])
        flags_str = ", ".join(flags_list) if isinstance(flags_list, list) and flags_list else ""

        lines.append(
            f"{score:>5}  {req_id:<20} {status:<22} {age:>5} {refs:>4} {fresh:>5}  {flags_str}"
        )

    return "\n".join(lines)


def format_deprecated_report(rows: list[dict[str, object]], repo_root: Path) -> str:
    """Format deprecated-only report grouped by requirement ID."""
    if not rows:
        return "No deprecated requirements with live code cross-refs found."

    lines: list[str] = []
    for row in rows:
        req_id = str(row["id"])
        status = str(row["status"] or "—")
        xrefs = row.get("xrefs", [])
        xref_count = len(xrefs) if isinstance(xrefs, list) else 0
        lines.append(f"{req_id}: {status} — {xref_count} live cross-ref(s)")
        if isinstance(xrefs, list):
            for xref in xrefs:
                lines.append(f"  {xref['path']}:{xref['line']}: {xref['content']}")
        lines.append("")

    return "\n".join(lines)
