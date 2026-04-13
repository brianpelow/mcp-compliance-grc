# Contributing

## Development setup

```bash
git clone https://github.com/brianpelow/mcp-compliance-grc
cd mcp-compliance-grc
uv sync
uv run pytest
```

## Running the MCP server locally

```bash
export ANTHROPIC_API_KEY=your_key
export GRC_REPO_PATH=./your-service
export GRC_FRAMEWORK=soc2
uv run mcp-compliance-grc
```

## Standards

- All PRs require passing CI
- Test coverage must not decrease
- Update CHANGELOG.md for user-facing changes