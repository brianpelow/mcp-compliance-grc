"""FastMCP server entry point for mcp-compliance-grc."""

from __future__ import annotations

import json
from mcpgrc.core.config import GRCConfig
from mcpgrc.tools.controls import (
    list_controls,
    map_control_to_evidence_tool,
    get_control_status,
    get_framework_summary,
    list_open_findings,
)
from mcpgrc.tools.narrative import draft_narrative_tool, query_audit_trail_tool


def create_server() -> object:
    """Create and configure the FastMCP server."""
    try:
        from fastmcp import FastMCP
    except ImportError:
        raise ImportError("fastmcp is required. Run: pip install fastmcp")

    config = GRCConfig.from_env()
    mcp = FastMCP(
        name="mcp-compliance-grc",
        instructions=(
            "I provide GRC (Governance, Risk, and Compliance) intelligence by mapping "
            "compliance controls from SOC 2, ISO 27001, and PCI-DSS to actual code evidence. "
            "I can assess control status, draft audit narratives, query audit trails, "
            "and identify open compliance findings."
        ),
    )

    @mcp.tool()
    def list_controls_tool(framework: str = "") -> str:
        """List all controls for a compliance framework (soc2, iso27001, pcidss)."""
        return json.dumps(list_controls(config, framework=framework), indent=2)

    @mcp.tool()
    def map_control_to_evidence(control_id: str, framework: str = "") -> str:
        """Find code evidence for a specific control in the repository."""
        return json.dumps(map_control_to_evidence_tool(config, control_id=control_id, framework=framework), indent=2)

    @mcp.tool()
    def get_control_status(control_id: str, framework: str = "") -> str:
        """Get pass/fail status of a specific control."""
        from mcpgrc.tools.controls import get_control_status as _get
        return json.dumps(_get(config, control_id=control_id, framework=framework), indent=2)

    @mcp.tool()
    def draft_compliance_narrative(control_id: str, framework: str = "") -> str:
        """AI-draft a compliance narrative for an audit finding."""
        return json.dumps(draft_narrative_tool(config, control_id=control_id, framework=framework), indent=2)

    @mcp.tool()
    def query_audit_trail(since_days: int = 90, author: str = "", path_filter: str = "") -> str:
        """Query git history as a compliance audit trail."""
        return json.dumps(query_audit_trail_tool(config, since_days=since_days, author=author, path_filter=path_filter), indent=2)

    @mcp.tool()
    def get_framework_summary(framework: str = "") -> str:
        """Get compliance posture summary across all controls in a framework."""
        from mcpgrc.tools.controls import get_framework_summary as _get
        return json.dumps(_get(config, framework=framework), indent=2)

    @mcp.tool()
    def list_open_findings(framework: str = "") -> str:
        """List controls with insufficient or partial evidence."""
        from mcpgrc.tools.controls import list_open_findings as _list
        return json.dumps(_list(config, framework=framework), indent=2)

    return mcp


def main() -> None:
    """Entry point for the MCP server."""
    mcp = create_server()
    mcp.run()


if __name__ == "__main__":
    main()