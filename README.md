# Evidence-Driven QA Toolkit

[![Status: pre-alpha](https://img.shields.io/badge/status-pre--alpha-orange)](docs/ROADMAP.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

**An agent-assisted, evidence-first QA toolkit for developer-owned applications.**

One core, three intended interfaces: a Python CLI, an MCP server, and a portable agent skill. The eventual goal is to trace requirements to meaningful integration tests, execute authorized tests against real application boundaries, and create auditable evidence. **The current pre-alpha only scans case references; it does not run tests or certify coverage.**

## What works now

- `qa-toolkit audit`: reads stable case IDs from first-column Markdown tables and locates candidate references in Python/JS/TS test files.
- `qa-toolkit-mcp`: optional local **stdio** MCP server exposing `qa_capabilities` and `qa_audit_case_references`, scoped to an explicit project root.
- `skills/evidence-driven-qa/SKILL.md`: portable agent guidance for conservative, evidence-backed QA work.
- Unit tests for reference discovery and MCP file-path confinement.

**Not yet implemented:** verification of assertion quality, test generation, test execution/orchestration, artifact collection, HTML reports, remote MCP hosting, GitHub Action, registry/PyPI publishing, billing, or autonomous QA. Any reference found remains `referenced_unverified`.

## Install the Python CLI (from this checkout)

Requirements: Python 3.11 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
qa-toolkit --version
```

Audit an existing indexed Markdown test plan:

```bash
qa-toolkit audit \
  --plan /absolute/path/to/project/docs/testing/INDEXED_TEST_PLAN.md \
  --tests /absolute/path/to/project/backend/tests \
  --json
```

This produces JSON on stdout. `referenced_unverified` means **a candidate text reference**, never a passing test, proof of a working assertion, or verified behavioral coverage. `unreferenced` is a candidate gap, not definitive absence of coverage. This first adapter expects case IDs in the **first column of Markdown tables**. No network access, test runs, writes, or project changes are performed by `audit`.

## Agent setup

Install the generic Agent Skill into whichever coding agent you use. Review the skill and give the agent only the repository access it needs. The skill is model-agnostic; file discovery conventions differ by client.

**Claude Code — user-level skill:**

```bash
mkdir -p ~/.claude/skills/evidence-driven-qa
cp skills/evidence-driven-qa/SKILL.md \
  ~/.claude/skills/evidence-driven-qa/SKILL.md
```

**Codex / project-local agents — project skill folder:**

```bash
mkdir -p /absolute/path/to/your-project/.agents/skills/evidence-driven-qa
cp skills/evidence-driven-qa/SKILL.md \
  /absolute/path/to/your-project/.agents/skills/evidence-driven-qa/SKILL.md
```

Then ask the agent: **“Audit the indexed QA cases against existing tests. Identify candidate gaps, distinguish references from verified assertions, and do not execute anything without approval.”** For current functionality, point it to the local CLI below.

### Optional local MCP server

Install the optional MCP SDK alongside the CLI:

```bash
python -m pip install -e '.[mcp]'
```

Start a **stdio** MCP server scoped to a single project:

```bash
qa-toolkit-mcp --project /absolute/path/to/your-project
```

A stdio server is started by an MCP client, not normally run interactively. For a Claude Code client, an example registration is:

```bash
claude mcp add qa-toolkit -- \
  /absolute/path/to/qa-toolkit/.venv/bin/qa-toolkit-mcp \
  --project /absolute/path/to/your-project
```

Or configure the client with the equivalent `command`, `args`, and stdio transport. The server exposes:

- `qa_capabilities()` — current capabilities and limitations.
- `qa_audit_case_references(plan_path, tests_path)` — read-only audit using paths **inside** the configured project.

**Do not configure this stdio process as a public ChatGPT app.** A hosted ChatGPT-compatible app needs a separately deployed, authenticated, network-accessible MCP endpoint and platform review. That is a future milestone, not a capability of this initial checkout.

## Flowstead case study

[Flowstead](https://github.com/darizae/flowstead) is the planned real-app case study: FastAPI, PostgreSQL, NATS/JetStream, JWT authorization, and React/Playwright. Its GitHub repository is currently private; the public QA toolkit must not assume visitors can access it.

This repo contains **no copied Flowstead source, tests, fixtures, credentials, or documentation**, and no code from the static archived reference. Case-study instructions and the intended validation approach are in [examples/flowstead](examples/flowstead/README.md). Do not run the reference archive.

## Architecture and planning

| Surface | Current implementation | Planned role |
| --- | --- | --- |
| Python core / CLI | Read-only reference audit | Case registry, adapters, controlled executor, evidence and reports |
| Local MCP server | Read-only stdio tool | Agent-friendly audited operations |
| Portable skill | QA workflow instructions | Discover, propose, review, verify and report |
| Remote MCP app | Not implemented | Optional authenticated hosted service and UI |

- [Product contract](docs/PRODUCT_SPEC.md)
- [Roadmap with acceptance criteria](docs/ROADMAP.md)
- [Evidence and case schema](docs/EVIDENCE_MODEL.md)
- [MCP publication and monetization strategy](docs/MCP_COMMERCIALIZATION.md)
- [Decisions and provenance](docs/DECISIONS.md)
- [Release checklist](docs/RELEASE_CHECKLIST.md)
- [GitHub issues](https://github.com/darizae/qa-toolkit/issues) track milestone work

## Development

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m qa_toolkit.cli --version
```

The CLI has **no arbitrary shell-execution command** in the pre-alpha. Running integration tests, touching external resources, or proposing patches belongs to future, explicitly approved work.

## Licensing and commercialization

MIT-licensed open core; possible paid value in managed QA monitoring, team evidence retention, cross-repository dashboards and integrations. An MCP Registry listing is **discovery metadata, not a storefront**. Current ChatGPT plugin commerce restrictions must be respected, especially restrictions on in-plugin sales/upselling of digital subscriptions. See [the commercialization plan](docs/MCP_COMMERCIALIZATION.md) before shipping any paid app.

This repository is an early portfolio project. Do not present planned capabilities as shipping or make claims about test outcomes that have not been executed.
