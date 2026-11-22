"""CLI for local, non-executing API contract design and test-reference discovery."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .audit import audit_case_references
from .cases import cases_from_file, cases_markdown
from .surface import surface_from_file, surface_markdown


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="qa-toolkit",
        description="Discover API surfaces, design indexed QA cases, and audit case references.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    surface = sub.add_parser(
        "surface", help="Discover an OpenAPI JSON surface and create a question-first worksheet"
    )
    surface.add_argument("--openapi", type=Path, required=True, help="Local OpenAPI JSON file")
    surface.add_argument("--json", action="store_true", help="Emit editable JSON questionnaire")

    cases = sub.add_parser(
        "cases", help="Compile answered test stories into deterministic indexed cases"
    )
    cases.add_argument("--answers", type=Path, required=True, help="Reviewed JSON questionnaire")
    cases.add_argument("--json", action="store_true", help="Emit JSON case registry")

    audit = sub.add_parser(
        "audit", help="Find candidate test references to indexed cases, without executing"
    )
    audit.add_argument("--plan", type=Path, required=True, help="Markdown case plan")
    audit.add_argument("--tests", type=Path, required=True, help="Test source directory")
    audit.add_argument("--json", action="store_true", help="Emit full JSON report")

    args = parser.parse_args(argv)
    try:
        if args.command == "surface":
            result = surface_from_file(args.openapi)
            print(json.dumps(result, indent=2) if args.json else surface_markdown(result))
        elif args.command == "cases":
            result = cases_from_file(args.answers)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(cases_markdown(result), end="")
        else:
            result = audit_case_references(args.plan, args.tests)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                referenced = sum(
                    case["status"] == "referenced_unverified" for case in result["cases"]
                )
                print(
                    f"Found {len(result['cases'])} indexed cases; "
                    f"{referenced} referenced, "
                    f"{len(result['cases']) - referenced} unreferenced."
                )
                for case in result["cases"]:
                    print(f"{case['case_id']}: {case['status']}")
                print("No tests executed. No behavioral coverage or passing results are claimed.")
    except (OSError, UnicodeError, ValueError) as exc:
        parser.exit(2, f"qa-toolkit: {exc}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
