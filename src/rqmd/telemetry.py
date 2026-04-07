"""Telemetry client for rqmd AI agent self-reporting.

Provides a lightweight HTTP client that AI agents can use to submit
structured telemetry events (struggles, suggestions, errors) to a
configured telemetry gateway. Telemetry is opt-in and local-first:
no events are sent unless an endpoint is explicitly configured.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal
from uuid import uuid4

# Lazy import to keep startup fast when telemetry is not used.
_urllib_request = None

EventType = Literal["struggle", "suggestion", "error", "success", "workflow_step"]
Severity = Literal["low", "medium", "high", "critical"]

_MAX_SNIPPET_LENGTH = 2000


def _get_urllib():
    global _urllib_request
    if _urllib_request is None:
        import urllib.request
        _urllib_request = urllib.request
    return _urllib_request


def resolve_telemetry_endpoint(repo_root: Path | None = None) -> str | None:
    """Return the configured telemetry endpoint, or None if not configured.

    Checks in order:
    1. RQMD_TELEMETRY_ENDPOINT environment variable
    2. telemetry.endpoint in .rqmd.yml / .rqmd.yaml / .rqmd.json
    """
    env_endpoint = os.environ.get("RQMD_TELEMETRY_ENDPOINT")
    if env_endpoint:
        return env_endpoint.rstrip("/")

    if repo_root is not None:
        try:
            from .config import load_config
            config = load_config(repo_root)
            telemetry_config = config.get("telemetry", {})
            if isinstance(telemetry_config, dict):
                endpoint = telemetry_config.get("endpoint")
                if endpoint:
                    return str(endpoint).rstrip("/")
        except Exception:
            pass

    return None


def resolve_telemetry_api_key(repo_root: Path | None = None) -> str | None:
    """Return the configured telemetry API key, or None if not configured.

    Checks in order:
    1. RQMD_TELEMETRY_API_KEY environment variable
    2. telemetry.api_key in .rqmd.yml / .rqmd.yaml / .rqmd.json
    """
    env_key = os.environ.get("RQMD_TELEMETRY_API_KEY")
    if env_key:
        return env_key

    if repo_root is not None:
        try:
            from .config import load_config
            config = load_config(repo_root)
            telemetry_config = config.get("telemetry", {})
            if isinstance(telemetry_config, dict):
                api_key = telemetry_config.get("api_key")
                if api_key:
                    return str(api_key)
        except Exception:
            pass

    return None


def _truncate(text: str | None, max_len: int = _MAX_SNIPPET_LENGTH) -> str | None:
    if text is None:
        return None
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."


def submit_event(
    endpoint: str,
    *,
    event_type: EventType,
    severity: Severity,
    summary: str,
    session_id: str | None = None,
    agent_name: str | None = None,
    detail: dict[str, Any] | None = None,
    api_key: str | None = None,
) -> dict[str, Any] | None:
    """Submit a telemetry event to the gateway.

    Returns the parsed JSON response on success, or None on failure.
    Failures are logged to stderr but never raised.
    """
    if not endpoint:
        return None

    url = f"{endpoint}/api/v1/events"
    payload: dict[str, Any] = {
        "session_id": session_id or str(uuid4()),
        "event_type": event_type,
        "severity": severity,
        "summary": _truncate(summary, 200) or "",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    if agent_name:
        payload["agent_name"] = agent_name

    if detail:
        # Truncate known large text fields in detail.
        sanitized = dict(detail)
        for key in ("stderr_snippet", "stdout_snippet", "actual", "expected", "context"):
            if key in sanitized and isinstance(sanitized[key], str):
                sanitized[key] = _truncate(sanitized[key])
        payload["detail"] = sanitized

    body = json.dumps(payload).encode("utf-8")

    try:
        urllib_request = _get_urllib()
        headers: dict[str, str] = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        req = urllib_request.Request(
            url,
            data=body,
            headers=headers,
            method="POST",
        )
        with urllib_request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except Exception as exc:
        print(f"rqmd-telemetry: failed to submit event: {exc}", file=sys.stderr)
        return None


def report_struggle(
    endpoint: str,
    *,
    summary: str,
    command: str | None = None,
    expected: str | None = None,
    actual: str | None = None,
    stderr_snippet: str | None = None,
    severity: Severity = "medium",
    session_id: str | None = None,
    agent_name: str | None = None,
    api_key: str | None = None,
) -> dict[str, Any] | None:
    """Convenience wrapper for submitting a struggle event."""
    detail: dict[str, Any] = {}
    if command:
        detail["command"] = command
    if expected:
        detail["expected"] = expected
    if actual:
        detail["actual"] = actual
    if stderr_snippet:
        detail["stderr_snippet"] = stderr_snippet
    return submit_event(
        endpoint,
        event_type="struggle",
        severity=severity,
        summary=summary,
        session_id=session_id,
        agent_name=agent_name,
        detail=detail or None,
        api_key=api_key,
    )


def report_suggestion(
    endpoint: str,
    *,
    summary: str,
    suggestion: str,
    confidence: Literal["low", "medium", "high"] = "medium",
    command: str | None = None,
    severity: Severity = "low",
    session_id: str | None = None,
    agent_name: str | None = None,
    api_key: str | None = None,
) -> dict[str, Any] | None:
    """Convenience wrapper for submitting a suggestion event."""
    detail: dict[str, Any] = {
        "suggestion": suggestion,
        "confidence": confidence,
    }
    if command:
        detail["command"] = command
    return submit_event(
        endpoint,
        event_type="suggestion",
        severity=severity,
        summary=summary,
        session_id=session_id,
        agent_name=agent_name,
        detail=detail,
        api_key=api_key,
    )


def report_error(
    endpoint: str,
    *,
    summary: str,
    command: str | None = None,
    stderr_snippet: str | None = None,
    severity: Severity = "high",
    session_id: str | None = None,
    agent_name: str | None = None,
    api_key: str | None = None,
) -> dict[str, Any] | None:
    """Convenience wrapper for submitting an error event."""
    detail: dict[str, Any] = {}
    if command:
        detail["command"] = command
    if stderr_snippet:
        detail["stderr_snippet"] = stderr_snippet
    return submit_event(
        endpoint,
        event_type="error",
        severity=severity,
        summary=summary,
        session_id=session_id,
        agent_name=agent_name,
        detail=detail or None,
        api_key=api_key,
    )


def report_command_discovery_struggle(
    endpoint: str,
    *,
    summary: str,
    commands_attempted: list[str],
    fallback_action: str | None = None,
    stderr_snippet: str | None = None,
    session_id: str | None = None,
    agent_name: str | None = None,
    api_key: str | None = None,
) -> dict[str, Any] | None:
    """Report a command-discovery struggle when rqmd/rqmd-ai cannot be invoked.

    This is a high-signal friction category: when agents cannot find or run
    the CLI, the entire rqmd workflow contract breaks and the agent falls back
    to direct file manipulation.
    """
    detail: dict[str, Any] = {
        "category": "command_discovery",
        "commands_attempted": commands_attempted,
    }
    if fallback_action:
        detail["fallback_action"] = fallback_action
    if stderr_snippet:
        detail["stderr_snippet"] = stderr_snippet
    return submit_event(
        endpoint,
        event_type="struggle",
        severity="high",
        summary=summary,
        session_id=session_id,
        agent_name=agent_name,
        detail=detail,
        api_key=api_key,
    )
