# QA workflow: from testable API surface to indexed test cases

This is the conceptual foundation of Evidence-Driven QA. The goal is **an intentional test design, not random endpoint fuzzing**.

## Why start from the API surface?

An endpoint defines what a client can attempt. A product requirement defines what the endpoint *should* allow, forbid, and guarantee. Existing implementation code defines what it *currently* does. These are three different sources of information.

For every operation, the agent should first locate the operation contract, then reason about *actors*, *resources*, *conditions*, *relationships*, *effects* and *observables*. Each expected behavior becomes one or more **test stories**. Only after the stories are reviewed should we assign stable case IDs, map them to tests and run them.

```text
API route or event -> intended policy -> actors and state matrix
  -> allowed/forbidden decisions -> observable outcome
  -> test story -> stable case ID -> test and execution evidence
```

## Step A — Discover the surface

Start with a local OpenAPI JSON file (FastAPI's `openapi.json`, for example):

```bash
qa-toolkit surface --openapi examples/synthetic-api/openapi.json --json > qa-surface.json
```

This produces `operations[]` containing method, route, summary, declared parameters and status codes, security declarations, structured questions, blank contract fields and empty stories.

For gRPC, GraphQL, CLI, events or undocumented APIs, the agent can manually inventory operations from the declared contract. The CLI's automatic discovery currently understands local OpenAPI JSON.

The OpenAPI `security` field is a **hint**, not proof that runtime authorization works or describes the entire business policy.

## Step B — Answer nine contract questions per operation

| Question | Example: `GET /v1/records/{record_id}` |
| --- | --- |
| **Intent** | Return an existing record to its owning user |
| **Allowed** | Signed-in owner |
| **Forbidden** | Anonymous caller, authenticated foreign user |
| **Conditions** | Record exists and caller is not revoked |
| **Relationships** | Record belongs to the caller's workspace |
| **Effects** | Read must not change persisted bytes |
| **Observables** | Owner 200 + ID, anonymous 401, foreign/absent equivalent 404 |
| **Failure modes** | No disclosure from error text, status, or timing-sensitive long-poll path |
| **Sources** | Product policy or explicit approval establishing the requirement |

If the product owner never specified whether a foreign record should return 403 or 404, the agent must surface that decision rather than invent it. **Implementation is evidence of the current system, not automatically a specification of intended behavior.**

## Step C — Derive test-data equivalence classes

Choose data that distinguishes allowed from forbidden behavior. The smallest useful authorization example usually needs: (1) a real record owned by Alice, (2) a different real record owned by Bob and (3) an ID that does not exist. For transitions, choose the actual relevant states: queued/running/completed/failed. For validation, use valid, minimally invalid and boundary values. For data integrity, vary the exact property the contract claims to preserve.

Examples of relevant perspectives:

- Access: owner, foreign, anonymous, revoked, improperly scoped.
- Identity: same filename/different content, same external key/different tenant, real foreign vs absent ID.
- State: uncreated, queued, running, completed, failed, cancelled, retried.
- Reliability: repeated command, duplicate event, worker/broker outage, transient failure.
- Data: missing/null/invalid/finite values, ordering, timezone, units, pagination, export bytes.
- Browser: signed-in/out cache, user switching, responsive layout, accessibility, safe downloads.

No case should rely on global row counts in a shared test stack if unrelated tests can create data. Prefer test-owned resource IDs. A private controllable stack is appropriate only if scenarios require controlling global worker/broker state.

## Step D — Write explicit test stories

A story must connect setup, operation and evidence:

```json
{
  "key": "foreign-read-nondisclosure",
  "category": "privacy-nondisclosure",
  "actor": "authenticated foreign user",
  "given": "Alice owns a real record; Bob does not; an absent ID is available",
  "when": "Bob queries the real foreign ID and the absent ID",
  "then": [
    "Both calls return 404",
    "Bodies contain no privileged metadata"
  ],
  "evidence": [
    "HTTP statuses and normalized response bodies",
    "Alice's original record remains readable"
  ]
}
```

Add stories into the `qa-surface.json` worksheet and fill all `contract` keys. The contract must cite a real source. The [synthetic answers fixture](../examples/synthetic-api/answers.json) shows a full working example.

## Step E — Compile stable indexed cases

```bash
qa-toolkit cases --answers examples/synthetic-api/answers.json > INDEXED_TEST_PLAN.md
qa-toolkit cases --answers examples/synthetic-api/answers.json --json
```

The generated ID is a deterministic function of method, path and story key. It is not a test-function count. Group stories in implementation when they share setup *and* prove the same invariant; do not merge fundamentally different expectations for convenience.

If a reviewed API operation is intentionally excluded, set `out_of_scope` to a specific reason. An unreviewed operation without stories or a reason prevents plan compilation.

## Step F — Audit, implement and verify

```bash
qa-toolkit audit --plan INDEXED_TEST_PLAN.md --tests tests/ --json
```

The current audit looks only for exact textual case IDs inside test files. It is a **candidate index**, not static proof of assertions. The agent should inspect asserting tests and determine whether all required observables are proven. Execution receipts and report rendering require future runner adapters.

Example evidence chain for a future executor:

```text
AUTH-CASE → exact test node ID → actual runner invocation
          → source SHA → environment → measured outcome → redacted artifacts
```

A status from source-only analysis never becomes `verified_pass`. An empty, skipped, or partially executed required suite cannot imply full acceptance.

## Other testable surfaces

Beyond HTTP authorization, this method applies to event-driven APIs, transaction boundaries, data pipelines, machine-learning inference contracts, service-to-service APIs, exports, user interfaces and CLI commands. Discovery adapters for those technologies are planned; the reasoning workflow already applies independently of the current OpenAPI JSON parser.
