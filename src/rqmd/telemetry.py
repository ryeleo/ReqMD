"""Telemetry client for rqmd AI agent self-reporting.

Provides a lightweight HTTP client that AI agents can use to submit
structured telemetry events (struggles, suggestions, errors) to a
configured telemetry gateway. Telemetry is enabled by default using
the built-in production endpoint. Set RQMD_TELEMETRY_DISABLED=1 to
opt out.
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

EventType = Literal["struggle", "suggestion", "error", "success", "workflow_step", "feedback"]
Severity = Literal["low", "medium", "high", "critical"]

_MAX_SNIPPET_LENGTH = 2000

# Built-in production defaults.  Override with env vars or rqmd.yml config.
_DEFAULT_ENDPOINT = "http://20.94.227.192:18080"

# Public client identifier used for token exchange.  This is non-secret —
# the gateway uses it to decide whether to issue a short-lived session token.
_CLIENT_ID = "rqmd-agent-v1"

# In-process token cache (populated lazily on first event submission).
_cached_token: str | None = None
_cached_token_expiry: float = 0.0

# Hidden file name for persisting the session token across CLI invocations.
_TOKEN_CACHE_FILENAME = ".rqmd-telemetry-token"


def _telemetry_disabled() -> bool:
    """Return True when the user has explicitly opted out of telemetry."""
    val = os.environ.get("RQMD_TELEMETRY_DISABLED", "").strip().lower()
    return val in {"1", "true", "yes"}


def _get_urllib():
    global _urllib_request
    if _urllib_request is None:
        import urllib.request

        _urllib_request = urllib.request
    return _urllib_request


def _token_cache_path() -> Path | None:
    """Return the path to the on-disk token cache file, or None if no repo root is findable."""
    # Walk up from cwd looking for a docs/requirements directory (rqmd project marker).
    try:
        cur = Path.cwd()
    except OSError:
        return None
    for parent in [cur, *cur.parents]:
        if (parent / "docs" / "requirements").is_dir():
            return parent / _TOKEN_CACHE_FILENAME
        if (parent / ".git").exists():
            return parent / _TOKEN_CACHE_FILENAME
    return None


def _read_cached_token_from_disk() -> tuple[str | None, float]:
    """Read a previously cached token from disk.

    Returns (token, expiry_timestamp) or (None, 0.0) if no valid cache exists.
    """
    cache_path = _token_cache_path()
    if cache_path is None or not cache_path.is_file():
        return None, 0.0
    try:
        data = json.loads(cache_path.read_text(encoding="utf-8"))
        token = data.get("token")
        expiry = float(data.get("expiry", 0.0))
        if token and isinstance(token, str):
            return token, expiry
    except (json.JSONDecodeError, OSError, ValueError, TypeError):
        pass
    return None, 0.0


def _write_token_to_disk(token: str, expiry: float) -> None:
    """Persist a session token to the on-disk cache file."""
    cache_path = _token_cache_path()
    if cache_path is None:
        return
    try:
        cache_path.write_text(
            json.dumps({"token": token, "expiry": expiry}),
            encoding="utf-8",
        )
        # Best-effort: restrict permissions to owner-only.
        cache_path.chmod(0o600)
    except OSError:
        pass


def _ensure_gitignore_entry() -> None:
    """Add the token cache filename to .gitignore if not already present."""
    cache_path = _token_cache_path()
    if cache_path is None:
        return
    gitignore = cache_path.parent / ".gitignore"
    try:
        if gitignore.is_file():
            contents = gitignore.read_text(encoding="utf-8")
            # Check if already covered (exact line match).
            for line in contents.splitlines():
                stripped = line.strip()
                if stripped == _TOKEN_CACHE_FILENAME or stripped == f"/{_TOKEN_CACHE_FILENAME}":
                    return
            # Append with a preceding newline if file doesn't end with one.
            suffix = "" if contents.endswith("\n") else "\n"
            gitignore.write_text(
                contents + suffix + _TOKEN_CACHE_FILENAME + "\n",
                encoding="utf-8",
            )
        else:
            gitignore.write_text(_TOKEN_CACHE_FILENAME + "\n", encoding="utf-8")
    except OSError:
        pass


def _get_session_token(endpoint: str) -> str | None:
    """Fetch a short-lived session token from the gateway via token exchange.

    Checks in-process cache first, then on-disk cache, then fetches fresh.
    Persists new tokens to disk for reuse across CLI invocations.
    Returns None on any failure (network, auth, etc.).
    """
    import time as _time

    global _cached_token, _cached_token_expiry

    now = _time.time()

    # 1. In-process cache (fastest).
    if _cached_token and now < (_cached_token_expiry - 60):
        return _cached_token

    # 2. On-disk cache (survives across CLI invocations).
    disk_token, disk_expiry = _read_cached_token_from_disk()
    if disk_token and now < (disk_expiry - 60):
        _cached_token = disk_token
        _cached_token_expiry = disk_expiry
        return disk_token

    # 3. Fresh token exchange with the gateway.
    url = f"{endpoint}/api/v1/token"
    body = json.dumps({"client_id": _CLIENT_ID}).encode("utf-8")

    try:
        urllib_request = _get_urllib()
        req = urllib_request.Request(
            url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib_request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            token = data.get("token")
            expires_in = data.get("expires_in", 3600)
            if token:
                expiry = now + expires_in
                _cached_token = token
                _cached_token_expiry = expiry
                # Persist to disk and ensure gitignored.
                _write_token_to_disk(token, expiry)
                _ensure_gitignore_entry()
                return token
    except Exception as exc:
        print(f"rqmd-telemetry: token exchange failed: {exc}", file=sys.stderr)

    return None


def resolve_telemetry_endpoint(repo_root: Path | None = None) -> str | None:
    """Return the telemetry endpoint URL.

    Resolution order:
    1. ``RQMD_TELEMETRY_DISABLED=1`` → returns None immediately.
    2. ``RQMD_TELEMETRY_ENDPOINT`` environment variable.
    3. ``telemetry.endpoint`` in ``rqmd.yml`` / ``rqmd.yaml`` / ``rqmd.json``.
    4. Built-in production default.
    """
    if _telemetry_disabled():
        return None

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

    return _DEFAULT_ENDPOINT


def resolve_telemetry_api_key(repo_root: Path | None = None) -> str | None:
    """Return the telemetry API key or session token.

    Resolution order:
    1. ``RQMD_TELEMETRY_DISABLED=1`` → returns None immediately.
    2. ``RQMD_TELEMETRY_API_KEY`` environment variable.
    3. ``telemetry.api_key`` in ``rqmd.yml`` / ``rqmd.yaml`` / ``rqmd.json``.
    4. Short-lived session token fetched from the gateway via token exchange.
    """
    if _telemetry_disabled():
        return None

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

    # Fall back to token exchange with the gateway.
    endpoint = resolve_telemetry_endpoint(repo_root)
    if endpoint:
        return _get_session_token(endpoint)
    return None


def _truncate(text: str | None, max_len: int = _MAX_SNIPPET_LENGTH) -> str | None:
    if text is None:
        return None
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


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
        for key in (
            "stderr_snippet",
            "stdout_snippet",
            "actual",
            "expected",
            "context",
        ):
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


def send_event(
    *,
    event_type: EventType,
    severity: Severity,
    summary: str,
    session_id: str | None = None,
    agent_name: str | None = None,
    detail: dict[str, Any] | None = None,
    repo_root: Path | None = None,
) -> dict[str, Any] | None:
    """High-level convenience wrapper that resolves endpoint and auth automatically.

    Resolves the telemetry endpoint and API key (including automatic token
    exchange) and submits the event in one call.  Returns the gateway
    response on success, or None when telemetry is disabled or submission
    fails.
    """
    endpoint = resolve_telemetry_endpoint(repo_root)
    if not endpoint:
        return None
    api_key = resolve_telemetry_api_key(repo_root)
    return submit_event(
        endpoint,
        event_type=event_type,
        severity=severity,
        summary=summary,
        session_id=session_id,
        agent_name=agent_name,
        detail=detail,
        api_key=api_key,
    )


def submit_artifact(
    endpoint: str,
    *,
    session_id: str,
    event_id: str,
    filename: str,
    content: bytes,
    content_type: str = "application/octet-stream",
    api_key: str | None = None,
) -> dict[str, Any] | None:
    """Upload an artifact to the telemetry gateway.

    Returns the parsed JSON response on success, or None on failure.
    Failures are logged to stderr but never raised.
    """
    if not endpoint:
        return None

    url = f"{endpoint}/api/v1/artifacts"
    boundary = uuid4().hex

    parts: list[bytes] = []
    for field_name, field_value in [("session_id", session_id), ("event_id", event_id)]:
        parts.append(
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="{field_name}"\r\n\r\n'
            f"{field_value}\r\n".encode()
        )
    parts.append(
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n".encode()
        + content
        + b"\r\n"
    )
    parts.append(f"--{boundary}--\r\n".encode())
    body = b"".join(parts)

    try:
        urllib_request = _get_urllib()
        headers: dict[str, str] = {
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        }
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        req = urllib_request.Request(url, data=body, headers=headers, method="POST")
        with urllib_request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except Exception as exc:
        print(f"rqmd-telemetry: failed to upload artifact: {exc}", file=sys.stderr)
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
