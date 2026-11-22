# Indexed integration QA test cases

> Generated from reviewed test stories; specification is not proof of execution.

| Case ID | Endpoint | Category | Expected outcome | Evidence |
| --- | --- | --- | --- | --- |
| `QA-GET-V1-RECORDS-RECORD-ID-FOREIGN-READ-NONDISCLO-85D32E43` | `GET /v1/records/{record_id}` | privacy-nondisclosure | Both requests return HTTP 404; Sanitized responses do not disclose record existence or owner data | HTTP statuses and normalized response bodies |
| `QA-GET-V1-RECORDS-RECORD-ID-OWNER-READ-A76890AF` | `GET /v1/records/{record_id}` | authorization | HTTP 200 with Alice's record ID | HTTP response status and JSON record ID |
| `QA-POST-V1-JOBS-INVALID-JOB-UNCHANGED-519D7EC6` | `POST /v1/jobs` | input-validation | HTTP 400; No new job is persisted | HTTP status and comparison of test-owned job IDs |
| `QA-POST-V1-JOBS-VALID-JOB-QUEUED-92AAC9BD` | `POST /v1/jobs` | lifecycle-async | HTTP 202 with nonempty job ID; One job owned by this workspace enters queued state | HTTP response, test-owned queue observation |

## Test stories

### `QA-GET-V1-RECORDS-RECORD-ID-FOREIGN-READ-NONDISCLO-85D32E43` — foreign-read-nondisclosure

- **Actor:** authenticated foreign user
- **Given:** Alice has a record, Bob does not own it, and an absent record ID is available
- **When:** Bob fetches both Alice's and absent record IDs
- **Then:** Both requests return HTTP 404; Sanitized responses do not disclose record existence or owner data
- **Evidence:** HTTP statuses and normalized response bodies
- **Source:** examples/synthetic-api/CONTRACT.md
- **Status:** specified_unverified

### `QA-GET-V1-RECORDS-RECORD-ID-OWNER-READ-A76890AF` — owner-read

- **Actor:** authenticated owner
- **Given:** A record exists in Alice's workspace
- **When:** Alice requests GET /v1/records/{record_id}
- **Then:** HTTP 200 with Alice's record ID
- **Evidence:** HTTP response status and JSON record ID
- **Source:** examples/synthetic-api/CONTRACT.md
- **Status:** specified_unverified

### `QA-POST-V1-JOBS-INVALID-JOB-UNCHANGED-519D7EC6` — invalid-job-unchanged

- **Actor:** authenticated user
- **Given:** An invalid payload and a snapshot of owned job state
- **When:** The user submits the invalid job
- **Then:** HTTP 400; No new job is persisted
- **Evidence:** HTTP status and comparison of test-owned job IDs
- **Source:** examples/synthetic-api/CONTRACT.md
- **Status:** specified_unverified

### `QA-POST-V1-JOBS-VALID-JOB-QUEUED-92AAC9BD` — valid-job-queued

- **Actor:** authenticated user
- **Given:** Valid job payload and an isolated queue
- **When:** The user sends POST /v1/jobs
- **Then:** HTTP 202 with nonempty job ID; One job owned by this workspace enters queued state
- **Evidence:** HTTP response, test-owned queue observation
- **Source:** examples/synthetic-api/CONTRACT.md
- **Status:** specified_unverified
