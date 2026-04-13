"""MCP tools for control listing and evidence mapping."""

from __future__ import annotations

from pathlib import Path
from mcpgrc.core.config import GRCConfig
from mcpgrc.core.evidence import map_control_to_evidence
from mcpgrc.frameworks.registry import get_framework_controls, get_control_by_id, list_frameworks


def list_controls(config: GRCConfig, framework: str = "") -> dict:
    """List all controls for a given compliance framework."""
    fw = framework or config.framework
    controls = get_framework_controls(fw)

    if not controls:
        return {
            "error": f"Unknown framework: {fw}",
            "supported_frameworks": list_frameworks(),
        }

    return {
        "framework": fw,
        "control_count": len(controls),
        "controls": [
            {
                "id": c.id,
                "name": c.name,
                "category": c.category,
                "description": c.description[:150] + "..." if len(c.description) > 150 else c.description,
            }
            for c in controls
        ],
    }


def map_control_to_evidence_tool(
    config: GRCConfig,
    control_id: str,
    framework: str = "",
) -> dict:
    """Find code evidence for a specific control in the repository."""
    fw = framework or config.framework
    control = get_control_by_id(fw, control_id)

    if not control:
        return {
            "error": f"Control {control_id} not found in framework {fw}",
            "framework": fw,
        }

    repo_path = Path(config.repo_path)
    evidence = map_control_to_evidence(control, repo_path, max_files=config.max_evidence_files)

    return {
        "framework": fw,
        "control_id": control_id,
        "control_name": control.name,
        "status": evidence.status,
        "evidence_count": evidence.evidence_count,
        "matches": [
            {
                "file": m.file_path,
                "line": m.line_number,
                "snippet": m.snippet[:150],
                "relevance": m.relevance,
            }
            for m in evidence.matches[:20]
        ],
    }


def get_control_status(config: GRCConfig, control_id: str, framework: str = "") -> dict:
    """Get pass/fail status of a specific control."""
    fw = framework or config.framework
    control = get_control_by_id(fw, control_id)

    if not control:
        return {"error": f"Control {control_id} not found in framework {fw}"}

    repo_path = Path(config.repo_path)
    evidence = map_control_to_evidence(control, repo_path, max_files=config.max_evidence_files)

    return {
        "framework": fw,
        "control_id": control_id,
        "control_name": control.name,
        "category": control.category,
        "status": evidence.status,
        "evidence_count": evidence.evidence_count,
        "passing": evidence.status == "sufficient",
    }


def get_framework_summary(config: GRCConfig, framework: str = "") -> dict:
    """Get compliance posture summary across all controls in a framework."""
    fw = framework or config.framework
    controls = get_framework_controls(fw)

    if not controls:
        return {"error": f"Unknown framework: {fw}"}

    repo_path = Path(config.repo_path)
    results = []
    for control in controls:
        evidence = map_control_to_evidence(control, repo_path, max_files=20)
        results.append({"id": control.id, "name": control.name, "status": evidence.status})

    sufficient = sum(1 for r in results if r["status"] == "sufficient")
    partial = sum(1 for r in results if r["status"] == "partial")
    insufficient = sum(1 for r in results if r["status"] == "insufficient")
    score = int((sufficient + partial * 0.5) / len(results) * 100) if results else 0

    return {
        "framework": fw,
        "total_controls": len(results),
        "sufficient": sufficient,
        "partial": partial,
        "insufficient": insufficient,
        "compliance_score": score,
        "controls": results,
    }


def list_open_findings(config: GRCConfig, framework: str = "") -> dict:
    """List controls with insufficient or partial evidence."""
    fw = framework or config.framework
    controls = get_framework_controls(fw)

    if not controls:
        return {"error": f"Unknown framework: {fw}"}

    repo_path = Path(config.repo_path)
    findings = []
    for control in controls:
        evidence = map_control_to_evidence(control, repo_path, max_files=20)
        if evidence.status in ("insufficient", "partial"):
            findings.append({
                "control_id": control.id,
                "control_name": control.name,
                "category": control.category,
                "status": evidence.status,
                "evidence_count": evidence.evidence_count,
                "keywords_to_implement": control.keywords[:3],
            })

    return {
        "framework": fw,
        "open_findings": len(findings),
        "findings": findings,
    }