"""In-process caching layer for parsed requirement data.

Caches file text reads and parsed requirement lists keyed by
(path, mtime_ns, size) so that repeated access within a single
process (e.g. parse then body-extract for the same file) avoids
redundant I/O and re-parsing.

The cache is invalidated automatically when a file's mtime or
size changes.  It can also be cleared explicitly via ``clear()``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

# Cache keyed by resolved path -> (mtime_ns, size, payload).
_text_cache: dict[Path, tuple[int, int, str]] = {}
_parse_cache: dict[
    tuple[Path, tuple[str, ...]], tuple[int, int, list[dict[str, Any]]]
] = {}


def _file_key(path: Path) -> tuple[int, int]:
    stat = path.stat()
    return stat.st_mtime_ns, stat.st_size


def read_text_cached(path: Path) -> str:
    """Read file text with mtime+size caching."""
    resolved = path.resolve()
    key = _file_key(resolved)
    cached = _text_cache.get(resolved)
    if cached is not None and (cached[0], cached[1]) == key:
        return cached[2]
    text = resolved.read_text(encoding="utf-8")
    _text_cache[resolved] = (key[0], key[1], text)
    return text


def get_parsed(path: Path, id_prefixes: tuple[str, ...]) -> list[dict[str, Any]] | None:
    """Return cached parse results if still valid, else None."""
    resolved = path.resolve()
    cache_key = (resolved, id_prefixes)
    cached = _parse_cache.get(cache_key)
    if cached is None:
        return None
    key = _file_key(resolved)
    if (cached[0], cached[1]) != key:
        return None
    return cached[2]


def put_parsed(
    path: Path, id_prefixes: tuple[str, ...], result: list[dict[str, Any]]
) -> None:
    """Store parse results in the cache."""
    resolved = path.resolve()
    key = _file_key(resolved)
    _parse_cache[(resolved, id_prefixes)] = (key[0], key[1], result)


def clear() -> None:
    """Clear all caches."""
    _text_cache.clear()
    _parse_cache.clear()
