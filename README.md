# mcp-compliance-grc

> MCP server for GRC workflows — maps controls to code evidence and drafts compliance narratives.

![CI](https://github.com/brianpelow/mcp-compliance-grc/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.12+-green.svg)
![MCP](https://img.shields.io/badge/MCP-compatible-purple.svg)

## Overview

`mcp-compliance-grc` is a Model Context Protocol server that brings GRC
workflows into AI agent pipelines. It maps compliance controls from SOC 2,
ISO 27001, and PCI-DSS to actual code evidence in your repositories, queries
audit trails, and drafts compliance narratives using Claude.

Built for engineering and compliance teams in regulated financial services
and manufacturing where audit readiness is continuous, not quarterly.

## Tools exposed

| Tool | Description |
|------|-------------|
| `list_controls` | List all controls for a given framework |
| `map_control_to_evidence` | Find code evidence for a specific control |
| `get_control_status` | Assess pass/fail status of a control |
| `draft_compliance_narrative` | AI-draft a narrative for an audit finding |
| `query_audit_trail` | Query git history as an audit trail |
| `get_framework_summary` | Get compliance posture summary for a framework |
| `list_open_findings` | List controls with insufficient evidence |

## Quick start

```bash
pip install mcp-compliance-grc

export ANTHROPIC_API_KEY=your_key
export GRC_REPO_PATH=./your-service
export GRC_FRAMEWORK=soc2

mcp-compliance-grc
```

## Supported frameworks

| Framework | Controls | Industry |
|-----------|----------|----------|
| SOC 2 Type II | CC6, CC7, CC8, A1, PI1 | Fintech, SaaS |
| ISO 27001 | A.12, A.14, A.16, A.17 | All regulated |
| PCI-DSS v4 | Req 6, 7, 10, 11, 12 | Payments, fintech |

## Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| `ANTHROPIC_API_KEY` | Claude API key for narrative generation | Yes |
| `GRC_REPO_PATH` | Path to the repository to audit | No |
| `GRC_FRAMEWORK` | Default framework (soc2/iso27001/pcidss) | No |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Apache 2.0 — see [LICENSE](LICENSE).