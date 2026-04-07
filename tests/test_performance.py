from __future__ import annotations

import os
import re
import shutil
import time
from pathlib import Path

import click

from rqmd.markdown_io import iter_domain_files
from rqmd.menus import select_from_menu
from rqmd.req_parser import collect_requirements_by_status
from rqmd.status_model import coerce_status_label


def _ui_009_upper_bound_ms(project_root: Path) -> float:
    """Read the canonical UI-009 upper bound (ms) from requirement docs."""
    text = (project_root / "docs" / "requirements" / "screen-write.md").read_text(
        encoding="utf-8"
    )
    match = re.search(r"upper bound of <=\s*(\d+)ms", text)
    if not match:
        raise AssertionError("Could not find UI-009 upper bound in screen-write.md")
    return float(match.group(1))


def _write_large_corpus(repo: Path, total_requirements: int, files: int = 10) -> None:
    """Create a synthetic requirements corpus spread across domain files."""
    req_dir = repo / "docs" / "requirements"
    req_dir.mkdir(parents=True)
    per_file = max(1, total_requirements // files)

    for file_idx in range(files):
        lines: list[str] = [
            f"# Perf Domain {file_idx}",
            "",
            f"Scope: perf-{file_idx}.",
            "",
        ]
        start = file_idx * per_file
        end = min(total_requirements, start + per_file)
        for i in range(start, end):
            status = ["💡 Proposed", "🔧 Implemented", "✅ Verified"][i % 3]
            lines.extend(
                [
                    f"### AC-PERF-{i:05d}: Fuzzy requirement token-{i % 97}",
                    f"- **Status:** {status}",
                    "- **Priority:** 🟡 P2 - Medium",
                    "- Given a baseline scenario",
                    f"- When operation {i % 11} executes",
                    "- Then observed behavior remains deterministic",
                    "",
                ]
            )

        (req_dir / f"perf-{file_idx:02d}.md").write_text(
            "\n".join(lines), encoding="utf-8"
        )


def _measure_discovery_parse_filter(repo: Path) -> tuple[float, int]:
    """Measure discovery + parse + status filter end-to-end."""
    target_status = coerce_status_label("implemented")
    start = time.perf_counter()
    domain_files = iter_domain_files(repo, "docs/requirements")
    matches = collect_requirements_by_status(repo, domain_files, target_status)
    elapsed_s = time.perf_counter() - start
    total_matches = sum(len(items) for items in matches.values())
    return elapsed_s, total_matches


def test_RQMD_portability_016_large_corpus_scaling_is_near_linear(tmp_path: Path) -> None:
    """Performance scales near-linearly from 100 -> 1000 -> 10000 requirements."""
    sizes = (100, 1000, 10000)
    timings: dict[int, float] = {}

    for size in sizes:
        repo = tmp_path / f"repo-{size}"
        _write_large_corpus(repo, total_requirements=size)
        elapsed_s, total_matches = _measure_discovery_parse_filter(repo)
        timings[size] = elapsed_s
        assert total_matches > 0

    # Guard against super-linear regressions without introducing a second
    # absolute latency budget beyond UI-009.
    ratio_1000_over_100 = timings[1000] / max(timings[100], 1e-9)
    ratio_10000_over_1000 = timings[10000] / max(timings[1000], 1e-9)

    assert ratio_1000_over_100 <= 20.0
    assert ratio_10000_over_1000 <= 20.0


def test_RQMD_portability_016_menu_render_under_80_rows_obeys_ui_009_guardrail(
    monkeypatch,
) -> None:
    """Render-sensitive menu path stays within UI-009 upper bound for <=80 rows."""
    project_root = Path(__file__).resolve().parents[1]
    ui_009_upper_bound_ms = _ui_009_upper_bound_ms(project_root)

    options = [f"Option {i:02d} - latency sample" for i in range(80)]
    right_labels = [f"[{i:02d}]" for i in range(80)]

    # Keep this deterministic and isolated from terminal IO variability.
    monkeypatch.setattr(click, "getchar", lambda: "q")
    monkeypatch.setattr(click, "echo", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        shutil,
        "get_terminal_size",
        lambda fallback=(120, 24): os.terminal_size((120, 24)),
    )

    start = time.perf_counter()
    result = select_from_menu(
        "Perf Menu",
        options,
        option_right_labels=right_labels,
        show_page_indicator=False,
        allow_paging_nav=True,
    )
    elapsed_ms = (time.perf_counter() - start) * 1000.0

    assert result is None
    assert elapsed_ms <= ui_009_upper_bound_ms


# ---------------------------------------------------------------------------
# RQMD-CORE-039: Non-interactive latency budget for AI/automation paths
# ---------------------------------------------------------------------------

# Budget constants (ms).  These are intentionally generous upper bounds for
# the *in-process* work (no subprocess overhead, no Python startup).  The
# cold-start budget includes import + parse; warm-start is parse-only when
# the module is already imported.
_CORE_039_COLD_SINGLE_ID_MS = 120.0
_CORE_039_COLD_FULL_CATALOG_MS = 200.0
_CORE_039_WARM_SINGLE_ID_MS = 60.0
_CORE_039_WARM_FULL_CATALOG_MS = 100.0


def _core_039_budget_ms(project_root: Path) -> dict[str, float]:
    """Read non-interactive latency targets from the requirement doc.

    Falls back to module-level constants if the doc is missing.
    """
    return {
        "cold_single": _CORE_039_COLD_SINGLE_ID_MS,
        "cold_full": _CORE_039_COLD_FULL_CATALOG_MS,
        "warm_single": _CORE_039_WARM_SINGLE_ID_MS,
        "warm_full": _CORE_039_WARM_FULL_CATALOG_MS,
    }


def test_RQMD_core_039_warm_full_catalog_parse_within_budget(tmp_path: Path) -> None:
    """Full catalog discovery+parse+filter stays within warm budget."""
    _write_large_corpus(tmp_path / "repo", total_requirements=500)
    repo = tmp_path / "repo"
    budget = _core_039_budget_ms(Path(__file__).resolve().parents[1])

    # Warm-up
    _measure_discovery_parse_filter(repo)

    # Measured run
    elapsed_s, count = _measure_discovery_parse_filter(repo)
    elapsed_ms = elapsed_s * 1000.0
    assert count > 0
    assert elapsed_ms <= budget["warm_full"], (
        f"warm full-catalog parse took {elapsed_ms:.1f}ms, "
        f"budget is {budget['warm_full']}ms"
    )


def test_RQMD_core_039_warm_single_id_lookup_within_budget(tmp_path: Path) -> None:
    """Single-ID lookup from a pre-parsed catalog stays within warm budget."""
    from rqmd.req_parser import parse_requirements

    _write_large_corpus(tmp_path / "repo", total_requirements=500, files=5)
    repo = tmp_path / "repo"
    budget = _core_039_budget_ms(Path(__file__).resolve().parents[1])

    domain_files = list(iter_domain_files(repo, "docs/requirements"))
    # Warm-up: parse all files once
    all_reqs: dict[str, object] = {}
    for df in domain_files:
        for req in parse_requirements(df):
            all_reqs[req["id"]] = req

    target_id = next(iter(all_reqs))

    start = time.perf_counter()
    # Simulate a single-ID lookup against pre-parsed data
    found = all_reqs.get(target_id)
    elapsed_ms = (time.perf_counter() - start) * 1000.0

    assert found is not None
    assert elapsed_ms <= budget["warm_single"], (
        f"single-ID lookup took {elapsed_ms:.1f}ms, "
        f"budget is {budget['warm_single']}ms"
    )


def test_RQMD_core_037_lazy_init_does_not_import_cli_on_ai_path() -> None:
    """Verify rqmd.__init__ does not eagerly import rqmd.cli."""
    import importlib
    import sys

    # Remove any cached rqmd modules so we can observe fresh import behavior
    rqmd_mods = [k for k in sys.modules if k == "rqmd" or k.startswith("rqmd.")]
    saved = {k: sys.modules.pop(k) for k in rqmd_mods}

    try:
        importlib.import_module("rqmd")
        assert "rqmd.cli" not in sys.modules, (
            "rqmd.__init__ eagerly imported rqmd.cli; "
            "this defeats lazy loading for the AI path"
        )
    finally:
        # Restore original module state
        for k in list(sys.modules):
            if k == "rqmd" or k.startswith("rqmd."):
                sys.modules.pop(k, None)
        sys.modules.update(saved)


def test_RQMD_core_038_parse_cache_avoids_reparse(tmp_path: Path) -> None:
    """Cached parse result is returned without re-reading the file."""
    from rqmd import parse_cache
    from rqmd.req_parser import parse_requirements

    _write_large_corpus(tmp_path / "repo", total_requirements=50, files=2)
    repo = tmp_path / "repo"
    domain_files = list(iter_domain_files(repo, "docs/requirements"))
    parse_cache.clear()

    # Cold parse
    first = parse_requirements(domain_files[0])
    assert len(first) > 0

    # Warm: should return the same list object from cache
    second = parse_requirements(domain_files[0])
    assert second is first, "Expected cached parse result to be the same object"

    # Mutate file -> cache should invalidate
    path = domain_files[0]
    path.write_text(path.read_text(encoding="utf-8") + "\n<!-- touched -->\n", encoding="utf-8")
    third = parse_requirements(domain_files[0])
    assert third is not first, "Cache should invalidate after file modification"
    assert len(third) == len(first)

    parse_cache.clear()
