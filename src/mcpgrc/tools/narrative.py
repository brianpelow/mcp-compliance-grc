"""MCP tools for compliance narrative generation and audit trail."""

from __future__ import annotations

from pathlib import Path
from mcpgrc.core.config import GRCConfig
from mcpgrc.core.evidence import map_control_to_evidence
from mcpgrc.core.narrator import draft_compliance_narrative
from mcpgrc.core.audit_trail import query_audit_trail
from mcpgrc.frameworks.registry import get_control_by_id


def draft_narrative_tool(
    config: GRCConfig,
    control_id: str,
    framework: str = "",
) -> dict:
    """AI-draft a compliance narrative for a control finding."""
    fw = framework or config.framework
    control = get_control_by_id(fw, control_id)

    if not control:
        return {"error": f"Control {control_id} not found in framework {fw}"}

    repo_path = Path(config.repo_path)
    evidence = map_control_to_evidence(control, repo_path)
    narrative = draft_compliance_narrative(control, evidence, framework=fw, industry=config.industry)

    return {
        "framework": fw,
        "control_id": control_id,
        "control_name": control.name,
        "evidence_status": evidence.status,
        "narrative": narrative,
    }


def query_audit_trail_tool(
    config: GRCConfig,
    since_days: int = 90,
    author: str = "",
    path_filter: str = "",
) -> dict:
    """Query git history as a compliance audit trail."""
    repo_path = Path(config.repo_path)
    entries = query_audit_trail(
        repo_path,
        since_days=since_days,
        author=author,
        path_filter=path_filter,
    )

    return {
        "source": "git",
        "since_days": since_days,
        "entry_count": len(entries),
        "entries": [
            {
                "hash": e.commit_hash,
                "author": e.author,
                "email": e.email,
                "date": e.date,
                "message": e.message,
                "files_changed": e.files_changed,
            }
            for e in entries
        ],
    }