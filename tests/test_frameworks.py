"""Tests for compliance framework definitions."""

from mcpgrc.frameworks.soc2 import list_controls as soc2_controls, get_control as get_soc2
from mcpgrc.frameworks.iso27001 import list_controls as iso27001_controls, get_control as get_iso
from mcpgrc.frameworks.pcidss import list_controls as pcidss_controls, get_control as get_pci
from mcpgrc.frameworks.registry import get_framework_controls, get_control_by_id, list_frameworks


def test_soc2_controls_not_empty() -> None:
    assert len(soc2_controls()) >= 5


def test_iso27001_controls_not_empty() -> None:
    assert len(iso27001_controls()) >= 3


def test_pcidss_controls_not_empty() -> None:
    assert len(pcidss_controls()) >= 3


def test_soc2_control_has_evidence_patterns() -> None:
    for c in soc2_controls():
        assert len(c.evidence_patterns) > 0, f"{c.id} missing evidence patterns"


def test_get_soc2_control_by_id() -> None:
    control = get_soc2("CC6.1")
    assert control is not None
    assert control.name == "Logical and Physical Access Controls"


def test_get_iso_control_by_id() -> None:
    control = get_iso("A.12.4")
    assert control is not None
    assert "Logging" in control.name


def test_get_pci_control_by_id() -> None:
    control = get_pci("PCI-10.2")
    assert control is not None
    assert "Audit" in control.name


def test_registry_list_frameworks() -> None:
    frameworks = list_frameworks()
    assert "soc2" in frameworks
    assert "iso27001" in frameworks
    assert "pcidss" in frameworks


def test_registry_get_control_by_id() -> None:
    control = get_control_by_id("soc2", "CC8.1")
    assert control is not None
    assert "Change" in control.name


def test_registry_unknown_framework() -> None:
    controls = get_framework_controls("unknown")
    assert controls == []