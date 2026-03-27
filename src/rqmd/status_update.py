from __future__ import annotations

import shutil
import sys
from pathlib import Path

try:
    import click
except ImportError:
    print("Error: 'click' package is required.", file=sys.stderr)
    print("Install with: pip3 install click", file=sys.stderr)
    sys.exit(1)

from .constants import DEFAULT_ID_PREFIXES
from .criteria_parser import extract_criterion_block, find_criterion_by_id
from .priority_model import coerce_priority_label
from .status_model import normalize_status_input
from .summary import process_file


def _rule_style_kwargs(status_label: str) -> dict:
    if status_label == "✅ Verified":
        return {"fg": "green"}
    if status_label == "💡 Proposed":
        return {"fg": "bright_blue"}
    if status_label in ("⛔ Blocked", "🗑️ Deprecated"):
        return {"dim": True}
    return {"fg": "yellow"}


def print_criterion_panel(
    path: Path,
    requirement: dict[str, object],
    repo_root: Path,
    id_prefixes: tuple[str, ...] = DEFAULT_ID_PREFIXES,
) -> None:
    criterion_id = str(requirement["id"])
    title = str(requirement["title"])
    status = str(requirement.get("status") or "")
    criterion_text = extract_criterion_block(path, criterion_id, id_prefixes=id_prefixes)
    term_width = shutil.get_terminal_size(fallback=(120, 24)).columns
    rule = "=" * max(24, min(term_width, 100))
    rule_kwargs = _rule_style_kwargs(status)

    click.echo("")
    click.echo(click.style(rule, **rule_kwargs))
    click.echo(click.style(f"{criterion_id}: {title}", bold=True))
    click.echo(click.style(f"Source: {path.relative_to(repo_root).as_posix()}", dim=True))
    click.echo(click.style(rule, **rule_kwargs))
    if criterion_text:
        click.echo(criterion_text)
    click.echo(click.style(rule, **rule_kwargs))


def update_criterion_status(
    path: Path,
    requirement: dict[str, object],
    new_status: str,
    blocked_reason: str | None = None,
    deprecated_reason: str | None = None,
    new_priority: str | None = None,
) -> bool:
    lines = path.read_text(encoding="utf-8").splitlines()
    status_line = requirement["status_line"]
    blocked_reason_line = requirement.get("blocked_reason_line")
    deprecated_reason_line = requirement.get("deprecated_reason_line")
    priority_line = requirement.get("priority_line")
    if not isinstance(status_line, int):
        raise ValueError("Invalid requirement status line.")

    new_status_line_text = f"- **Status:** {new_status}"
    status_changed = lines[status_line] != new_status_line_text

    if status_changed:
        lines[status_line] = new_status_line_text

    is_blocked = "Blocked" in new_status
    is_deprecated = "Deprecated" in new_status

    shift = 0

    if isinstance(blocked_reason_line, int):
        adj_blocked = blocked_reason_line + shift
        if is_blocked and blocked_reason:
            new_line = f"**Blocked:** {blocked_reason}"
            if lines[adj_blocked] != new_line:
                lines[adj_blocked] = new_line
                status_changed = True
        elif is_blocked:
            pass
        else:
            lines.pop(adj_blocked)
            shift -= 1
            status_changed = True
    elif is_blocked and blocked_reason:
        insert_at = status_line + 1 + shift
        lines.insert(insert_at, f"**Blocked:** {blocked_reason}")
        shift += 1
        status_changed = True

    if isinstance(deprecated_reason_line, int):
        adj_deprecated = deprecated_reason_line + shift
        if is_deprecated and deprecated_reason:
            new_line = f"**Deprecated:** {deprecated_reason}"
            if lines[adj_deprecated] != new_line:
                lines[adj_deprecated] = new_line
                status_changed = True
        elif is_deprecated:
            pass
        else:
            lines.pop(adj_deprecated)
            status_changed = True
    elif is_deprecated and deprecated_reason:
        insert_at = status_line + 1 + shift
        lines.insert(insert_at, f"**Deprecated:** {deprecated_reason}")
        status_changed = True

    # Handle priority updates
    if new_priority:
        if isinstance(priority_line, int):
            adj_priority = priority_line + shift
            new_priority_line_text = f"- **Priority:** {new_priority}"
            if lines[adj_priority] != new_priority_line_text:
                lines[adj_priority] = new_priority_line_text
                status_changed = True
        else:
            # Insert new priority line after status
            insert_at = status_line + 1 + shift
            new_priority_line_text = f"- **Priority:** {new_priority}"
            lines.insert(insert_at, new_priority_line_text)
            shift += 1
            status_changed = True

    if status_changed:
        path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    return status_changed


def prompt_for_blocked_reason() -> str:
    click.echo()
    click.echo("Provide a reason for blocking (or press Enter to skip):")
    reason = click.prompt("Reason", default="", show_default=False).strip()
    return reason


def prompt_for_deprecated_reason() -> str:
    click.echo()
    click.echo("Provide a reason for deprecating (or press Enter to skip):")
    reason = click.prompt("Reason", default="", show_default=False).strip()
    return reason


def prompt_for_priority() -> str:
    """Interactive priority selection menu."""
    from .constants import PRIORITY_ORDER
    
    click.echo()
    click.echo("Select a priority:")
    for i, (label, _) in enumerate(PRIORITY_ORDER, 1):
        click.echo(f"  {i}. {label}")
    
    choice = click.prompt("Priority choice (1-4, or press Enter to skip)", default="", show_default=False).strip()
    if not choice:
        return ""
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(PRIORITY_ORDER):
            return PRIORITY_ORDER[idx][0]
    except (ValueError, IndexError):
        pass
    
    click.echo("Invalid choice. Skipping priority update.")
    return ""


def apply_status_change_by_id(
    repo_root: Path,
    domain_files: list[Path],
    criterion_id: str,
    new_status_input: str | None,
    file_filter: str | None,
    blocked_reason: str | None = None,
    deprecated_reason: str | None = None,
    new_priority_input: str | None = None,
    include_status_emojis: bool = True,
    include_priority_summary: bool = False,
    id_prefixes: tuple[str, ...] = DEFAULT_ID_PREFIXES,
    emit_output: bool = True,
) -> bool:
    target_paths: list[Path]
    if file_filter:
        candidate = (repo_root / file_filter).resolve()
        if not candidate.exists() or not candidate.is_file():
            raise click.ClickException(f"--file path not found: {file_filter}")
        target_paths = [candidate]
    else:
        target_paths = domain_files

    matches: list[tuple[Path, dict[str, object]]] = []
    for path in target_paths:
        requirement = find_criterion_by_id(path, criterion_id, id_prefixes=id_prefixes)
        if requirement:
            matches.append((path, requirement))

    if not matches:
        if file_filter:
            raise click.ClickException(
                f"Requirement '{criterion_id}' not found in {file_filter}."
            )
        raise click.ClickException(f"Requirement '{criterion_id}' not found in the configured docs.")

    if len(matches) > 1 and not file_filter:
        locations = ", ".join(path.relative_to(repo_root).as_posix() for path, _ in matches)
        raise click.ClickException(
            f"Requirement '{criterion_id}' matched multiple files: {locations}. Use --file to disambiguate."
        )

    path, requirement = matches[0]

    if new_status_input is None and new_priority_input is None:
        raise click.ClickException("No update requested. Provide status and/or priority.")

    current_status = str(requirement.get("status") or "")
    new_status = current_status
    if new_status_input is not None:
        new_status = normalize_status_input(new_status_input)

    new_priority: str | None = None
    if new_priority_input is not None:
        normalized_priority = coerce_priority_label(new_priority_input)
        if normalized_priority == "unset":
            raise click.ClickException(f"Unrecognized priority input: {new_priority_input}")
        new_priority = normalized_priority

    changed = update_criterion_status(
        path,
        requirement,
        new_status,
        blocked_reason=blocked_reason,
        deprecated_reason=deprecated_reason,
        new_priority=new_priority,
    )
    process_file(
        path,
        check_only=False,
        include_status_emojis=include_status_emojis,
        include_priority_summary=include_priority_summary,
    )

    if emit_output:
        updates: list[str] = []
        if new_status_input is not None:
            updates.append(new_status)
        if new_priority is not None:
            updates.append(new_priority)
        update_summary = " | ".join(updates) if updates else "no-op"
        if changed:
            click.echo(f"Updated {requirement['id']} in {path.relative_to(repo_root).as_posix()} -> {update_summary}")
        else:
            click.echo(f"No change for {requirement['id']} in {path.relative_to(repo_root).as_posix()} ({update_summary})")
    return changed
