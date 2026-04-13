"""Framework registry — maps framework names to control lists."""

from __future__ import annotations

from mcpgrc.frameworks.soc2 import Control
from mcpgrc.frameworks.soc2 import list_controls as soc2_controls
from mcpgrc.frameworks.iso27001 import list_controls as iso27001_controls
from mcpgrc.frameworks.pcidss import list_controls as pcidss_controls


FRAMEWORK_REGISTRY: dict[str, list[Control]] = {
    "soc2": soc2_controls(),
    "iso27001": iso27001_controls(),
    "pcidss": pcidss_controls(),
}


def get_framework_controls(framework: str) -> list[Control]:
    return FRAMEWORK_REGISTRY.get(framework.lower(), [])


def get_control_by_id(framework: str, control_id: str) -> Control | None:
    controls = get_framework_controls(framework)
    return next((c for c in controls if c.id == control_id), None)


def list_frameworks() -> list[str]:
    return list(FRAMEWORK_REGISTRY.keys())