# Roadmap — open-source QA planning and evidence

Updated: 2026-11-22. Issues are the canonical task tracker. A milestone is complete only when its stated acceptance conditions are achieved.

| Milestone | State | Purpose | Tracking |
| --- | --- | --- | --- |
| M0 — Repository and CLI | IN PROGRESS | Public MIT repo, package metadata, core tests, package install and MCP protocol smoke | [#1](https://github.com/darizae/qa-toolkit/issues/1) |
| M1 — Question-first API design | IN PROGRESS | OpenAPI discovery, per-operation 9-question worksheet, reviewed stories, deterministic IDs, stronger case schema | [#2](https://github.com/darizae/qa-toolkit/issues/2) |
| M2 — Evidence adapters | PLANNED | Assertion-level audits, controlled pytest runner, provenance, skipped/failed/empty fail-closed classification | [#3](https://github.com/darizae/qa-toolkit/issues/3) |
| M3 — Agent portability | IN PROGRESS | Portable skill, setup guides for multiple hosts, second-project validation | [#4](https://github.com/darizae/qa-toolkit/issues/4) |
| M4 — Flowstead case study | PLANNED | Read-only backend/queue coverage audit, redacted proof, safely contained fault injection | [#5](https://github.com/darizae/qa-toolkit/issues/5) |
| M5 — Distribution and browser evidence | IN PROGRESS | PyPI, MCP metadata, Playwright evidence import, readable reports and reproducible release | [#6](https://github.com/darizae/qa-toolkit/issues/6) |
| M6 — Optional hosted MCP | BACKLOG | Evaluate an authenticated hosted endpoint and app registration if useful; keep local core free | [#7](https://github.com/darizae/qa-toolkit/issues/7) |

## Current scope

**Shipped source capabilities:** local OpenAPI JSON endpoint discovery, explicit nine-question contract worksheet, validated reviewed stories, stable generated case IDs, reference audit, local MCP tools and Agent Skill.

**Not yet available:** semantic assertion verification, test generation into customer code, running integration tests on behalf of an agent, execution receipts and HTML QA dashboards. The CLI never reports a passing test without execution evidence.

## Upcoming decisions

1. Stabilize the questionnaire and indexed-case schema, including continuity when endpoints rename.
2. Choose a narrow native pytest adapter without arbitrarily executing project commands.
3. Require exact case ID → assertion → runner result → source SHA linkage in evidence reports.
4. Add Playwright JSON/HTML evidence import, and a second synthetic application example.
5. Expand beyond OpenAPI discovery to GraphQL/gRPC/event/CLI surfaces.
6. Consider remote MCP hosting only if it materially improves use; no commercial dependency is required.

## Evidence rule

`specified_unverified` is a designed case, `referenced_unverified` is a source string match; neither is a PASS. Only observed test executions with assertions and traceable results can eventually produce `verified_pass`.
