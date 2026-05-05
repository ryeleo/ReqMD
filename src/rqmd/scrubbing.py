"""Client-side secrets and PII scrubbing for telemetry payloads.

Three-layer pipeline applied to every freeform string before transmission:
  Pre-pass : home-directory path normalisation (fast, no deps)
  Layer 1  : detect-secrets  — secret pattern detection and redaction
  Layer 2  : gitleaks stdin  — comprehensive ruleset (best-effort, optional subprocess)
  Layer 3  : scrubadub       — PII redaction (emails, names, addresses, phone numbers)

Any layer that raises an exception is skipped with a WARNING log; the pipeline
continues with the previous layer's output and never transmits raw data.
"""

from __future__ import annotations

import json
import logging
import os
import re
import shutil
import subprocess
from typing import Any

logger = logging.getLogger(__name__)

# Replacement placeholders
_PLACEHOLDER_PATH = "{{REDACTED_PATH}}"
_PLACEHOLDER_SECRET = "{{REDACTED_SECRET}}"
_PLACEHOLDER_GUID = "{{REDACTED_GUID}}"
_PLACEHOLDER_GITLEAKS = "{{REDACTED_GITLEAKS}}"

# One-time warning flag for absent gitleaks binary
_gitleaks_warning_emitted = False

# ---------------------------------------------------------------------------
# Infrastructure pattern regexes (pre-pass, no external deps)
# ---------------------------------------------------------------------------

# UUID / GUID (all versions — Azure subscription IDs, tenant IDs, client IDs, etc.)
_RE_UUID = re.compile(
    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
)

# SSH / PEM private key blocks (RSA, EC, OPENSSH, DSA — with optional header word)
_RE_PEM_PRIVATE_KEY = re.compile(
    r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----"
    r".*?"
    r"-----END (?:RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----",
    re.DOTALL,
)

# Azure storage account key embedded in a connection string: AccountKey=<base64>=
_RE_AZURE_ACCOUNT_KEY = re.compile(
    r"AccountKey=[A-Za-z0-9+/]{44,}={0,2}"
)

# Azure SAS token signature parameter: sig=<url-encoded base64>
_RE_AZURE_SAS_SIG = re.compile(
    r"(?<=[?&;])sig=[A-Za-z0-9%+/]{20,}(?:={0,2}|%3D{0,2})"
)

# 1Password service account tokens: ops_<base58-ish, 20+ chars>
_RE_1PASSWORD_SAT = re.compile(
    r"\bops_[A-Za-z0-9]{20,}\b"
)

# JWT tokens (1Password Connect, Azure AD bearer, GitHub Apps, etc.)
# Three base64url segments separated by dots; conservative min lengths.
_RE_JWT = re.compile(
    r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"
)

# GitHub token prefixes (supplement detect-secrets; catches all known prefix families)
# ghp_ = PAT, gho_ = OAuth, ghs_ = Actions/server, ghr_ = refresh, github_pat_ = fine-grained
_RE_GITHUB_TOKEN = re.compile(
    r"\b(?:ghp|gho|ghs|ghr|github_pat)_[A-Za-z0-9_]{20,}\b"
)

# AWS access key ID (AKIA / ABIA / ACCA / ASIA prefixes)
_RE_AWS_ACCESS_KEY = re.compile(
    r"\b(?:AKIA|ABIA|ACCA|ASIA)[A-Z0-9]{16}\b"
)

# AWS secret access key: 40-char base64-ish after known context keywords
_RE_AWS_SECRET_KEY = re.compile(
    r"(?:aws_secret_access_key|AWS_SECRET_ACCESS_KEY|SecretAccessKey)"
    r"\s*[=:]\s*['\"]?([A-Za-z0-9+/]{40})['\"]?"
)

# Azure client secret (common format: random ~34-char string after known keys)
_RE_AZURE_CLIENT_SECRET = re.compile(
    r"(?:client[_\-]?secret|AZURE_CLIENT_SECRET|clientSecret)"
    r"\s*[=:]\s*['\"]?([A-Za-z0-9~._\-]{20,})['\"]?"
)


# ---------------------------------------------------------------------------
# Pre-pass: home-directory path normalisation
# ---------------------------------------------------------------------------

def _scrub_home_paths(text: str) -> str:
    """Replace home-directory paths with a safe placeholder.

    Covers:
    - Exact expanded home dir prefix (e.g. /Users/alice or /home/alice)
    - Tilde shorthand (~/...)
    - Other users' home dirs matching /home/<user>/ or /Users/<user>/
    """
    # Expanded home dir for the current user — replace longest match first.
    home = os.path.expanduser("~")
    if home and home != "~":
        text = text.replace(home, _PLACEHOLDER_PATH)

    # ~/... shorthand
    text = re.sub(r"~/", _PLACEHOLDER_PATH + "/", text)

    # /home/<user>/... and /Users/<user>/... for any username
    text = re.sub(r"/(?:home|Users)/[^/\s\"']+/", _PLACEHOLDER_PATH + "/", text)

    return text


# ---------------------------------------------------------------------------
# Pre-pass 2: infrastructure-specific secret patterns (regex, no deps)
# ---------------------------------------------------------------------------

def _scrub_infra_patterns(text: str) -> str:
    """Redact infrastructure secrets using regex patterns.

    Catches patterns that PII scrubbers miss and that detect-secrets /
    gitleaks may not handle consistently:
    - UUIDs / GUIDs (Azure subscription, tenant, client IDs)
    - SSH / PEM private key blocks
    - Azure storage account keys, SAS signatures, client secrets
    - 1Password service account tokens and Connect JWTs
    - GitHub token families (ghp_, gho_, ghs_, ghr_, github_pat_)
    - AWS access key IDs and secret access keys
    """
    # PEM private key blocks (replace entire block including content)
    text = _RE_PEM_PRIVATE_KEY.sub(_PLACEHOLDER_SECRET, text)

    # AWS access key IDs (AKIA...)
    text = _RE_AWS_ACCESS_KEY.sub(_PLACEHOLDER_SECRET, text)

    # AWS secret access key (context-keyword-gated)
    text = _RE_AWS_SECRET_KEY.sub(
        lambda m: m.group(0).replace(m.group(1), _PLACEHOLDER_SECRET), text
    )

    # GitHub token families
    text = _RE_GITHUB_TOKEN.sub(_PLACEHOLDER_SECRET, text)

    # Azure storage account key in connection strings
    text = _RE_AZURE_ACCOUNT_KEY.sub("AccountKey=" + _PLACEHOLDER_SECRET, text)

    # Azure SAS signature parameter
    text = _RE_AZURE_SAS_SIG.sub("sig=" + _PLACEHOLDER_SECRET, text)

    # Azure client secret (context-keyword-gated)
    text = _RE_AZURE_CLIENT_SECRET.sub(
        lambda m: m.group(0).replace(m.group(1), _PLACEHOLDER_SECRET), text
    )

    # 1Password service account tokens
    text = _RE_1PASSWORD_SAT.sub(_PLACEHOLDER_SECRET, text)

    # JWT tokens (1Password Connect, Azure AD, GitHub Apps bearer tokens)
    text = _RE_JWT.sub(_PLACEHOLDER_SECRET, text)

    # UUIDs / GUIDs — redact last, after context-specific patterns above
    # have already consumed keys that contain GUIDs.
    text = _RE_UUID.sub(_PLACEHOLDER_GUID, text)

    return text


# ---------------------------------------------------------------------------
# Layer 1: detect-secrets
# ---------------------------------------------------------------------------

# Minimum secret length for detect-secrets redaction.
# High-entropy string detectors can flag short tokens as secrets, producing
# false positives on normal CLI output.  Real secrets (API keys, tokens) are
# always at least this many characters.
_MIN_SECRET_LENGTH = 20


def _scrub_layer_detect_secrets(text: str) -> str:
    """Scan for secret patterns using detect-secrets and replace matches."""
    try:
        from detect_secrets.core.scan import \
            scan_line as _ds_scan_line  # type: ignore[import-untyped]
        from detect_secrets.settings import \
            default_settings  # type: ignore[import-untyped]
    except ImportError:
        logger.warning(
            "rqmd-scrubbing: detect-secrets not importable, skipping layer 1"
        )
        return text

    try:
        result = text
        with default_settings():
            for line in text.splitlines():
                for secret in _ds_scan_line(line):
                    sv = getattr(secret, "secret_value", None)
                    if (
                        sv
                        and isinstance(sv, str)
                        and len(sv) >= _MIN_SECRET_LENGTH
                        and sv in result
                    ):
                        result = result.replace(sv, _PLACEHOLDER_SECRET)
        return result
    except Exception:
        logger.warning(
            "rqmd-scrubbing: detect-secrets layer raised an exception, skipping",
            exc_info=True,
        )
        return text


# ---------------------------------------------------------------------------
# Layer 2: gitleaks subprocess (best-effort, optional)
# ---------------------------------------------------------------------------

def _scrub_layer_gitleaks(text: str) -> str:
    """Run gitleaks stdin against the text and replace reported secrets."""
    global _gitleaks_warning_emitted

    if not shutil.which("gitleaks"):
        if not _gitleaks_warning_emitted:
            logger.debug(
                "rqmd-scrubbing: gitleaks not found in PATH, skipping layer 2 "
                "(install gitleaks for enhanced secret detection)"
            )
            _gitleaks_warning_emitted = True
        return text

    try:
        proc = subprocess.run(
            [
                "gitleaks",
                "stdin",
                "--report-format", "json",
                "--report-path", "-",
                "--no-banner",
            ],
            input=text,
            capture_output=True,
            text=True,
            timeout=15,
        )
        # exit 0 = no findings; exit 1 = findings found; anything else = error
        if proc.returncode not in (0, 1):
            logger.warning(
                "rqmd-scrubbing: gitleaks exited %d, skipping layer 2",
                proc.returncode,
            )
            return text

        raw = proc.stdout.strip()
        if not raw or raw in ("null", "[]"):
            return text

        findings = json.loads(raw)
        if not isinstance(findings, list):
            return text

        result = text
        for finding in findings:
            secret_val = finding.get("Secret") or finding.get("secret")
            if secret_val and isinstance(secret_val, str) and secret_val in result:
                result = result.replace(secret_val, _PLACEHOLDER_GITLEAKS)
        return result

    except subprocess.TimeoutExpired:
        logger.warning("rqmd-scrubbing: gitleaks timed out, skipping layer 2")
        return text
    except Exception:
        logger.warning(
            "rqmd-scrubbing: gitleaks layer raised an exception, skipping",
            exc_info=True,
        )
        return text


# ---------------------------------------------------------------------------
# Layer 3: scrubadub (PII redaction)
# ---------------------------------------------------------------------------

def _scrub_layer_scrubadub(text: str) -> str:
    """Redact PII using scrubadub (emails, names, addresses, phone numbers)."""
    try:
        import scrubadub  # type: ignore[import-untyped]
    except ImportError:
        logger.warning(
            "rqmd-scrubbing: scrubadub not importable, skipping layer 3"
        )
        return text

    try:
        scrubber = scrubadub.Scrubber()
        return scrubber.clean(text)
    except Exception:
        logger.warning(
            "rqmd-scrubbing: scrubadub layer raised an exception, skipping",
            exc_info=True,
        )
        return text


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

def scrub_text(text: str) -> str:
    """Run a string through the full three-layer scrubbing pipeline.

    Pre-pass (home-path normalisation and infrastructure patterns) runs first
    and is not guarded — it has no external deps and should never fail.

    Each of the three pipeline layers is wrapped in a per-layer guard:
    if a layer raises for any reason, it is skipped with a WARNING and
    the pipeline continues.  This function never raises.
    """
    text = _scrub_home_paths(text)
    text = _scrub_infra_patterns(text)

    for _layer, _name in (
        (_scrub_layer_detect_secrets, "detect-secrets"),
        (_scrub_layer_gitleaks, "gitleaks"),
        (_scrub_layer_scrubadub, "scrubadub"),
    ):
        try:
            text = _layer(text)
        except Exception:
            logger.warning(
                "rqmd-scrubbing: layer %s raised unexpectedly, skipping",
                _name,
                exc_info=True,
            )

    return text


def scrub_payload_strings(obj: Any) -> Any:
    """Recursively scrub all string values in a nested dict / list / str.

    Non-string leaf values (int, bool, None, etc.) are returned unchanged.
    """
    if isinstance(obj, str):
        return scrub_text(obj)
    if isinstance(obj, dict):
        return {k: scrub_payload_strings(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [scrub_payload_strings(item) for item in obj]
    return obj
