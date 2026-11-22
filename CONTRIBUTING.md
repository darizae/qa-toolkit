# Contributing

Contributions to Evidence-Driven QA are welcome. The project is MIT-licensed and intended to remain useful without paid services.

## Before a substantial change

Open an issue describing the problem, expected behavior and example scenario. Especially for case-ID and report schema changes, propose a migration plan that preserves previously published test identities.

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m unittest discover -s tests -v
ruff check src tests
```

Changes should include tests and documentation. Keep the core deterministic, project-local and read-only by default; never introduce arbitrary shell execution in MCP tools.

## Proprietary material

Do not contribute proprietary application source, archives, API tokens, customer data, credentials or unlicensed code. Use independently authored synthetic fixtures and redacted logs.

## Reporting issues

File normal bugs and feature requests in [GitHub Issues](https://github.com/darizae/qa-toolkit/issues). Do not publish credentials or sensitive vulnerability details in a public issue.
