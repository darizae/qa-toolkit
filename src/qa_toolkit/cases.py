"""Produce deterministic case IDs from explicitly answered test stories."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from .surface import CONTRACT_FIELDS, MAX_INPUT_BYTES, TOPICS

_KEY = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
_ID_CHARS = re.compile(r"[^A-Z0-9]+")
_MAX_STORIES = 3000


def _nonempty_string(obj: Any, label: str) -> str:
    if not isinstance(obj, str) or not obj.strip():
        raise ValueError(f"{label} must be a nonempty string")
    return obj.strip()


def _string_list(obj: Any, label: str, *, required: bool = False) -> list[str]:
    if not isinstance(obj, list) or any(not isinstance(s, str) or not s.strip() for s in obj):
        raise ValueError(f"{label} must be an array of nonempty strings")
    if required and not obj:
        raise ValueError(f"{label} must not be empty")
    return [s.strip() for s in obj]


def _case_id(method: str, path: str, key: str) -> str:
    op_slug = _ID_CHARS.sub("-", path.upper()).strip("-")[:28].rstrip("-") or "ROOT"
    story_slug = key.upper().replace("-", "-")[:22].rstrip("-")
    suffix = hashlib.sha256(f"{method}\n{path}\n{key}".encode()).hexdigest()[:8].upper()
    return f"QA-{method}-{op_slug}-{story_slug}-{suffix}"


def compile_cases(answers: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(answers, dict) or answers.get("kind") != "qa_surface_questionnaire":
        raise ValueError("answers must be a qa_surface_questionnaire from the surface command")
    ops = answers.get("operations")
    if not isinstance(ops, list) or not ops:
        raise ValueError("answers.operations must be a nonempty array")
    result: list[dict[str, Any]] = []
    exclusions: list[dict[str, str]] = []
    seen_operations: set[tuple[str, str]] = set()
    seen_cases: set[str] = set()
    for op in ops:
        if not isinstance(op, dict):
            raise ValueError("each operation must be an object")
        method = _nonempty_string(op.get("method"), "method").upper()
        path = _nonempty_string(op.get("path"), "path")
        if method not in {
            "GET",
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
            "HEAD",
            "OPTIONS",
            "TRACE",
        } or not path.startswith("/"):
            raise ValueError("invalid method or path in answer")
        identity = (method, path)
        if identity in seen_operations:
            raise ValueError(f"duplicate operation: {method} {path}")
        seen_operations.add(identity)
        stories = op.get("stories")
        if not isinstance(stories, list):
            raise ValueError(f"{method} {path}: stories must be an array")
        if not stories:
            reason = op.get("out_of_scope")
            if not isinstance(reason, str) or not reason.strip():
                raise ValueError(f"{method} {path}: add stories or an explicit out_of_scope reason")
            exclusions.append({"method": method, "path": path, "reason": reason.strip()})
            continue
        if len(stories) + len(result) > _MAX_STORIES:
            raise ValueError("case limit exceeded (3000)")
        contract = op.get("contract")
        if not isinstance(contract, dict):
            raise ValueError(f"{method} {path}: contract must be an object")
        for name in CONTRACT_FIELDS:
            _string_list(
                contract.get(name),
                f"{method} {path}: contract.{name}",
                required=name in {"intent", "observables", "sources"},
            )
        keys: set[str] = set()
        for story in stories:
            if not isinstance(story, dict):
                raise ValueError(f"{method} {path}: story must be an object")
            key = _nonempty_string(story.get("key"), "story.key")
            if not _KEY.fullmatch(key) or len(key) > 60:
                raise ValueError("story.key must be a lowercase hyphenated slug (max 60 chars)")
            if key in keys:
                raise ValueError(f"{method} {path}: duplicate story key {key}")
            keys.add(key)
            category = _nonempty_string(story.get("category"), "story.category")
            if category not in TOPICS:
                raise ValueError(f"unsupported story category: {category}")
            case_id = _case_id(method, path, key)
            if case_id in seen_cases:
                raise ValueError(f"case ID collision: {case_id}")
            seen_cases.add(case_id)
            result.append(
                {
                    "case_id": case_id,
                    "method": method,
                    "path": path,
                    "story_key": key,
                    "category": category,
                    "actor": _nonempty_string(story.get("actor"), "story.actor"),
                    "given": _nonempty_string(story.get("given"), "story.given"),
                    "when": _nonempty_string(story.get("when"), "story.when"),
                    "then": _string_list(story.get("then"), "story.then", required=True),
                    "evidence": _string_list(
                        story.get("evidence"), "story.evidence", required=True
                    ),
                    "contract_sources": contract["sources"],
                    "status": "specified_unverified",
                }
            )
    if not result:
        raise ValueError("no test stories supplied")
    return {
        "schema_version": "0.1",
        "kind": "indexed_test_cases",
        "coverage_claim": "specified_unverified",
        "cases": sorted(result, key=lambda x: (x["method"], x["path"], x["story_key"])),
        "explicit_exclusions": exclusions,
    }


def cases_from_file(path: Path) -> dict[str, Any]:
    path = Path(path).resolve(strict=True)
    if not path.is_file() or path.stat().st_size > MAX_INPUT_BYTES:
        raise ValueError("answers must be an existing JSON file up to 5 MB")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError("answers must contain UTF-8 JSON") from exc
    return compile_cases(data)


def cases_markdown(compiled: dict[str, Any]) -> str:
    lines = [
        "# Indexed integration QA test cases",
        "",
        "> Generated from reviewed test stories; specification is not proof of execution.",
        "",
        "| Case ID | Endpoint | Category | Expected outcome | Evidence |",
        "| --- | --- | --- | --- | --- |",
    ]

    def safe(value: str) -> str:
        return value.replace("|", "\\|").replace("\n", " ")

    for case in compiled["cases"]:
        lines.append(
            f"| `{case['case_id']}` | `{case['method']} {safe(case['path'])}` | "
            f"{case['category']} | {safe('; '.join(case['then']))} | "
            f"{safe('; '.join(case['evidence']))} |"
        )
    lines.extend(["", "## Test stories", ""])
    for case in compiled["cases"]:
        lines.extend(
            [
                f"### `{case['case_id']}` — {case['story_key']}",
                "",
                f"- **Actor:** {case['actor']}",
                f"- **Given:** {case['given']}",
                f"- **When:** {case['when']}",
                f"- **Then:** {'; '.join(case['then'])}",
                f"- **Evidence:** {'; '.join(case['evidence'])}",
                f"- **Source:** {'; '.join(case['contract_sources'])}",
                "- **Status:** specified_unverified",
                "",
            ]
        )
    if compiled["explicit_exclusions"]:
        lines.extend(["## Explicitly excluded operations", ""])
        for exclusion in compiled["explicit_exclusions"]:
            lines.append(f"- `{exclusion['method']} {exclusion['path']}`: {exclusion['reason']}")
    return "\n".join(lines).rstrip() + "\n"
