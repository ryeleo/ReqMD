from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_config(repo_root: Path) -> dict[str, Any]:
    """
    Load project configuration from .rqmd.json at repo root.
    
    Precedence:
    1. CLI flags (handled by Click, not this function)
    2. .rqmd.json values (this function)
    3. Built-in defaults (handled by Click)
    
    Args:
        repo_root: Path to project root
        
    Returns:
        Dictionary of config values; empty dict if no config file exists
    """
    config_path = repo_root / ".rqmd.json"
    
    if not config_path.exists():
        return {}
    
    if not config_path.is_file():
        raise ValueError(f"Config file exists but is not a file: {config_path}")
    
    try:
        content = config_path.read_text(encoding="utf-8")
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {config_path}: {e}") from e
    except OSError as e:
        raise ValueError(f"Cannot read {config_path}: {e}") from e


def validate_config(config: dict[str, Any]) -> None:
    """
    Validate that config keys are known and values are reasonable.
    
    Args:
        config: Configuration dictionary
        
    Raises:
        ValueError: If config is invalid
    """
    allowed_keys = {
        "repo_root",
        "requirements_dir",
        "id_prefix",
        "sort_strategy",
        "state_dir",
    }
    
    for key in config:
        if key not in allowed_keys:
            raise ValueError(f"Unknown config key: {key}. Allowed keys: {', '.join(sorted(allowed_keys))}")
    
    # Validate types
    if "repo_root" in config and not isinstance(config["repo_root"], str):
        raise ValueError("Config key 'repo_root' must be a string")
    if "requirements_dir" in config and not isinstance(config["requirements_dir"], str):
        raise ValueError("Config key 'requirements_dir' must be a string")
    if "id_prefix" in config and not isinstance(config["id_prefix"], str):
        raise ValueError("Config key 'id_prefix' must be a string")
    if "sort_strategy" in config and not isinstance(config["sort_strategy"], str):
        raise ValueError("Config key 'sort_strategy' must be a string")
    if "state_dir" in config and not isinstance(config["state_dir"], str):
        raise ValueError("Config key 'state_dir' must be a string")
