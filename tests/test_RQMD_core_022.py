"""Tests for RQMD-CORE-022: Enhanced blocking with linked requirements."""

from pathlib import Path

import pytest

from rqmd.req_parser import extract_blocking_id


class TestExtractBlockingId:
    def test_returns_none_for_none(self):
        assert extract_blocking_id(None) is None

    def test_returns_none_for_empty(self):
        assert extract_blocking_id("") is None

    def test_bare_id_in_text(self):
        assert (
            extract_blocking_id("Waiting on RQMD-CORE-001 to land") == "RQMD-CORE-001"
        )

    def test_bare_id_case_normalized(self):
        result = extract_blocking_id("blocked by rqmd-core-001")
        # lowercase won't match the uppercase pattern
        assert result is None  # IDs are uppercase only

    def test_markdown_link_label_is_req_id(self):
        reason = "See [RQMD-CORE-005](../core-engine.md#rqmd-core-005) for context"
        result = extract_blocking_id(reason)
        assert result == "RQMD-CORE-005"

    def test_markdown_link_preferred_over_bare(self):
        reason = "[RQMD-CORE-005](../core.md) also related to RQMD-CORE-009"
        result = extract_blocking_id(reason)
        assert result == "RQMD-CORE-005"

    def test_first_bare_id_returned(self):
        reason = "depends on RQMD-CORE-003 and RQMD-CORE-007"
        result = extract_blocking_id(reason)
        assert result == "RQMD-CORE-003"

    def test_prefix_filter_respected(self):
        reason = "blocked by AC-001"
        result = extract_blocking_id(reason, id_prefixes=("RQMD",))
        assert result is None

    def test_prefix_filter_matches(self):
        reason = "blocked by RQMD-CORE-001"
        result = extract_blocking_id(reason, id_prefixes=("RQMD",))
        assert result == "RQMD-CORE-001"

    def test_free_form_text_with_no_id(self):
        assert extract_blocking_id("waiting on design review") is None

    def test_req_id_at_start_of_string(self):
        assert extract_blocking_id("RQMD-PRIO-001 must ship first") == "RQMD-PRIO-001"

    def test_default_id_prefixes_used(self):
        # AC, R, RQMD are defaults
        assert extract_blocking_id("waiting for AC-001") == "AC-001"
        assert extract_blocking_id("waiting for R-001") == "R-001"

    def test_custom_prefix_registered(self):
        result = extract_blocking_id("waiting for MYPROJ-007", id_prefixes=("MYPROJ",))
        assert result == "MYPROJ-007"
