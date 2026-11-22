# Roadmap — open-source QA planning and evidence

Updated: 2026-11-22. Issues are the canonical task tracker; statuses describe actual capabilities, not intended outcomes.

| Milestone | State | Purpose | Tracking |
| --- | --- | --- | --- |
| M0 — Repository and release foundations | DONE | Public MIT repo, clean package install, real MCP protocol smoke, 12 passing tests, PyPI/GitHub/MCP Registry v0.1.0 | [#1](https://github.com/darizae/qa-toolkit/issues/1) |
| M1 — Question-first API design | IN PROGRESS | Local OpenAPI discovery, nine-question worksheet, reviewed test stories and stable indexed IDs implemented; richer case schema pending | [#2](https://github.com/darizae/qa-toolkit/issues/2) |
| M2 — Evidence adapters | PLANNED | Assertion-level audits, controlled pytest runner, provenance and honest skip/empty classification | [#3](https://github.com/darizae/qa-toolkit/issues/3) |
| M3 — Agent portability | IN PROGRESS | Portable skill and multi-agent setup published; second-project workflow validation pending | [#4](https://github.com/darizae/qa-toolkit/issues/4) |
| M4 — Flowstead case study | PLANNED | Backend/queue coverage audit, redacted evidence and safely contained fault injection | [#5](https://github.com/darizae/qa-toolkit/issues/5) |
| M5 — Browser evidence and distribution | IN PROGRESS | PyPI, GitHub release and official MCP Registry published; Playwright import, readable reports and broader release QA pending | [#6](https://github.com/darizae/qa-toolkit/issues/6) |
| M6 — Optional hosted MCP | BACKLOG | Evaluate an authenticated hosted endpoint/app listing if useful; free local core retained | [#7](https://github.com/darizae/qa-toolkit/issues/7) |

## Delivered in v0.1.0

- CLI: local OpenAPI JSON `surface`, reviewed `cases`, and static-reference `audit`
- MCP stdio tools: discovery, case compiling, auditing and capability reporting
- Portable Agent Skill explaining question-first QA for authorization, validation, data integrity, asynchronous workflows, recovery and related testing
- Original synthetic API contract, questionnaire answers and indexed test-plan example
- MIT license, installation guides and reproducible release assets

## Coming next

1. Stronger normalized case/requirement schema and migration-safe indexing for renamed endpoints.
2. Assertion-quality auditing and test-source generation into native project frameworks.
3. Controlled local pytest execution with provenance, fail-closed results and redacted reports.
4. Browser artifact import and readable HTML reports.
5. More API-surface adapters and a second independent application validation.
6. Optional hosted MCP only if use cases justify it; no paid service prerequisite.

## Evidence rule

`specified_unverified` is a designed case and `referenced_unverified` is a source match. Neither is a PASS. Only observed test executions linked to asserting tests and concrete outcomes can eventually become `verified_pass`.

[Release record](RELEASE_CHECKLIST.md) · [v0.1.0](https://github.com/darizae/qa-toolkit/releases/tag/v0.1.0)
