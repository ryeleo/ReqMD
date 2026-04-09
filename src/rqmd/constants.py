from __future__ import annotations

import re

from .default_catalogs import (load_default_priority_catalog_resource,
                               load_default_status_catalog_resource)

SUMMARY_START = "<!-- acceptance-status-summary:start -->"
SUMMARY_END = "<!-- acceptance-status-summary:end -->"
DEFAULT_ID_PREFIXES = ("AC", "R", "RQMD")
DEFAULT_REQUIREMENTS_DIR = "docs/requirements"
REQUIREMENTS_INDEX_NAME = "README.md"
JSON_SCHEMA_VERSION = "1.0.0"


def _catalog_entry_label(entry: dict[str, str]) -> str:
    return f"{entry['emoji']} {entry['name']}".strip()


def _normalize_catalog_entries(
    raw_entries: object,
    *,
    required_keys: tuple[str, ...],
    entry_kind: str,
) -> list[dict[str, str]]:
    if not isinstance(raw_entries, list) or not raw_entries:
        raise RuntimeError(
            f"Packaged default {entry_kind} catalog must be a non-empty list"
        )

    entries: list[dict[str, str]] = []
    for index, item in enumerate(raw_entries, start=1):
        if not isinstance(item, dict):
            raise RuntimeError(
                f"Packaged default {entry_kind} item #{index} must be a mapping"
            )
        normalized = {key: str(item.get(key, "")).strip() for key in required_keys}
        missing = [key for key, value in normalized.items() if not value]
        if missing:
            missing_display = ", ".join(missing)
            raise RuntimeError(
                f"Packaged default {entry_kind} item #{index} missing required keys: {missing_display}"
            )
        entries.append(normalized)
    return entries


_STATUS_DEFAULTS = load_default_status_catalog_resource()
DEFAULT_STATUS_CATALOG = _normalize_catalog_entries(
    _STATUS_DEFAULTS.get("statuses"),
    required_keys=("name", "shortcode", "emoji", "slug", "terse_header"),
    entry_kind="status",
)

_PRIORITY_DEFAULTS = load_default_priority_catalog_resource()
DEFAULT_PRIORITY_CATALOG = _normalize_catalog_entries(
    _PRIORITY_DEFAULTS.get("priorities"),
    required_keys=("name", "shortcode", "emoji", "slug"),
    entry_kind="priority",
)

STATUS_ORDER = [
    (_catalog_entry_label(entry), entry["slug"]) for entry in DEFAULT_STATUS_CATALOG
]
STATUS_TERSE_HEADERS_ASCII = [entry["terse_header"] for entry in DEFAULT_STATUS_CATALOG]
STATUS_ALIASES = {
    str(alias_from): str(alias_to)
    for alias_from, alias_to in dict(_STATUS_DEFAULTS.get("aliases") or {}).items()
}
STATUS_PARSE_ALIASES = {
    str(alias_from): str(alias_to)
    for alias_from, alias_to in dict(
        _STATUS_DEFAULTS.get("parse_aliases") or {}
    ).items()
}

PRIORITY_ORDER = [
    (_catalog_entry_label(entry), entry["slug"]) for entry in DEFAULT_PRIORITY_CATALOG
]
PRIORITY_ALIASES = {
    str(alias_from): str(alias_to)
    for alias_from, alias_to in dict(_PRIORITY_DEFAULTS.get("aliases") or {}).items()
}
PRIORITY_PARSE_ALIASES = {
    str(alias_from): str(alias_to)
    for alias_from, alias_to in dict(
        _PRIORITY_DEFAULTS.get("parse_aliases") or {}
    ).items()
}

MENU_UP = "u"
MENU_QUIT = "q"
MENU_NEXT = "j"
MENU_PREV = "k"
MENU_TOGGLE_SORT = "s"
MENU_TOGGLE_DIRECTION = "d"
MENU_REFRESH = "r"
MENU_PAGE_SIZE = 9

# H2 subsection header pattern — optional organizational structure within domain files
# Matches: ## Some Subsection Title
H2_SUBSECTION_PATTERN = re.compile(r"^##\s+(?P<section_title>.+?)\s*$", re.MULTILINE)

STATUS_PATTERN = re.compile(r"^- \*\*Status:\*\* (?P<status>.+?)\s*$", re.MULTILINE)
PRIORITY_PATTERN = re.compile(
    r"^- \*\*Priority:\*\* (?P<priority>.+?)\s*$", re.MULTILINE
)
BLOCKED_REASON_PATTERN = re.compile(r"^\*\*Blocked:\*\*\s*(.+?)\s*$", re.MULTILINE)
DEPRECATED_REASON_PATTERN = re.compile(
    r"^\*\*Deprecated:\*\*\s*(.+?)\s*$", re.MULTILINE
)
FLAGGED_PATTERN = re.compile(
    r"^- \*\*Flagged:\*\* (?P<flagged>true|false)\s*$", re.MULTILINE
)
TYPE_PATTERN = re.compile(
    r"^- \*\*Type:\*\* (?P<type>.+?)\s*$", re.MULTILINE
)
AFFECTS_PATTERN = re.compile(
    r"^- \*\*Affects:\*\* (?P<affects>.+?)\s*$", re.MULTILINE
)

# Canonical requirement type values.
REQUIREMENT_TYPES = ("feature", "bug")
DEFAULT_REQUIREMENT_TYPE = "feature"

LINKS_HEADER_PATTERN = re.compile(r"^- \*\*Links:\*\*\s*$", re.MULTILINE)
LINK_ITEM_PATTERN = re.compile(r"^  - (?P<link_text>.+)$", re.MULTILINE)
ID_PREFIX_PATTERN = re.compile(r"^[A-Z][A-Z0-9]*(-[A-Z][A-Z0-9]*)*$")
GENERIC_REQUIREMENT_HEADER_PATTERN = re.compile(
    r"^###\s+(?P<id>(?P<prefix>[A-Z][A-Z0-9]*)-[A-Z0-9-]+):\s*(?P<title>.+?)\s*$"
)
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]+\]\((?P<target>[^)#?]+\.md)(?:#[^)]+)?\)")
ANSI_ESCAPE_PATTERN = re.compile(r"\x1b\[[0-9;]*m")
NON_ALNUM_PREFIX_PATTERN = re.compile(r"^[^a-zA-Z0-9]+")
NON_ALNUM_PATTERN = re.compile(r"[^a-z0-9]+")

ANSI_RESET = "\x1b[0m"
# Default zebra stripe (light gray) — works on dark-background terminals.
ZEBRA_BG = "\x1b[48;5;254m"
# Zebra stripe for light-background terminals (medium gray).
ZEBRA_BG_LIGHT = "\x1b[48;5;250m"
# Fixed 256-color purple for Proposed status; avoids theme-dependent drift.
PROPOSED_FG = "\x1b[38;5;135m"
