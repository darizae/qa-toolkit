"""Extract a testable API surface and a question-first contract worksheet from OpenAPI.

Only local JSON files are inspected; this module does not follow $refs or issue HTTP
requests. OpenAPI declarations provide discovery context, not authorization truth.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

HTTP_METHODS = ("get", "post", "put", "patch", "delete", "head", "options", "trace")
MAX_INPUT_BYTES = 5_000_000
MAX_OPERATIONS = 500

QUESTIONS: tuple[tuple[str, str], ...] = (
    ("intent", "What business behavior is this endpoint supposed to provide?"),
    ("allowed", "Who is allowed to call it or access each resource?"),
    ("forbidden", "Who is forbidden, including anonymous, foreign and revoked principals?"),
    ("conditions", "Which preconditions, input ranges, states and validation rules must hold?"),
    ("relationships", "Which ownership, tenancy and parent-child relationships must be true?"),
    ("effects", "What must be created, changed, queued, persisted or left unchanged?"),
    (
        "observables",
        "Which HTTP outputs and side effects prove success, rejection and non-disclosure?",
    ),
    ("failure_modes", "Which error, timeout, retry, race or recovery behaviors matter?"),
    ("sources", "Which requirements or owner decisions establish the intended contract?"),
)

TOPICS = (
    "authentication",
    "authorization",
    "input-validation",
    "boundary-values",
    "resource-relationships",
    "data-isolation",
    "privacy-nondisclosure",
    "lifecycle-async",
    "idempotency",
    "concurrency",
    "failure-recovery",
    "data-integrity",
    "pagination-filtering",
    "error-contracts",
    "rate-limiting",
    "performance",
    "export-content",
    "business-rules",
    "compatibility",
    "accessibility",
)

CONTRACT_FIELDS = (
    "intent",
    "allowed",
    "forbidden",
    "conditions",
    "relationships",
    "effects",
    "observables",
    "failure_modes",
    "sources",
)


def _read_json(path: Path) -> dict[str, Any]:
    path = Path(path).resolve(strict=True)
    if not path.is_file():
        raise ValueError("expected a JSON file")
    if path.stat().st_size > MAX_INPUT_BYTES:
        raise ValueError("input exceeds the 5 MB safety limit")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError("input must contain UTF-8 JSON") from exc
    if not isinstance(data, dict):
        raise ValueError("JSON root must be an object")
    return data


def _short_type(value: Any) -> str:
    if not isinstance(value, dict):
        return ""
    schema = value.get("schema", {})
    return schema.get("type", "") if isinstance(schema, dict) else ""


def extract_surface(spec: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(spec, dict) or not (
        isinstance(spec.get("openapi"), str) or isinstance(spec.get("swagger"), str)
    ):
        raise ValueError("expected an OpenAPI 3.x or Swagger 2.x JSON document")
    paths = spec.get("paths")
    if not isinstance(paths, dict):
        raise ValueError("OpenAPI paths must be an object")
    operations: list[dict[str, Any]] = []
    for path, item in sorted(paths.items()):
        if not isinstance(path, str) or not path.startswith("/") or not isinstance(item, dict):
            raise ValueError("each path must be an absolute API path with an object value")
        for method in HTTP_METHODS:
            operation = item.get(method)
            if operation is None:
                continue
            if not isinstance(operation, dict):
                raise ValueError(f"{method.upper()} {path} must be an operation object")
            path_params = item.get("parameters", [])
            operation_params = operation.get("parameters", [])
            if not isinstance(path_params, list) or not isinstance(operation_params, list):
                raise ValueError(f"{method.upper()} {path} has malformed parameters")
            combined_params = path_params + operation_params
            params = [
                {
                    "name": p.get("name", ""),
                    "in": p.get("in", ""),
                    "required": bool(p.get("required", False)),
                    "type": _short_type(p),
                }
                for p in combined_params
                if isinstance(p, dict)
            ]
            security = operation.get("security", spec.get("security", []))
            responses = operation.get("responses", {})
            if not isinstance(responses, dict):
                raise ValueError(f"{method.upper()} {path} has malformed responses")
            operations.append(
                {
                    "method": method.upper(),
                    "path": path,
                    "operation_id": str(operation.get("operationId", "")),
                    "summary": str(operation.get("summary", "")),
                    "description": str(operation.get("description", ""))[:500],
                    "tags": operation.get("tags", [])
                    if isinstance(operation.get("tags", []), list)
                    else [],
                    "declared_security": security,
                    "parameters": params,
                    "request_body_present": "requestBody" in operation,
                    "declared_responses": sorted(str(key) for key in responses),
                    "questions": [{"key": key, "question": q} for key, q in QUESTIONS],
                    "contract": {key: [] for key in CONTRACT_FIELDS},
                    "stories": [],
                    "out_of_scope": None,
                }
            )
            if len(operations) > MAX_OPERATIONS:
                raise ValueError("OpenAPI exceeds 500-operation safety limit")
    if not operations:
        raise ValueError("OpenAPI document has no HTTP operations")
    return {
        "schema_version": "0.1",
        "kind": "qa_surface_questionnaire",
        "note": (
            "Declared OpenAPI security is a clue, not verified policy. "
            "An agent or reviewer must answer the questions using authoritative "
            "requirements before indexed cases can be generated."
        ),
        "source_title": str(spec.get("info", {}).get("title", ""))
        if isinstance(spec.get("info"), dict)
        else "",
        "available_topics": list(TOPICS),
        "operations": operations,
    }


def surface_from_file(path: Path) -> dict[str, Any]:
    return extract_surface(_read_json(path))


def surface_markdown(surface: dict[str, Any]) -> str:
    def safe(value: Any) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ")

    lines = [
        f"# Testable API surface: {safe(surface['source_title']) or 'API'}",
        "",
        "> Worksheet: OpenAPI is discovery context; answer from intended requirements.",
        "",
        f"**Operations discovered:** {len(surface['operations'])}",
        "",
        "| Method | Endpoint | Operation | Declared responses |",
        "| --- | --- | --- | --- |",
    ]
    for op in surface["operations"]:
        lines.append(
            f"| `{op['method']}` | `{safe(op['path'])}` | {safe(op['summary'] or op['operation_id'])} | "
            f"{', '.join(op['declared_responses'])} |"
        )
    for op in surface["operations"]:
        lines.extend(["", f"## {op['method']} `{op['path']}`", ""])
        for q in op["questions"]:
            lines.append(f"- **{q['key']}:** {q['question']}")
        lines.append(
            "- **Test stories:** For each meaningful positive/negative case, specify actor, given, when, expected results and observable evidence."
        )
    lines.extend(
        ["", "Next: fill the JSON questionnaire, then run `qa-toolkit cases --answers ...`.", ""]
    )
    return "\n".join(lines)
