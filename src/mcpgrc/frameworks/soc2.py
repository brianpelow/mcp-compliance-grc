"""SOC 2 Type II control definitions."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Control:
    """A compliance control definition."""

    id: str
    name: str
    description: str
    category: str
    evidence_patterns: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)


SOC2_CONTROLS: list[Control] = [
    Control(
        id="CC6.1",
        name="Logical and Physical Access Controls",
        description="The entity implements logical access security measures to protect against threats from sources outside its system boundaries.",
        category="Common Criteria",
        evidence_patterns=["auth", "authentication", "authorization", "rbac", "iam", "oauth", "jwt"],
        keywords=["access control", "authentication", "authorization", "MFA", "SSO"],
    ),
    Control(
        id="CC6.2",
        name="New Internal Personnel Access",
        description="Prior to issuing system credentials, the entity registers and authorizes new internal users.",
        category="Common Criteria",
        evidence_patterns=["user", "onboard", "provision", "role", "permission"],
        keywords=["user provisioning", "access request", "role assignment"],
    ),
    Control(
        id="CC6.3",
        name="Access Removal",
        description="The entity removes access to protected information when appropriate.",
        category="Common Criteria",
        evidence_patterns=["deprovision", "offboard", "revoke", "deactivate", "remove_user"],
        keywords=["access revocation", "offboarding", "deprovisioning"],
    ),
    Control(
        id="CC7.1",
        name="System Monitoring",
        description="The entity uses detection and monitoring procedures to identify changes to configurations that result in the introduction of new vulnerabilities.",
        category="Common Criteria",
        evidence_patterns=["monitor", "alert", "logging", "audit_log", "siem", "dynatrace", "datadog"],
        keywords=["monitoring", "alerting", "logging", "SIEM", "observability"],
    ),
    Control(
        id="CC7.2",
        name="Monitoring of System Components",
        description="The entity monitors system components and the operation of those controls.",
        category="Common Criteria",
        evidence_patterns=["health", "metric", "dashboard", "prometheus", "grafana", "dynatrace"],
        keywords=["system monitoring", "health checks", "metrics", "dashboards"],
    ),
    Control(
        id="CC8.1",
        name="Change Management",
        description="The entity authorizes, designs, develops or acquires, configures, documents, tests, approves, and implements changes to infrastructure, data, software, and procedures.",
        category="Common Criteria",
        evidence_patterns=["pull_request", "review", "approval", "deploy", "ci", "cd", "pipeline"],
        keywords=["change management", "code review", "deployment", "CI/CD", "approval"],
    ),
    Control(
        id="A1.1",
        name="Availability — Capacity Planning",
        description="The entity maintains, monitors, and evaluates current processing capacity.",
        category="Availability",
        evidence_patterns=["capacity", "scaling", "autoscale", "load", "resource"],
        keywords=["capacity planning", "auto-scaling", "load testing", "resource limits"],
    ),
    Control(
        id="PI1.1",
        name="Processing Integrity",
        description="The entity obtains or generates information about changes to inputs, processing, and outputs.",
        category="Processing Integrity",
        evidence_patterns=["validation", "integrity", "checksum", "audit", "reconcil"],
        keywords=["data validation", "processing integrity", "reconciliation", "checksums"],
    ),
]


def get_control(control_id: str) -> Control | None:
    return next((c for c in SOC2_CONTROLS if c.id == control_id), None)


def list_controls() -> list[Control]:
    return SOC2_CONTROLS