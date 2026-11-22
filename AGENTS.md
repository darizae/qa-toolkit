# Agent instructions — Evidence-Driven QA Toolkit

## Mission

Build an independently authored, portable QA tool with a Python CLI, optional MCP adapter and Agent Skill. Consult README.md, docs/PRODUCT_SPEC.md, docs/ROADMAP.md and docs/EVIDENCE_MODEL.md. Update the roadmap and relevant GitHub issues when implementing a milestone.

## Safety and provenance

- Never copy or vendor content from the reconstructed static reference repository or its documents, fixtures, source code, and scripts. Do not execute anything from that archive.
- Flowstead is a **separate, currently private** example application. You may inspect it only when authorized; do not vendor, commit, or expose any of its source, secrets, data, or documents here.
- This repository must stand alone. Tests and examples shipped here must be independently authored and synthetic.
- Static source references are **not** coverage. Distinguish `indexed`, `referenced_unverified`, `unreferenced`, `blocked`, `verified_pass`, `verified_fail` and `skipped` where relevant, with real execution evidence for the latter statuses.
- Read-only by default. Do not run projects, Docker, databases, migrations, browser automation, or other potentially destructive workloads unless explicitly approved for a safe disposable environment.
- Keep MCP file access within the configured project, and never introduce arbitrary shell execution in public MCP tools.
- Never expose tokens, database URLs, private source, raw user data, test credentials, or internal services in reports.
- No publication to PyPI, MCP Registry, an app marketplace, or deployment of a remote service without an explicit release instruction.
- No false claims that paid ChatGPT subscription checkout is available through its plugin UI; verify current platform rules before monetization decisions.

## Engineering

- Prefer the project's existing test tools, dependency and environment management.
- Keep the core deterministic and free of mandatory LLM dependencies.
- Write focused tests for each behavior and verify them locally.
- Favor minimal configuration and dependency surfaces; preserve clear CLI and MCP contracts.
- When finishing a task, update the roadmap/issue status with commands and observed evidence, not assumptions.
