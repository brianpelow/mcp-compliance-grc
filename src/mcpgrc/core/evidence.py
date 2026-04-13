"""Control-to-code evidence mapper."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from mcpgrc.frameworks.soc2 import Control


@dataclass
class EvidenceMatch:
    """A piece of code evidence matching a control."""

    file_path: str
    line_number: int
    snippet: str
    match_type: str
    relevance: str = "medium"


@dataclass
class ControlEvidence:
    """Evidence collected for a single control."""

    control_id: str
    control_name: str
    matches: list[EvidenceMatch] = field(default_factory=list)
    status: str = "insufficient"

    @property
    def has_evidence(self) -> bool:
        return len(self.matches) > 0

    @property
    def evidence_count(self) -> int:
        return len(self.matches)


def map_control_to_evidence(
    control: Control,
    repo_path: Path,
    max_files: int = 50,
) -> ControlEvidence:
    """Scan a repository for evidence matching a control."""
    evidence = ControlEvidence(
        control_id=control.id,
        control_name=control.name,
    )

    if not repo_path.exists():
        return evidence

    extensions = {".py", ".ts", ".js", ".go", ".java", ".yaml", ".yml", ".tf", ".md"}
    files = [
        f for f in repo_path.rglob("*")
        if f.is_file()
        and f.suffix in extensions
        and ".git" not in f.parts
        and ".venv" not in f.parts
    ][:max_files]

    for file_path in files:
        try:
            text = file_path.read_text(errors="ignore")
            lines = text.splitlines()
            for i, line in enumerate(lines, 1):
                line_lower = line.lower()
                for pattern in control.evidence_patterns:
                    if pattern.lower() in line_lower:
                        evidence.matches.append(EvidenceMatch(
                            file_path=str(file_path.relative_to(repo_path)),
                            line_number=i,
                            snippet=line.strip()[:200],
                            match_type="pattern",
                            relevance="high" if any(kw.lower() in line_lower for kw in control.keywords) else "medium",
                        ))
                        break
        except Exception:
            pass

    if evidence.evidence_count >= 3:
        evidence.status = "sufficient"
    elif evidence.evidence_count >= 1:
        evidence.status = "partial"
    else:
        evidence.status = "insufficient"

    return evidence