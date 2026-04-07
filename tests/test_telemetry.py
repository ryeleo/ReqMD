"""Tests for the rqmd telemetry client module (RQMD-TELEMETRY-002 through 007)."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from threading import Thread
from unittest.mock import patch

import pytest
from rqmd.telemetry import (
    report_error,
    report_struggle,
    report_suggestion,
    resolve_telemetry_endpoint,
    submit_event,
)
class TestResolveTelemetryEndpoint:
    def test_returns_none_when_unconfigured(self, tmp_path: Path):
        """RQMD-TELEMETRY-007: No endpoint configured means no telemetry."""
        with patch.dict("os.environ", {}, clear=True):
            assert resolve_telemetry_endpoint(tmp_path) is None

    def test_env_var_takes_precedence(self, tmp_path: Path):
        """RQMD-TELEMETRY-007: Env var is highest priority."""
        config_file = tmp_path / ".rqmd.yml"
        config_file.write_text("telemetry:\n  endpoint: http://from-config:8080\n")
        with patch.dict("os.environ", {"RQMD_TELEMETRY_ENDPOINT": "http://from-env:8080"}):
            assert resolve_telemetry_endpoint(tmp_path) == "http://from-env:8080"

    def test_strips_trailing_slash(self, tmp_path: Path):
        with patch.dict("os.environ", {"RQMD_TELEMETRY_ENDPOINT": "http://localhost:8080/"}):
            assert resolve_telemetry_endpoint(tmp_path) == "http://localhost:8080"

    def test_reads_from_config_file(self, tmp_path: Path):
        config_file = tmp_path / ".rqmd.yml"
        config_file.write_text("telemetry:\n  endpoint: http://config-host:18080\n")
        with patch.dict("os.environ", {}, clear=True):
            assert resolve_telemetry_endpoint(tmp_path) == "http://config-host:18080"

    def test_returns_none_when_config_has_no_telemetry(self, tmp_path: Path):
        config_file = tmp_path / ".rqmd.yml"
        config_file.write_text("requirements_dir: docs/requirements\n")
        with patch.dict("os.environ", {}, clear=True):
            assert resolve_telemetry_endpoint(tmp_path) is None


# ---------------------------------------------------------------------------
# Stub HTTP server for event submission tests
# ---------------------------------------------------------------------------


class _StubHandler(BaseHTTPRequestHandler):
    """Minimal handler that records POSTed JSON bodies."""

    received: list[dict] = []

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))
        _StubHandler.received.append(body)
        response = json.dumps({"event_id": "test-event-id", "session_id": body.get("session_id"), "status": "accepted"})
        self.send_response(201)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(response.encode())

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status":"healthy","postgres":true,"minio":true}')

    def log_message(self, format, *args):
        pass  # Suppress request logging during tests.


@pytest.fixture
def telemetry_server():
    """Start a local stub telemetry server and yield its base URL."""
    _StubHandler.received = []
    server = HTTPServer(("127.0.0.1", 0), _StubHandler)
    port = server.server_address[1]
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{port}"
    server.shutdown()


# ---------------------------------------------------------------------------
# submit_event
# ---------------------------------------------------------------------------


class TestSubmitEvent:
    def test_returns_none_when_no_endpoint(self):
        """RQMD-TELEMETRY-007: submit_event is a no-op with empty endpoint."""
        result = submit_event("", event_type="error", severity="high", summary="test")
        assert result is None

    def test_posts_event_to_endpoint(self, telemetry_server: str):
        """RQMD-TELEMETRY-002/003: event reaches the gateway with correct schema."""
        result = submit_event(
            telemetry_server,
            event_type="struggle",
            severity="medium",
            summary="Could not parse JSON output",
            agent_name="rqmd-dev",
            session_id="00000000-0000-0000-0000-000000000001",
            detail={"command": "rqmd-ai --json"},
        )
        assert result is not None
        assert result["status"] == "accepted"
        assert len(_StubHandler.received) == 1
        body = _StubHandler.received[0]
        assert body["event_type"] == "struggle"
        assert body["severity"] == "medium"
        assert body["agent_name"] == "rqmd-dev"
        assert body["detail"]["command"] == "rqmd-ai --json"

    def test_truncates_long_summary(self, telemetry_server: str):
        """RQMD-TELEMETRY-002: summary is capped at 200 chars."""
        long_summary = "x" * 500
        submit_event(
            telemetry_server,
            event_type="error",
            severity="high",
            summary=long_summary,
        )
        body = _StubHandler.received[0]
        assert len(body["summary"]) <= 200

    def test_truncates_detail_snippets(self, telemetry_server: str):
        """RQMD-TELEMETRY-005: large stderr snippets are truncated."""
        submit_event(
            telemetry_server,
            event_type="error",
            severity="high",
            summary="test",
            detail={"stderr_snippet": "e" * 5000},
        )
        body = _StubHandler.received[0]
        assert len(body["detail"]["stderr_snippet"]) <= 2003  # 2000 + "..."

    def test_handles_unreachable_endpoint_gracefully(self):
        """RQMD-TELEMETRY-003: unreachable endpoint returns None instead of raising."""
        result = submit_event(
            "http://127.0.0.1:1",  # almost certainly not listening
            event_type="error",
            severity="high",
            summary="should not crash",
        )
        assert result is None


# ---------------------------------------------------------------------------
# Convenience wrappers
# ---------------------------------------------------------------------------


class TestReportStruggle:
    def test_posts_struggle_event(self, telemetry_server: str):
        """RQMD-TELEMETRY-005: struggle events include expected detail fields."""
        result = report_struggle(
            telemetry_server,
            summary="rqmd --verify-summaries exited 1",
            command="rqmd --verify-summaries",
            expected="exit 0",
            actual="exit 1 with summary mismatch",
            stderr_snippet="Error: summary mismatch in core-engine.md",
        )
        assert result is not None
        body = _StubHandler.received[0]
        assert body["event_type"] == "struggle"
        assert body["detail"]["command"] == "rqmd --verify-summaries"
        assert body["detail"]["expected"] == "exit 0"


class TestReportSuggestion:
    def test_posts_suggestion_event(self, telemetry_server: str):
        """RQMD-TELEMETRY-006: suggestion events include suggestion text and confidence."""
        result = report_suggestion(
            telemetry_server,
            summary="rqmd-ai JSON output should include domain file path in each requirement",
            suggestion="Add a 'domain_file' field to each requirement in --dump-status output",
            confidence="high",
            command="rqmd-ai --json --dump-status proposed",
        )
        assert result is not None
        body = _StubHandler.received[0]
        assert body["event_type"] == "suggestion"
        assert body["detail"]["suggestion"].startswith("Add a")
        assert body["detail"]["confidence"] == "high"


class TestReportError:
    def test_posts_error_event(self, telemetry_server: str):
        """RQMD-TELEMETRY-005: error events include stderr output."""
        result = report_error(
            telemetry_server,
            summary="rqmd crashed with traceback",
            command="rqmd --verify-summaries",
            stderr_snippet="Traceback (most recent call last): ...",
        )
        assert result is not None
        body = _StubHandler.received[0]
        assert body["event_type"] == "error"
        assert body["severity"] == "high"
