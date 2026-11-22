# Product contract — Evidence-Driven QA Toolkit

Status: **proposed architecture; read-only pre-alpha implemented** (2026-11-22).

## Problem

Repositories can contain many tests yet lack verifiable evidence that security, data isolation, asynchronous states and failure recovery satisfy their intended contracts. A matching test name or case ID is not proof that the expected behavior was observed.

## Target users

Independent developers, small teams and maintainers of API-backed applications who already own a test framework and want better test completeness and auditable execution evidence.

## Product promise

From a documented behavior to a traceable test, approved execution and reproducible evidence. The agent reasons about expected behavior; a deterministic core performs discovery, execution and reporting.

## Three clients, one core

1. Python CLI for local automation and CI integration.
2. MCP server tools for agents, initially read-only stdio; optionally remote authenticated server later.
3. Portable Agent Skill for discovery, test proposal, review and evidence interpretation.

No requirement to use an LLM for deterministic CLI or report operations.

## Design priorities

- Native pytest/Playwright adapters before inventing new test DSLs.
- Stable case identities with explicit expected outcomes.
- Public-contract assertions first; storage/broker/DB/browser assertions only when necessary to prove required side effects.
- Resource-data equivalence classes: own/foreign/absent; valid/invalid; queued/finished/failed; same/related/unrelated; safe isolation.
- Shared stack for owner-isolated scenarios, private controllable stack when a test mutates global infrastructure or timing.
- Clear distinction between *unreferenced*, *referenced*, *verified* and *passed*.
- Reproducible evidence tied to repository SHA, environment, command, test selector, test output, timestamp and redaction policy.
- No arbitrary shell execution by remotely accessible MCP tools.
- Safe failure on unknown project ownership, infrastructure status or destructive operations.

## MVP boundary

**Implemented now:** parse IDs from Markdown table first columns, find candidate references in test sources, emit JSON; optional MCP wrapper exposes the same read-only operation and enforces a configured project path.

**Next:** parse stronger case definitions and test markers, add assertion review workflow, a saved schema-valid report with execution evidence, then controlled pytest adapter. Playwright, remote MCP, hosted history and payments are later work.

## Out of scope for first release

- Autonomous unattended test execution against unknown applications.
- Automatic destructive database or cloud-service provisioning.
- A replacement for pytest, Playwright or application CI.
- Production penetration testing or security certification.
- Model-hosted paid checkout or an operational SaaS platform.
- Publishing private Flowstead materials or reconstructed static sources.

## Acceptance demonstration

Use Flowstead as a private local case study with operator/Plant isolation and forecast queue behavior. The public repo contains only original, synthetic demonstration materials and independently authored evaluation summaries. Verify usefulness on an unrelated second application before claiming framework generality.
