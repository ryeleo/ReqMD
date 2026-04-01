from __future__ import annotations

import importlib.resources
from typing import Any

_CATALOG_RESOURCE_ROOT = ("resources", "catalogs")


def _catalog_resource_path(filename: str) -> Any:
    return importlib.resources.files("rqmd").joinpath(*_CATALOG_RESOURCE_ROOT, filename)


def _load_yaml_resource(filename: str) -> dict[str, Any]:
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            f"Default catalog resource loading requires PyYAML while reading {filename}"
        ) from exc

    resource = _catalog_resource_path(filename)
    try:
        data = yaml.safe_load(resource.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(f"Missing packaged default catalog resource: {filename}") from exc
    except Exception as exc:
        raise RuntimeError(f"Invalid packaged default catalog resource {filename}: {exc}") from exc

    if not isinstance(data, dict):
        raise RuntimeError(f"Packaged default catalog resource {filename} must be a mapping")
    return data


def load_default_status_catalog_resource() -> dict[str, Any]:
    data = _load_yaml_resource("statuses.yml")
    statuses = data.get("statuses")
    if not isinstance(statuses, list) or not statuses:
        raise RuntimeError("Packaged default status catalog must define a non-empty 'statuses' list")
    return data


def load_default_priority_catalog_resource() -> dict[str, Any]:
    data = _load_yaml_resource("priorities.yml")
    priorities = data.get("priorities")
    if not isinstance(priorities, list) or not priorities:
        raise RuntimeError("Packaged default priority catalog must define a non-empty 'priorities' list")
    return data