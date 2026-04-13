"""Configuration for mcp-compliance-grc."""

from __future__ import annotations

import os
from pydantic import BaseModel, Field

SUPPORTED_FRAMEWORKS = ["soc2", "iso27001", "pcidss"]


class GRCConfig(BaseModel):
    """Runtime configuration for the GRC MCP server."""

    framework: str = Field("soc2", description="Default compliance framework")
    repo_path: str = Field(".", description="Path to repository to audit")
    industry: str = Field("fintech", description="Industry context")
    timeout_seconds: int = Field(30, description="HTTP client timeout")
    max_evidence_files: int = Field(50, description="Max files to scan for evidence")

    @classmethod
    def from_env(cls) -> "GRCConfig":
        return cls(
            framework=os.environ.get("GRC_FRAMEWORK", "soc2"),
            repo_path=os.environ.get("GRC_REPO_PATH", "."),
            industry=os.environ.get("GRC_INDUSTRY", "fintech"),
        )

    @property
    def is_valid_framework(self) -> bool:
        return self.framework in SUPPORTED_FRAMEWORKS