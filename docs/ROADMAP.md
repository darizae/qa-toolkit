# Roadmap and milestone acceptance

Last updated: **2026-11-22**. Milestone status reflects implemented work, not aspiration. GitHub issues are the task tracker; update this document when the public state changes.

| Milestone | Status | Deliverable | Exit criterion |
| --- | --- | --- | --- |
| [M0 — Foundations](https://github.com/darizae/qa-toolkit/issues/1) | IN PROGRESS | Public repository and initial commit published at [07cd039](https://github.com/darizae/qa-toolkit/commit/07cd039899b514053a7291a383e1f0899b60979b); original architecture, tests and reference-audit CLI exist | Still needs clean install and actual MCP client protocol smoke test |
| [M1 — Case and evidence contracts](https://github.com/darizae/qa-toolkit/issues/2) | PLANNED | Versioned case schema, assertion-level linkage, machine-readable report | Deterministic validation fixtures and failure modes covered |
| [M2 — Native test adapters](https://github.com/darizae/qa-toolkit/issues/3) | PLANNED | Controlled pytest execution; optional Playwright result reader | Nonzero/empty/skipped/crashed runs classified accurately |
| [M3 — Portable QA skill](https://github.com/darizae/qa-toolkit/issues/4) | IN PROGRESS | Repository inspection, case reasoning, review, safe execution guidance | Skill works with two different projects and does not overclaim |
| [M4 — Flowstead case study](https://github.com/darizae/qa-toolkit/issues/5) | PLANNED | Private local authorization/queue audit, controlled fault injection, redacted public report | Actual run and evidence are reproducible; no private source copied |
| [M5 — Distributable release](https://github.com/darizae/qa-toolkit/issues/6) | PLANNED | PyPI release, portable skill distribution, MCP package metadata | Fresh-install tests, version, license, docs, security checklist |
| [M6 — Hosted commercial MCP app](https://github.com/darizae/qa-toolkit/issues/7) | RESEARCH | Remote auth, tenant isolation, billing outside restricted in-app channels, supported app review | Compliance, user consent, privacy policy and operational reliability verified |

## Near-term task order

1. Complete M0 by validating a clean install and stdio MCP protocol behavior. Public GitHub initialization and milestone issues are already complete.
2. Design a normalized case document and evidence receipt: intended outcomes, source anchors, test selector, boundary, result, SHA.
3. Improve discovery to distinguish literal ID references from asserting tests without treating either as execution.
4. Add a tightly bounded explicit local pytest runner, with no arbitrary shell strings and an ownership-aware environment contract.
5. Assess Flowstead's selected cases read-only, identify one evidence gap and one controlled test fault.
6. Add Playwright JSON consumption, then human-readable HTML report, and verify a second unrelated project.
7. Only then prepare PyPI/official MCP Registry and optional remote ChatGPT/Claude app submission.

## Reporting convention

Use `DONE` only with a link to a commit and successful acceptance evidence. Keep `BLOCKED`, `UNVERIFIED` and `PLANNED` explicit. A case ID seen in source does not prove that a test has executed or passed.

## Distribution decision

Use one Python distribution for core CLI + optional MCP SDK extra. A local MCP server is not a hosted app. A managed commercial plan can be added behind a separately secured service, but ChatGPT plugin digital-subscription checkout restrictions apply.
