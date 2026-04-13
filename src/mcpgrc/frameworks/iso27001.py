"""ISO 27001 control definitions."""

from __future__ import annotations

from mcpgrc.frameworks.soc2 import Control

ISO27001_CONTROLS: list[Control] = [
    Control(
        id="A.12.1",
        name="Operational Procedures and Responsibilities",
        description="Documented operating procedures shall be maintained and made available to all users who need them.",
        category="Operations Security",
        evidence_patterns=["runbook", "procedure", "sop", "playbook", "operational"],
        keywords=["runbooks", "SOPs", "operational procedures", "documentation"],
    ),
    Control(
        id="A.12.4",
        name="Logging and Monitoring",
        description="Event logs recording user activities, exceptions, faults and information security events shall be produced and kept.",
        category="Operations Security",
        evidence_patterns=["log", "audit", "event", "monitor", "siem", "splunk", "dynatrace"],
        keywords=["audit logging", "event logging", "log retention", "SIEM"],
    ),
    Control(
        id="A.14.2",
        name="Security in Development and Support Processes",
        description="Rules for the development of software and systems shall be established and applied.",
        category="System Acquisition",
        evidence_patterns=["sast", "sca", "security", "scan", "vulnerability", "review"],
        keywords=["secure SDLC", "security scanning", "SAST", "SCA", "code review"],
    ),
    Control(
        id="A.16.1",
        name="Management of Information Security Incidents",
        description="Responsibilities and procedures shall be established to ensure a quick, effective and orderly response to information security incidents.",
        category="Incident Management",
        evidence_patterns=["incident", "pagerduty", "response", "escalation", "postmortem"],
        keywords=["incident response", "escalation", "postmortem", "PagerDuty"],
    ),
    Control(
        id="A.17.1",
        name="Information Security Continuity",
        description="The continuity of information security shall be embedded in the business continuity management systems.",
        category="Business Continuity",
        evidence_patterns=["backup", "recovery", "rto", "rpo", "disaster", "continuity"],
        keywords=["business continuity", "disaster recovery", "RTO", "RPO", "backups"],
    ),
]


def get_control(control_id: str) -> Control | None:
    return next((c for c in ISO27001_CONTROLS if c.id == control_id), None)


def list_controls() -> list[Control]:
    return ISO27001_CONTROLS