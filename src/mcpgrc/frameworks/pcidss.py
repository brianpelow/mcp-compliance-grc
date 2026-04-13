"""PCI-DSS v4 control definitions."""

from __future__ import annotations

from mcpgrc.frameworks.soc2 import Control

PCIDSS_CONTROLS: list[Control] = [
    Control(
        id="PCI-6.3",
        name="Security Vulnerabilities Are Identified and Addressed",
        description="Security vulnerabilities are identified and protected against via security patch management.",
        category="Develop and Maintain Secure Systems",
        evidence_patterns=["vulnerability", "patch", "cve", "scan", "dependency", "sca"],
        keywords=["vulnerability management", "patching", "CVE", "SCA", "dependency scanning"],
    ),
    Control(
        id="PCI-6.4",
        name="Web-Facing Applications Are Protected",
        description="Web-facing applications are protected against attacks.",
        category="Develop and Maintain Secure Systems",
        evidence_patterns=["waf", "owasp", "injection", "xss", "csrf", "api_gateway"],
        keywords=["WAF", "OWASP", "injection prevention", "XSS", "CSRF", "API security"],
    ),
    Control(
        id="PCI-7.2",
        name="Access to System Components Is Managed",
        description="Access to system components and data is appropriately defined and assigned.",
        category="Restrict Access to System Components",
        evidence_patterns=["rbac", "iam", "role", "permission", "least_privilege", "access"],
        keywords=["least privilege", "RBAC", "IAM", "access management", "role-based access"],
    ),
    Control(
        id="PCI-10.2",
        name="Audit Logs Are Implemented",
        description="Audit logs are implemented to support the detection of anomalies and suspicious activity.",
        category="Log and Monitor All Access",
        evidence_patterns=["audit", "log", "event", "trail", "siem", "monitor"],
        keywords=["audit logging", "audit trail", "log management", "SIEM", "event logging"],
    ),
    Control(
        id="PCI-11.3",
        name="External and Internal Vulnerabilities Are Regularly Tested",
        description="External and internal vulnerabilities are regularly identified, prioritized, and addressed.",
        category="Test Security of Systems and Networks",
        evidence_patterns=["pentest", "scan", "vulnerability", "dast", "nessus", "qualys"],
        keywords=["penetration testing", "vulnerability scanning", "DAST", "security testing"],
    ),
    Control(
        id="PCI-12.10",
        name="Suspected and Confirmed Security Incidents Are Responded To",
        description="Suspected and confirmed security incidents that could impact the CDE are responded to immediately.",
        category="Support Information Security with Organizational Policies",
        evidence_patterns=["incident", "response", "pagerduty", "runbook", "escalation"],
        keywords=["incident response", "security incident", "escalation", "CDE", "PagerDuty"],
    ),
]


def get_control(control_id: str) -> Control | None:
    return next((c for c in PCIDSS_CONTROLS if c.id == control_id), None)


def list_controls() -> list[Control]:
    return PCIDSS_CONTROLS