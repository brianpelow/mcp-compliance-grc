"""Tests for control evidence mapping."""

import tempfile
from pathlib import Path
from mcpgrc.frameworks.soc2 import get_control
from mcpgrc.core.evidence import map_control_to_evidence, ControlEvidence


def test_evidence_insufficient_on_empty_repo() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        control = get_control("CC6.1")
        assert control is not None
        evidence = map_control_to_evidence(control, Path(tmpdir))
        assert evidence.status == "insufficient"
        assert evidence.evidence_count == 0


def test_evidence_found_in_repo() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        (path / "auth.py").write_text(
            "from oauth import authenticate\n"
            "def login(user): return jwt.encode(rbac.get_roles(user))\n"
        )
        control = get_control("CC6.1")
        assert control is not None
        evidence = map_control_to_evidence(control, path)
        assert evidence.evidence_count > 0
        assert evidence.status in ("sufficient", "partial")


def test_evidence_nonexistent_path() -> None:
    control = get_control("CC7.1")
    assert control is not None
    evidence = map_control_to_evidence(control, Path("/nonexistent/path"))
    assert evidence.status == "insufficient"


def test_control_evidence_has_evidence_property() -> None:
    ev = ControlEvidence(control_id="CC6.1", control_name="Test")
    assert ev.has_evidence is False
    assert ev.evidence_count == 0