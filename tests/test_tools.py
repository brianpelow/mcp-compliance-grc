"""Tests for GRC MCP tool functions."""

import tempfile
from pathlib import Path
from mcpgrc.core.config import GRCConfig
from mcpgrc.tools.controls import (
    list_controls,
    map_control_to_evidence_tool,
    get_control_status,
    get_framework_summary,
    list_open_findings,
)
from mcpgrc.tools.narrative import query_audit_trail_tool


def make_config(**kwargs) -> GRCConfig:
    return GRCConfig(**kwargs)


def test_list_controls_soc2() -> None:
    config = make_config()
    result = list_controls(config, framework="soc2")
    assert "controls" in result
    assert result["framework"] == "soc2"
    assert result["control_count"] >= 5


def test_list_controls_unknown_framework() -> None:
    config = make_config()
    result = list_controls(config, framework="unknown")
    assert "error" in result
    assert "supported_frameworks" in result


def test_map_control_to_evidence_tool() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        config = make_config(repo_path=tmpdir)
        result = map_control_to_evidence_tool(config, control_id="CC6.1", framework="soc2")
        assert "status" in result
        assert "evidence_count" in result


def test_get_control_status_known() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        config = make_config(repo_path=tmpdir)
        result = get_control_status(config, control_id="CC8.1", framework="soc2")
        assert "status" in result
        assert "passing" in result


def test_get_control_status_unknown() -> None:
    config = make_config()
    result = get_control_status(config, control_id="UNKNOWN-99")
    assert "error" in result


def test_get_framework_summary() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        config = make_config(repo_path=tmpdir, framework="soc2")
        result = get_framework_summary(config, framework="soc2")
        assert "compliance_score" in result
        assert "total_controls" in result
        assert result["total_controls"] >= 5


def test_list_open_findings() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        config = make_config(repo_path=tmpdir, framework="soc2")
        result = list_open_findings(config, framework="soc2")
        assert "findings" in result
        assert "open_findings" in result


def test_query_audit_trail_tool() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        config = make_config(repo_path=tmpdir)
        result = query_audit_trail_tool(config, since_days=30)
        assert "entries" in result
        assert "entry_count" in result
        assert result["source"] == "git"