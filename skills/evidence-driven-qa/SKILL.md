---
name: evidence-driven-qa
description: Discover the testable API surface, question each endpoint's allowed/forbidden behavior and conditions, design test stories, generate indexed QA cases, and audit evidence. Applies to security, authorization, validation, asynchronous workflows, data integrity, reliability and other integration scenarios.
---

# Evidence-Driven QA

## Core principle

**Do not start by writing tests.** Start by understanding the testable behavior.

For each exposed behavior, distinguish *intended requirements* from *current implementation*. An existing handler shows how the application behaves now, not necessarily how it should behave. A test ID is not proof of an assertion; an assertion is not proof of an executed PASS.

## 1 — Discover the testable surface

Read the repository's agent instructions and relevant specifications. Find a committed OpenAPI/Swagger JSON, FastAPI generated schema, router/handler definitions, other contracts (GraphQL schema, gRPC protobufs, events, CLI commands), and nearby tests. Read only required source.

For OpenAPI JSON already present locally:

```bash
qa-toolkit surface --openapi path/to/openapi.json --json
```

Or use MCP `qa_discover_api_surface(openapi_path)`. This yields a worksheet. When there is no OpenAPI file, inventory the actual declared routes/contracts manually in a compact table and apply exactly the same question sequence. Never contact an unknown hosted endpoint simply to retrieve a schema.

## 2 — Ask and answer for each operation

Use **the requirements, documented security rules, contracts and owner decisions**, not assumptions. Ask the owner about unresolved policies instead of guessing.

For *each endpoint or operation*, answer:

1. **Intent:** What useful behavior should this expose?
2. **Allowed:** Who should be allowed to do it or see the result?
3. **Forbidden:** Who must be rejected, including anonymous, foreign, revoked or otherwise invalid principals?
4. **Conditions:** What must be true about input shape, ranges, timestamps, roles, state and feature flags?
5. **Relationships:** What must be true about tenant, owner, parent-child links, requested IDs and related resources?
6. **Effects:** Which persistent records, files, events, messages or caches should change? Which must remain unchanged after rejection?
7. **Observables:** What HTTP response, schema, headers, state or side effect would actually prove the required behavior?
8. **Failure modes:** What happens for absent/stale/queued/failed states, timeouts, retries, concurrency, partial writes and unavailable dependencies?
9. **Sources:** Which explicit specification, policy or approved decision justifies the expected result?

Use an actor/resource/state matrix. Include **owner / foreign / anonymous / absent** where applicable and preserve meaningful distinctions. "GET returns 200" alone rarely proves a secure end-to-end requirement.

## 3 — Choose relevant testing dimensions

Use the smallest equivalence classes that expose plausible bugs:

- **Authentication and authorization:** expired/invalid/anonymous principals, cross-tenant resources, real foreign IDs versus absent IDs, error-based disclosure.
- **Validation & boundary values:** required/missing/null fields, malformed formats, maximum sizes, timestamp/timezone rules, rejected invalid input that leaves state unchanged.
- **Resource identity & relationship:** ownership, parent/child mismatches, duplicate external references, same-name/different-content cases.
- **Lifecycle / asynchronous execution:** created/queued/running/completed/failed states, worker pause, bounded wait, retries, crash before/after commit, duplicate delivery.
- **Idempotency and concurrency:** repeated commands, parallel users, races, partial success and atomic rollback.
- **Data integrity & contracts:** serialization, sorting, pagination, filtering, rounding, data provenance, schema compatibility.
- **Failures & operations:** unavailable dependencies, timeouts, 4xx/5xx privacy, rate limits, graceful recovery, user-visible degradation.
- **Exports & frontend (if present):** file bytes, downloadable CSV/PNG/PDF, cached private data, accessibility, navigation and responsiveness.
- **Business invariants:** domain-specific constraints and permissible transitions.

Do **not** generate a giant indiscriminate product of all dimensions; choose distinct fixtures and outcomes that would catch a meaningful failure. Group stories that share setup and actually prove the same invariant.

## 4 — Write test stories, then indexed cases

Before implementing any test, represent each story with:

- **Stable story key**, unique within the endpoint (e.g. `foreign-read-nondisclosure`)
- **Category** from the worksheet's available topics
- **Actor**, **Given** conditions, **When** action
- **Then** required outcomes (include non-mutation, data isolation, side effects when relevant)
- **Evidence** that concretely proves every outcome

Fill each operation's `contract` fields in the generated JSON worksheet, including a source reference. Add explicit `stories` with those fields. An operation with no stories must include a reasoned `out_of_scope` value. Review answers with the user before treating them as canonical.

Compile cases:

```bash
qa-toolkit cases --answers qa-surface.json > INDEXED_TEST_PLAN.md
```

Or use MCP `qa_compile_indexed_cases(answers_path)`. The CLI derives stable IDs from method/path/story key. Do not silently change an existing key/ID after a case is accepted. Compiled cases are `specified_unverified`: not yet implemented or passed.

## 5 — Audit current test implementations

Search exact case IDs in test function names, pytest docstrings, Vitest/Playwright titles or nearby references. `qa-toolkit audit --plan INDEXED_TEST_PLAN.md --tests tests/ --json` (or MCP `qa_audit_case_references`) finds **candidate textual references** only.

Open relevant tests, inspect their assertions and verify each explicitly required observable is actually asserted. Respect the current project's test tools and fixture conventions. Reuse suitable fixtures rather than creating whole new runners for one story.

## 6 — Propose and verify incrementally

Propose minimal test changes in the project's native framework. Do not change application code, run tests, start containers, contact remote resources or mutate data without an approved environment. If authorized, run only the smallest relevant tests and collect the exact SHA, command, environment, observed statuses and redacted artifacts. A skipped/empty run must never be accepted as full coverage.

The current CLI/MCP package is the **discovery + story indexing + static reference** portion. Execution orchestration, report rendering and autonomous source changes are future extensions and should not be invented as implemented tools.

## 7 — Report accurately

Use the chain **requirement → endpoint/behavior → story → case ID → asserting test → execution → evidence**.

Distinguish `specified_unverified`, `referenced_unverified`, `unreferenced`, `blocked`, `skipped`, `verified_pass` and `verified_fail`. Be specific about why evidence is insufficient. Do not turn present code or matching labels into a PASS.

## Safety

Work read-only by default. Respect all repository instructions and user ownership boundaries. Never execute reconstructed archive content or copy it into this package. Do not expose secrets, live credentials, private test data, full raw request bodies or protected URLs in published case studies.
