"""Conservative static case-reference discovery: references are NOT proof of coverage."""

from __future__ import annotations

import re
from pathlib import Path

CASE_ID = re.compile(r"(?<![A-Z0-9])(?:[A-Z][A-Z0-9]*-)+[A-Z0-9]+(?![A-Z0-9])")
TEST_SUFFIXES = (".py", ".ts", ".tsx", ".js", ".jsx")


def _test_file(path: Path) -> bool:
    name = path.name
    return path.suffix in TEST_SUFFIXES and (
        name.startswith("test_")
        or name.endswith("_test.py")
        or any(
            name.endswith(suffix)
            for suffix in (
                ".test.ts",
                ".test.tsx",
                ".test.js",
                ".test.jsx",
                ".spec.ts",
                ".spec.tsx",
                ".spec.js",
                ".spec.jsx",
            )
        )
    )


def extract_plan_ids(text: str) -> list[str]:
    """Find stable IDs in the first column of Markdown case tables."""
    ids: set[str] = set()
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        first_cell = line.split("|", 2)[1]
        ids.update(CASE_ID.findall(first_cell))
    return sorted(ids)


def audit_case_references(plan: Path, tests: Path) -> dict:
    """Read a Markdown plan and test sources without executing code.

    A matched case ID remains *referenced_unverified*: this does not verify the
    asserting test, runtime boundary, execution status, or its observables.
    """
    plan = Path(plan).resolve(strict=True)
    tests = Path(tests).resolve(strict=True)
    if not plan.is_file():
        raise ValueError("plan must be a Markdown file")
    if not tests.is_dir():
        raise ValueError("tests must be a directory")

    ids = extract_plan_ids(plan.read_text(encoding="utf-8"))
    if not ids:
        raise ValueError("no case IDs found in Markdown table first columns")

    refs: dict[str, list[str]] = {case_id: [] for case_id in ids}
    scanned = 0
    for path in sorted(tests.rglob("*")):
        if not path.is_file() or not _test_file(path):
            continue
        if any(part in {".venv", "node_modules", ".git"} for part in path.parts):
            continue
        # A test tree may contain symlinks; do not follow files outside it.
        if not path.resolve(strict=True).is_relative_to(tests):
            continue
        if path.stat().st_size > 1_000_000:
            continue
        scanned += 1
        # A string reference is only a candidate. Never call it a PASS.
        content_ids = set(CASE_ID.findall(path.read_text(encoding="utf-8")))
        for case_id in content_ids.intersection(refs):
            refs[case_id].append(path.relative_to(tests).as_posix())

    return {
        "schema_version": "0.1",
        "analysis": "static_reference_discovery",
        "verified_execution": False,
        "plan_path": str(plan),
        "test_root": str(tests),
        "test_files_scanned": scanned,
        "cases": [
            {
                "case_id": case_id,
                "status": "referenced_unverified" if paths else "unreferenced",
                "candidate_test_files": paths,
            }
            for case_id, paths in refs.items()
        ],
        "limitations": [
            "Text matches are not assertion or behavioral coverage.",
            "No test was executed; no case is PASS.",
            "A case missing a text reference may still be tested indirectly.",
        ],
    }
