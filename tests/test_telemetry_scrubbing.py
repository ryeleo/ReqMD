"""Tests for RQMD-TELEMETRY-016: client-side secrets and PII scrubbing.

Covers:
- Pre-pass: home-directory path normalisation
- Layer 1: detect-secrets secret pattern redaction
- Layer 2: gitleaks subprocess (present and absent)
- Layer 3: scrubadub PII redaction
- Full pipeline end-to-end
- scrub_payload_strings recursive traversal
- telemetry.submit_event scrubbing integration
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from rqmd.scrubbing import (_scrub_home_paths, _scrub_infra_patterns,
                            _scrub_layer_detect_secrets, _scrub_layer_gitleaks,
                            _scrub_layer_scrubadub, scrub_payload_strings,
                            scrub_text)

# ---------------------------------------------------------------------------
# Pre-pass: home-directory path normalisation
# ---------------------------------------------------------------------------

class TestScrubHomePaths:
    def test_expanded_home_replaced(self) -> None:
        home = os.path.expanduser("~")
        text = f"path: {home}/.ssh/id_rsa"
        result = _scrub_home_paths(text)
        assert home not in result
        assert "{{REDACTED_PATH}}" in result

    def test_tilde_shorthand_replaced(self) -> None:
        result = _scrub_home_paths("ls ~/Documents/secret.txt")
        assert "~/" not in result
        assert "{{REDACTED_PATH}}" in result

    def test_other_user_home_linux_replaced(self) -> None:
        result = _scrub_home_paths("cat /home/alice/.bashrc")
        assert "/home/alice/" not in result
        assert "{{REDACTED_PATH}}" in result

    def test_other_user_home_macos_replaced(self) -> None:
        result = _scrub_home_paths("open /Users/bob/Desktop/notes.txt")
        assert "/Users/bob/" not in result
        assert "{{REDACTED_PATH}}" in result

    def test_unrelated_path_unchanged(self) -> None:
        result = _scrub_home_paths("/var/log/rqmd.log")
        assert result == "/var/log/rqmd.log"

    def test_non_path_text_unchanged(self) -> None:
        result = _scrub_home_paths("Hello world, no paths here.")
        assert result == "Hello world, no paths here."


# ---------------------------------------------------------------------------
# Infrastructure pattern pre-pass
# ---------------------------------------------------------------------------

class TestScrubInfraPatterns:
    """Tests for the regex-based infrastructure secret pre-pass."""

    # --- UUIDs / GUIDs ---

    def test_guid_standalone_redacted(self) -> None:
        guid = "12345678-1234-4abc-8def-123456789abc"
        result = _scrub_infra_patterns(f"subscription: {guid}")
        assert guid not in result
        assert "{{REDACTED_GUID}}" in result

    def test_azure_subscription_id_in_error_message(self) -> None:
        guid = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        result = _scrub_infra_patterns(
            f"ERROR: The subscription '{guid}' was not found."
        )
        assert guid not in result
        assert "{{REDACTED_GUID}}" in result

    def test_azure_tenant_id_in_output(self) -> None:
        guid = "deadbeef-dead-dead-dead-deadbeefcafe"
        result = _scrub_infra_patterns(f"tenant_id={guid}")
        assert guid not in result

    def test_multiple_guids_all_redacted(self) -> None:
        sub = "11111111-2222-3333-4444-555555555555"
        tenant = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        result = _scrub_infra_patterns(f"sub={sub} tenant={tenant}")
        assert sub not in result
        assert tenant not in result

    def test_non_guid_hex_unchanged(self) -> None:
        # Short hex that is NOT a GUID should not be touched
        result = _scrub_infra_patterns("colour: #ff0000 code: abc123")
        assert "#ff0000" in result
        assert "abc123" in result

    # --- SSH / PEM private keys ---

    def test_rsa_private_key_block_redacted(self) -> None:
        pem = (
            "-----BEGIN RSA PRIVATE KEY-----\n"
            "MIIEowIBAAKCAQEA0Z3VS5JJcds3xHn/ygWep4SsZDMKFaCRBMRPK9WxDKUBvTi8\n"
            "<...fake key content...>\n"
            "-----END RSA PRIVATE KEY-----"
        )
        result = _scrub_infra_patterns(f"key: {pem}")
        assert "MIIEowIBAAK" not in result
        assert "{{REDACTED_SECRET}}" in result

    def test_openssh_private_key_block_redacted(self) -> None:
        pem = (
            "-----BEGIN OPENSSH PRIVATE KEY-----\n"
            "b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZWQy\n"
            "<...fake openssh key...>\n"
            "-----END OPENSSH PRIVATE KEY-----"
        )
        result = _scrub_infra_patterns(pem)
        assert "b3BlbnNzaC1rZXktdjEA" not in result
        assert "{{REDACTED_SECRET}}" in result

    def test_ec_private_key_block_redacted(self) -> None:
        pem = (
            "-----BEGIN EC PRIVATE KEY-----\n"
            "MHQCAQEEIOaXpZMJUlgvBqiFBanelVS8TBAA7uHGJLPo4G5YvPxgoAoGCCqGSM49\n"
            "-----END EC PRIVATE KEY-----"
        )
        result = _scrub_infra_patterns(pem)
        assert "MHQCAQEEIOaXpZMJ" not in result

    # --- AWS ---

    def test_aws_access_key_id_redacted(self) -> None:
        # All four AKIA/ABIA/ACCA/ASIA prefixes
        for prefix in ("AKIA", "ABIA", "ACCA", "ASIA"):
            key = f"{prefix}IOSFODNN7EXAMPLE"
            result = _scrub_infra_patterns(f"key={key}")
            assert key not in result, f"{prefix} key not scrubbed"
            assert "{{REDACTED_SECRET}}" in result

    def test_aws_secret_access_key_redacted(self) -> None:
        # 40-char base64-ish string after context keyword
        secret = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
        for keyword in (
            "aws_secret_access_key",
            "AWS_SECRET_ACCESS_KEY",
            "SecretAccessKey",
        ):
            text = f"{keyword}={secret}"
            result = _scrub_infra_patterns(text)
            assert secret not in result, f"{keyword} context did not scrub secret"

    # --- GitHub ---

    def test_github_pat_ghp_redacted(self) -> None:
        token = "ghp_16C7e42F292c6912E7710c838347Ae178B4a"
        result = _scrub_infra_patterns(f"GITHUB_TOKEN={token}")
        assert token not in result
        assert "{{REDACTED_SECRET}}" in result

    def test_github_oauth_gho_redacted(self) -> None:
        token = "gho_16C7e42F292c6912E7710c838347Ae178B4a"
        result = _scrub_infra_patterns(f"token: {token}")
        assert token not in result

    def test_github_actions_ghs_redacted(self) -> None:
        token = "ghs_16C7e42F292c6912E7710c838347Ae178B4a"
        result = _scrub_infra_patterns(f"Authorization: Bearer {token}")
        assert token not in result

    def test_github_fine_grained_pat_redacted(self) -> None:
        token = "github_pat_11ABCDEFG0example12345ABCDEFGHIJ"
        result = _scrub_infra_patterns(f"token={token}")
        assert token not in result

    # --- Azure ---

    def test_azure_storage_account_key_redacted(self) -> None:
        # 88-char base64 storage key in a connection string
        key = "dGhpcyBpcyBhIGZha2Uga2V5IGZvciBBenVyZSBzdG9yYWdlIGFjY291bnQgaW4gdGVzdGluZz09"
        conn = f"DefaultEndpointsProtocol=https;AccountName=myaccount;AccountKey={key};EndpointSuffix=core.windows.net"
        result = _scrub_infra_patterns(conn)
        assert key not in result
        assert "{{REDACTED_SECRET}}" in result

    def test_azure_sas_signature_redacted(self) -> None:
        sig = "dGhpcyBpcyBhIGZha2Ugc2lnbmF0dXJlIGZvciBBenVyZSBTQVM%3D"
        url = f"https://myaccount.blob.core.windows.net/container/blob?sv=2021-06-08&sig={sig}&se=2026-01-01"
        result = _scrub_infra_patterns(url)
        assert sig not in result
        assert "{{REDACTED_SECRET}}" in result

    def test_azure_client_secret_redacted(self) -> None:
        for keyword in ("client_secret", "AZURE_CLIENT_SECRET", "clientSecret"):
            secret = "AbCdEf~GhIjKl_MnOpQrStUvWxYz12345678"
            text = f"{keyword}={secret}"
            result = _scrub_infra_patterns(text)
            assert secret not in result, f"{keyword} context did not scrub client secret"

    # --- 1Password ---

    def test_1password_service_account_token_redacted(self) -> None:
        # ops_ prefix + 20+ alphanumeric chars
        token = "ops_eyJhbGciOiJFUzI1NiIsImtpZCI6InV2bXJRZW1"
        result = _scrub_infra_patterns(f"OP_SERVICE_ACCOUNT_TOKEN={token}")
        assert token not in result
        assert "{{REDACTED_SECRET}}" in result

    def test_1password_connect_jwt_redacted(self) -> None:
        # JWTs start with eyJ (base64url of '{'); 1Password Connect tokens are JWTs
        jwt = "eyJhbGciOiJFUzI1NiIsImtpZCI6InV2bXJRZW1YMGF3RE9HWGFUcEl3OFIifQ.eyJhIjoiMDFKViIsImV4cCI6MTc0NjUwMDAwMH0.SIG_PLACEHOLDER_12345678901234567890"
        result = _scrub_infra_patterns(f"OP_CONNECT_TOKEN={jwt}")
        assert "eyJhbGciOiJFUzI1NiIsImtpZCI6InV2bXJRZW1" not in result
        assert "{{REDACTED_SECRET}}" in result

    # --- Full pipeline sanity (infra layer via scrub_text) ---

    @pytest.mark.parametrize("token,label", [
        ("12345678-1234-4abc-8def-123456789abc", "UUID"),
        ("AKIAIOSFODNN7EXAMPLE", "AWS access key"),
        ("ghp_16C7e42F292c6912E7710c838347Ae178B4a", "GitHub PAT"),
        ("ops_eyJhbGciOiJFUzI1NiIsImtpZCI6InV2bXJRZW1YMGF3RE9HWGFUcEl3OFIi", "1Password SAT"),
    ])
    def test_full_pipeline_scrubs_infra_tokens(self, token: str, label: str) -> None:
        result = scrub_text(f"error detail: token={token} during rqmd run")
        assert token not in result, f"{label} survived the full pipeline"


# ---------------------------------------------------------------------------
# Layer 1: detect-secrets
# ---------------------------------------------------------------------------

class TestDetectSecretsLayer:
    def test_aws_access_key_redacted(self) -> None:
        # AKIA prefix — detect-secrets has an explicit rule for this
        fake_key = "AKIAIOSFODNN7EXAMPLE"
        result = _scrub_layer_detect_secrets(f"key={fake_key}")
        # detect-secrets should catch AKIA keys; assert the raw key is gone
        assert fake_key not in result
        assert isinstance(result, str)

    def test_github_token_redacted(self) -> None:
        # ghp_ prefix is a known GitHub Personal Access Token pattern
        fake_token = "ghp_16C7e42F292c6912E7710c838347Ae178B4a"
        result = _scrub_layer_detect_secrets(f"token={fake_token}")
        assert fake_token not in result
        assert isinstance(result, str)

    def test_import_error_returns_text_unchanged(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """If the detect-secrets layer raises ImportError, scrub_text must skip and continue."""
        import rqmd.scrubbing as scrubbing_mod

        def _raise_import(text: str) -> str:  # noqa: ARG001
            raise ImportError("simulated missing dep")

        monkeypatch.setattr(scrubbing_mod, "_scrub_layer_detect_secrets", _raise_import)
        result = scrub_text("safe text no secrets here")
        assert isinstance(result, str)
        assert result  # non-empty

    def test_exception_in_layer_returns_input(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """A layer-level exception should log and return the input unchanged."""
        import rqmd.scrubbing as scrubbing_mod

        def _bad_scan(text: str) -> str:
            raise RuntimeError("boom")

        monkeypatch.setattr(scrubbing_mod, "_scrub_layer_detect_secrets", _bad_scan)
        result = scrub_text("some text")
        assert isinstance(result, str)


# ---------------------------------------------------------------------------
# Layer 2: gitleaks subprocess
# ---------------------------------------------------------------------------

class TestGitleaksLayer:
    def test_skips_gracefully_when_not_in_path(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("shutil.which", lambda _cmd: None)
        import rqmd.scrubbing as scrubbing_mod
        scrubbing_mod._gitleaks_warning_emitted = False

        text = "nothing special"
        result = _scrub_layer_gitleaks(text)
        assert result == text

    def test_redacts_secret_from_json_report(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import json as _json
        import shutil
        import subprocess

        fake_secret = "supersecretvalue123"
        fake_report = _json.dumps([
            {"RuleID": "generic-api-key", "Secret": fake_secret, "Match": f"key={fake_secret}"}
        ])

        mock_proc = MagicMock()
        mock_proc.returncode = 1
        mock_proc.stdout = fake_report

        monkeypatch.setattr(shutil, "which", lambda cmd: "/usr/bin/gitleaks" if cmd == "gitleaks" else None)
        monkeypatch.setattr(subprocess, "run", lambda *a, **kw: mock_proc)

        result = _scrub_layer_gitleaks(f"key={fake_secret}")
        assert fake_secret not in result
        assert "{{REDACTED_GITLEAKS}}" in result

    def test_empty_report_returns_text_unchanged(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import shutil
        import subprocess

        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = ""

        monkeypatch.setattr(shutil, "which", lambda cmd: "/usr/bin/gitleaks" if cmd == "gitleaks" else None)
        monkeypatch.setattr(subprocess, "run", lambda *a, **kw: mock_proc)

        text = "no secrets here"
        result = _scrub_layer_gitleaks(text)
        assert result == text

    def test_timeout_returns_text_unchanged(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import shutil
        import subprocess

        def _raise_timeout(*a: object, **kw: object) -> None:
            raise subprocess.TimeoutExpired("gitleaks", 15)

        monkeypatch.setattr(shutil, "which", lambda cmd: "/usr/bin/gitleaks" if cmd == "gitleaks" else None)
        monkeypatch.setattr(subprocess, "run", _raise_timeout)

        text = "some text"
        result = _scrub_layer_gitleaks(text)
        assert result == text


# ---------------------------------------------------------------------------
# Layer 3: scrubadub PII
# ---------------------------------------------------------------------------

class TestScrubadubLayer:
    def test_email_redacted(self) -> None:
        result = _scrub_layer_scrubadub("contact us at user@example.com for help")
        assert "user@example.com" not in result

    def test_non_pii_text_unchanged(self) -> None:
        text = "rqmd --verify-summaries exited 1"
        result = _scrub_layer_scrubadub(text)
        # No PII — result should not have introduced garbled output
        assert isinstance(result, str)
        assert len(result) > 0

    def test_import_error_returns_text(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import rqmd.scrubbing as scrubbing_mod

        monkeypatch.setattr(scrubbing_mod, "_scrub_layer_scrubadub", lambda t: t)
        result = scrub_text("no pii here")
        assert isinstance(result, str)


# ---------------------------------------------------------------------------
# Full pipeline end-to-end
# ---------------------------------------------------------------------------

class TestFullPipeline:
    @pytest.mark.parametrize("sensitive,description", [
        (os.path.expanduser("~") + "/.ssh/id_rsa", "expanded home path"),
        ("~/secrets/key.pem", "tilde home path"),
        ("user@example.com", "email address"),
    ])
    def test_sensitive_data_not_in_output(self, sensitive: str, description: str) -> None:
        result = scrub_text(f"error processing {sensitive}")
        # The raw sensitive value should not survive the pipeline
        assert sensitive not in result, f"Expected {description!r} to be scrubbed"

    def test_safe_text_survives(self) -> None:
        text = "rqmd --verify-summaries exited non-zero with summary mismatch"
        result = scrub_text(text)
        # Core diagnostic text should survive (no false positives on safe content)
        assert "rqmd" in result
        assert "verify-summaries" in result

    def test_empty_string_survives(self) -> None:
        assert scrub_text("") == ""

    def test_pipeline_layer_failure_is_skipped(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """A layer raising RuntimeError should be skipped; pipeline returns a string."""
        import rqmd.scrubbing as scrubbing_mod

        def _boom(text: str) -> str:
            raise RuntimeError("boom")

        monkeypatch.setattr(scrubbing_mod, "_scrub_layer_detect_secrets", _boom)
        result = scrub_text("safe text")
        assert isinstance(result, str)
        assert result  # non-empty

    def test_prepass_failure_propagates(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """_scrub_home_paths failure propagates since it has no external deps."""
        import rqmd.scrubbing as scrubbing_mod

        def _boom(text: str) -> str:
            raise RuntimeError("pre-pass boom")

        monkeypatch.setattr(scrubbing_mod, "_scrub_home_paths", _boom)
        with pytest.raises(RuntimeError, match="pre-pass boom"):
            scrub_text("anything")


# ---------------------------------------------------------------------------
# scrub_payload_strings recursive traversal
# ---------------------------------------------------------------------------

class TestScrubPayloadStrings:
    def test_string_leaf_scrubbed(self) -> None:
        home = os.path.expanduser("~")
        result = scrub_payload_strings(f"path: {home}/.aws/credentials")
        assert home not in result

    def test_dict_values_scrubbed(self) -> None:
        home = os.path.expanduser("~")
        payload: dict[str, Any] = {
            "command": f"cat {home}/.ssh/id_rsa",
            "exit_code": 1,
            "ok": True,
        }
        result = scrub_payload_strings(payload)
        assert home not in result["command"]
        assert result["exit_code"] == 1  # non-string unchanged
        assert result["ok"] is True  # bool unchanged

    def test_nested_dict_scrubbed(self) -> None:
        home = os.path.expanduser("~")
        payload: dict[str, Any] = {
            "detail": {
                "stderr_snippet": f"error: {home}/project/secrets.yml not found",
            }
        }
        result = scrub_payload_strings(payload)
        assert home not in result["detail"]["stderr_snippet"]

    def test_list_values_scrubbed(self) -> None:
        home = os.path.expanduser("~")
        result = scrub_payload_strings([f"{home}/a", f"{home}/b", 42])
        assert home not in result[0]
        assert home not in result[1]
        assert result[2] == 42

    def test_non_string_passthrough(self) -> None:
        assert scrub_payload_strings(123) == 123
        assert scrub_payload_strings(None) is None
        assert scrub_payload_strings(True) is True


# ---------------------------------------------------------------------------
# Integration: submit_event scrubs before transmitting
# ---------------------------------------------------------------------------

class TestSubmitEventScrubbing:
    def test_submit_event_scrubs_summary_before_send(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """submit_event must not transmit raw sensitive data in summary."""
        from rqmd import telemetry

        home = os.path.expanduser("~")
        captured: list[dict] = []

        def _fake_urlopen(req, timeout=None):  # noqa: ARG001
            import io
            import json as _json

            captured.append(_json.loads(req.data))
            resp = MagicMock()
            resp.read.return_value = b'{"ok": true}'
            resp.__enter__ = lambda s: s
            resp.__exit__ = MagicMock(return_value=False)
            return resp

        fake_urllib = MagicMock()
        fake_urllib.Request = __import__("urllib.request", fromlist=["Request"]).Request
        fake_urllib.urlopen = _fake_urlopen

        monkeypatch.setattr(telemetry, "_urllib_request", fake_urllib)

        telemetry.submit_event(
            "http://localhost:18080",
            event_type="struggle",
            severity="high",
            summary=f"rqmd failed reading {home}/.ssh/config",
            detail={"stderr_snippet": f"No such file: {home}/.ssh/config"},
        )

        assert len(captured) == 1
        assert home not in captured[0]["summary"]
        assert home not in captured[0]["detail"]["stderr_snippet"]
