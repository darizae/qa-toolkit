# Case and evidence model (draft)

**Do not confuse case indexing, source references, assertion review and execution evidence.**

## Candidate case record (planned schema)

```json
{
  "case_id": "AUTH-001",
  "requirement_source": "docs/requirements.md#authorization",
  "invariant": "Foreign user cannot read a protected resource",
  "actors": ["owner", "foreign", "anonymous"],
  "resource_states": ["present", "absent"],
  "expected_observables": ["HTTP status", "response disclosure"],
  "candidate_test_selectors": ["tests/test_auth.py::test_foreign"],
  "status": "referenced_unverified"
}
```

## Planned execution receipt

```json
{
  "schema_version": "0.1",
  "source_sha": "<actual checked-out commit hash>",
  "run_id": "<generated run identity>",
  "started_at_utc": "<observed timestamp>",
  "executor": "pytest",
  "command_argv": ["python", "-m", "pytest", "..."],
  "test_selector": "tests/test_auth.py::test_foreign",
  "case_ids": ["AUTH-001"],
  "environment_class": "isolated_local",
  "result": "verified_pass",
  "exit_code": 0,
  "artifacts": [],
  "redaction": "applied"
}
```

This is a **design example**, not an actual observed execution. There is no v0.1 execution writer yet.

## Status semantics

- `unreferenced`: no candidate case ID text reference discovered (not definitive absence of coverage).
- `referenced_unverified`: source mentions an ID; assertion semantics and execution unverified.
- `blocked`: missing requirement, infrastructure, access or other obstacle.
- `skipped`: execution collected the test but did not run its assertions, with a reason.
- `verified_pass`: an identified asserting test ran successfully in the recorded environment and its required observables were checked.
- `verified_fail`: an identified execution failed or observed a violated invariant.

A skip, empty collection, missing environment, or partial run cannot produce accepted all-pass evidence. No CLI or MCP feature may silently upgrade a static reference to `verified_pass`.

## Security

Only allow bounded redacted evidence artifacts. Keep source excerpts minimal and avoid capturing authorization tokens, personal identifiers, private endpoint payloads, credentials, or sensitive logs. Remote adapters require explicit least-privilege project authorization and tenant isolation.
