# Flowstead integration case study (plan only)

Flowstead is a separate, currently private user-owned application with a FastAPI API, real PostgreSQL, NATS JetStream, authorization, and Playwright browser tests. See [the repository](https://github.com/darizae/flowstead) if your account has access.

**This directory contains no Flowstead source, test fixture, data, documentation or test execution receipt.** No Flowstead tests were run to create this document.

## Evaluation scope

1. Compare its existing `docs/testing/INDEXED_TEST_PLAN.md` case IDs with tests under `backend/tests` and `frontend/e2e`, using candidate-reference discovery.
2. Select authorization cases involving owner, foreign, anonymous and absent Plants. Manually inspect whether the test asserts information non-disclosure as well as status.
3. Select forecast lifecycle cases covering queued, completed, and worker outage behavior. Distinguish mocked, in-process and actual subprocess/broker boundaries.
4. Record baseline case-to-test links. Only mark a case PASS after a safe, approved local run with a test selector and actual observed evidence.
5. Add a controlled fault-injection demonstration in a **disposable test environment**; never alter production services or persistent real data.
6. Publish only redacted independently authored summaries, synthetic reproduction fixtures and run metadata approved for disclosure.

## Local-only candidate-reference example

From a toolkit checkout next to a separate Flowstead checkout:

```bash
qa-toolkit audit \
  --plan ../flowstead/docs/testing/INDEXED_TEST_PLAN.md \
  --tests ../flowstead/backend/tests \
  --json
```

This does **not** execute Flowstead and does not imply PASS/FAIL. Respect Flowstead's `AGENTS.md` restrictions, including its explicitly paused GitHub Actions CI through 2026-11-30.
