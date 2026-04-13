"""Tests for GRCConfig."""

from mcpgrc.core.config import GRCConfig, SUPPORTED_FRAMEWORKS


def test_config_defaults() -> None:
    config = GRCConfig()
    assert config.framework == "soc2"
    assert config.repo_path == "."
    assert config.industry == "fintech"
    assert config.timeout_seconds == 30


def test_config_custom() -> None:
    config = GRCConfig(framework="iso27001", industry="manufacturing")
    assert config.framework == "iso27001"
    assert config.industry == "manufacturing"


def test_supported_frameworks() -> None:
    assert "soc2" in SUPPORTED_FRAMEWORKS
    assert "iso27001" in SUPPORTED_FRAMEWORKS
    assert "pcidss" in SUPPORTED_FRAMEWORKS


def test_is_valid_framework_true() -> None:
    config = GRCConfig(framework="soc2")
    assert config.is_valid_framework is True


def test_is_valid_framework_false() -> None:
    config = GRCConfig(framework="unknown")
    assert config.is_valid_framework is False