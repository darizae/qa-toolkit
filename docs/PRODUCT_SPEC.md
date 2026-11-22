# Product contract — Evidence-Driven QA Toolkit

Status: **early open-source release** (2026-11-22).

## Problem

Repositories often have tests but lack a systematic process for deriving the right tests from their intended API contracts. Existing test names and IDs provide little assurance that all allowed, denied, conditional, lifecycle and failure behaviors have been exercised.

## Model

The complete direction is:

```text
testable API surface
  → agent asks and answers contract questions for each operation
  → actor / data / state equivalence classes
  → explicit test stories
  → deterministic indexed test IDs
  → assertion-level coverage inspection
  → controlled execution and verifiable evidence
```

The first five steps are partly implemented (endpoint discovery, questionnaire, indexed case generation and static reference audit); the agent currently performs the semantic reasoning and requirement discovery. Execution and report orchestration are future work.

## Inputs, responsibilities and truth

- **OpenAPI/Swagger JSON**: discovery of actually declared HTTP operations, inputs, outputs and security hints. It cannot prove intended business policy.
- **Product specification**: truth for who is allowed, forbidden, conditions, relationships, effects, expected outcomes and failure rules.
- **Agent Skill**: question-first analysis, gap detection, planning and proposal of test stories. Unknown intended requirements should be asked, not guessed.
- **Core CLI and MCP**: bounded, deterministic read-only extraction/validation, reproducible IDs and test-source ID matching.
- **Existing tests**: evidence of coverage only after assertions have been reviewed; passing status requires actual execution evidence.

## Test families

Authentication/authorization, data isolation, input validation and boundaries, resource relationship/existence, privacy/non-disclosure, async lifecycle/worker recovery, concurrency, idempotency, transactional integrity, pagination, ordering, failure responses, rate limiting, exports, compatibility and domain-specific rules. Not every endpoint requires every dimension.

## Surfaces and packaging

- Python CLI: `qa-toolkit`.
- Local MCP stdio server: `qa-toolkit-mcp` or `evidence-driven-qa`.
- Portable skill: `skills/evidence-driven-qa/SKILL.md`.
- Registry metadata: `server.json`.

Single Python package, MIT license. Hosted HTTP app and any paid offerings are optional future work, not prerequisites.

## Current functionality

`qa-toolkit surface --openapi <local.json> --json` returns an editable JSON questionnaire. `qa-toolkit cases --answers <reviewed.json>` compiles stories with deterministic IDs and `specified_unverified` status. `qa-toolkit audit --plan <plan.md> --tests <folder>` finds candidate case ID references; no tests are run or marked PASS. The MCP server exposes the same operations without writing files.

## Deferred

- Deriving requirements without human/agent reasoning.
- Automatic source edits, arbitrary test execution and infrastructure orchestration.
- Assertion semantic checking, execution receipts, Playwright artifacts and HTML reports.
- Hosted remote MCP and app marketplace integrations.

For a worked example, see [the QA methodology](WORKFLOW.md) and [synthetic API fixture](../examples/synthetic-api/CONTRACT.md). A private Flowstead application may be used for local evaluation, without distributing its source or fixtures.
