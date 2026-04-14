"""Tests for RQMD-PRIORITY-012: Domain and sub-domain priority metadata."""

from pathlib import Path

from rqmd.req_parser import parse_domain_priority_metadata


class TestParseDomainPriorityMetadata:
    def test_no_priority_in_empty_file(self, tmp_path: Path):
        f = tmp_path / "domain.md"
        f.write_text("# Domain\n\n### RQMD-DOM-001: First\n- **Status:** 💡 Proposed\n")
        result = parse_domain_priority_metadata(f)
        assert result["domain_priority"] is None
        assert result["sub_section_priorities"] == {}

    def test_domain_priority_in_preamble(self, tmp_path: Path):
        f = tmp_path / "domain.md"
        f.write_text(
            "# Domain\n"
            "- **Priority:** 🟠 P1 - High\n\n"
            "### RQMD-DOM-001: First\n"
            "- **Status:** 💡 Proposed\n"
        )
        result = parse_domain_priority_metadata(f)
        assert result["domain_priority"] == "🟠 P1 - High"

    def test_subsection_priority(self, tmp_path: Path):
        f = tmp_path / "domain.md"
        f.write_text(
            "# Domain\n\n"
            "## API Subsection\n"
            "- **Priority:** 🟡 P2 - Medium\n\n"
            "### RQMD-DOM-001: First\n"
            "- **Status:** 💡 Proposed\n"
        )
        result = parse_domain_priority_metadata(f)
        assert result["domain_priority"] is None
        assert (
            result["sub_section_priorities"].get("API Subsection") == "🟡 P2 - Medium"
        )

    def test_domain_and_subsection_priorities(self, tmp_path: Path):
        f = tmp_path / "domain.md"
        f.write_text(
            "# Domain\n"
            "- **Priority:** 🔴 P0 - Critical\n\n"
            "## Front End\n"
            "- **Priority:** 🟠 P1 - High\n\n"
            "### RQMD-DOM-001: First\n"
            "- **Status:** 💡 Proposed\n\n"
            "## Backend\n"
            "### RQMD-DOM-002: Second\n"
            "- **Status:** 💡 Proposed\n"
        )
        result = parse_domain_priority_metadata(f)
        assert result["domain_priority"] == "🔴 P0 - Critical"
        assert result["sub_section_priorities"]["Front End"] == "🟠 P1 - High"
        assert result["sub_section_priorities"]["Backend"] is None

    def test_missing_file_returns_empty(self, tmp_path: Path):
        result = parse_domain_priority_metadata(tmp_path / "nonexistent.md")
        assert result["domain_priority"] is None
        assert result["sub_section_priorities"] == {}

    def test_no_priority_in_subsection(self, tmp_path: Path):
        f = tmp_path / "domain.md"
        f.write_text(
            "# Domain\n\n"
            "## Subsection\n\n"
            "### RQMD-DOM-001: First\n"
            "- **Status:** 💡 Proposed\n"
        )
        result = parse_domain_priority_metadata(f)
        assert result["sub_section_priorities"].get("Subsection") is None

    def test_multiple_subsections_each_tracked(self, tmp_path: Path):
        f = tmp_path / "domain.md"
        f.write_text(
            "# Domain\n\n"
            "## Alpha\n"
            "- **Priority:** 🟢 P3 - Low\n\n"
            "### RQMD-DOM-001: Req\n- **Status:** 💡 Proposed\n\n"
            "## Beta\n"
            "- **Priority:** 🔴 P0 - Critical\n\n"
            "### RQMD-DOM-002: Req\n- **Status:** 💡 Proposed\n"
        )
        result = parse_domain_priority_metadata(f)
        assert result["sub_section_priorities"]["Alpha"] == "🟢 P3 - Low"
        assert result["sub_section_priorities"]["Beta"] == "🔴 P0 - Critical"

