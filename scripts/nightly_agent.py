"""Nightly agent — automated maintenance for mcp-compliance-grc."""

from __future__ import annotations

import json
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

REPO_ROOT = Path(__file__).parent.parent


def update_framework_manifest() -> None:
    """Write a manifest of all supported frameworks and controls."""
    from mcpgrc.frameworks.registry import FRAMEWORK_REGISTRY
    manifest = {
        "generated_at": datetime.utcnow().isoformat(),
        "date": date.today().isoformat(),
        "frameworks": {
            name: {
                "control_count": len(controls),
                "controls": [{"id": c.id, "name": c.name, "category": c.category} for c in controls],
            }
            for name, controls in FRAMEWORK_REGISTRY.items()
        },
    }
    out = REPO_ROOT / "docs" / "framework-manifest.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2))
    print(f"[agent] Updated framework manifest -> {out}")


def self_assess() -> None:
    """Run a SOC2 self-assessment against this repo and save the report."""
    from mcpgrc.core.config import GRCConfig
    from mcpgrc.tools.controls import get_framework_summary
    config = GRCConfig(repo_path=str(REPO_ROOT), framework="soc2")
    summary = get_framework_summary(config, framework="soc2")
    out = REPO_ROOT / "docs" / "self-assessment.json"
    summary["generated_at"] = datetime.utcnow().isoformat()
    out.write_text(json.dumps(summary, indent=2))
    print(f"[agent] Self-assessment score: {summary.get('compliance_score', 0)}% -> {out}")


def refresh_changelog() -> None:
    changelog = REPO_ROOT / "CHANGELOG.md"
    if not changelog.exists():
        return
    today = date.today().isoformat()
    content = changelog.read_text()
    if today not in content:
        content = content.replace("## [Unreleased]", f"## [Unreleased]\n\n_Last checked: {today}_", 1)
        changelog.write_text(content)
    print("[agent] Refreshed CHANGELOG timestamp")


if __name__ == "__main__":
    print(f"[agent] Starting nightly agent - {date.today().isoformat()}")
    update_framework_manifest()
    self_assess()
    refresh_changelog()
    print("[agent] Done.")