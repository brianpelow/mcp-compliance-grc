"""AI-powered compliance narrative generator."""

from __future__ import annotations

import os
from mcpgrc.core.evidence import ControlEvidence
from mcpgrc.frameworks.soc2 import Control


def draft_compliance_narrative(
    control: Control,
    evidence: ControlEvidence,
    framework: str = "soc2",
    industry: str = "fintech",
) -> str:
    """Draft a compliance narrative for an audit finding using Claude."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return _fallback_narrative(control, evidence, framework)

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)

        evidence_summary = "\n".join(
            f"- {m.file_path}:{m.line_number} — {m.snippet[:100]}"
            for m in evidence.matches[:10]
        ) or "No evidence found."

        prompt = f"""You are a compliance officer writing audit narratives for a {industry} engineering team.

Draft a compliance narrative for the following control:

Framework: {framework.upper()}
Control ID: {control.id}
Control Name: {control.name}
Control Description: {control.description}
Evidence Status: {evidence.status}
Evidence Count: {evidence.evidence_count} items found

Code Evidence:
{evidence_summary}

Write a 2-3 paragraph compliance narrative that:
1. States whether the control is satisfied, partially satisfied, or not satisfied
2. Describes the evidence found (or lack thereof) in specific technical terms
3. Recommends remediation steps if evidence is insufficient
4. Uses language appropriate for an external auditor

Be specific, factual, and professional. No filler."""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=600,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text

    except Exception:
        return _fallback_narrative(control, evidence, framework)


def _fallback_narrative(control: Control, evidence: ControlEvidence, framework: str) -> str:
    status_text = {
        "sufficient": "satisfied",
        "partial": "partially satisfied",
        "insufficient": "not satisfied",
    }.get(evidence.status, "unknown")

    return f"""## {framework.upper()} Control {control.id} — {control.name}

**Status**: {status_text.title()}

The assessment of control {control.id} ({control.name}) identified {evidence.evidence_count} piece(s) of evidence across the reviewed codebase. The control is currently **{status_text}**.

{"Evidence was found in the following locations: " + ", ".join(f"{m.file_path}" for m in evidence.matches[:5]) if evidence.has_evidence else "No evidence was identified for this control in the scanned repository."}

**Recommendation**: {"Continue to maintain existing controls and ensure evidence is kept current." if evidence.status == "sufficient" else "Implement additional controls and ensure evidence is documented and accessible for audit review."}
"""