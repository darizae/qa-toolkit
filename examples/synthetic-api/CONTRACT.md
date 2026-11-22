# Example Workspace API — synthetic product contract

This is an independently authored fictitious example for demonstrating the questionnaire-to-indexed-case workflow. It is not a deployed service or an executable test suite.

- Authenticated user Alice can read her own record.
- Anonymous calls to record read and job creation are rejected with 401.
- Another signed-in user Bob must not read or infer details of Alice's records. A foreign record ID and nonexistent ID have indistinguishable 404 response bodies after any incidental IDs are normalized for comparison.
- Successful record reads do not mutate stored data.
- Authenticated users can submit valid jobs; the service returns 202 with a job identifier and creates exactly one queued job in that user's workspace.
- Invalid job payloads return 400 and leave owned job state unchanged.

These requirements define intended behavior for the synthetic *planning* example. The compiled test cases have not been executed against an application.
