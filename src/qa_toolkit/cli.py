"""Small, safe command-line entry point."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .audit import audit_case_references


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="qa-toolkit",
        description="Evidence-driven QA (pre-alpha: read-only case reference auditing)",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)
    audit = sub.add_parser("audit", help="Find candidate test references to indexed cases")
    audit.add_argument("--plan", type=Path, required=True, help="Markdown case plan")
    audit.add_argument("--tests", type=Path, required=True, help="Test source directory")
    audit.add_argument("--json", action="store_true", help="Emit full JSON report")

    args = parser.parse_args(argv)
    try:
        result = audit_case_references(args.plan, args.tests)
    except (OSError, UnicodeError, ValueError) as exc:
        parser.exit(2, f"qa-toolkit: {exc}\n")

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        referenced = sum(c["status"] == "referenced_unverified" for c in result["cases"])
        print(f"Found {len(result['cases'])} indexed cases; "
              f"{referenced} referenced, {len(result['cases']) - referenced} unreferenced.")
        for case in result["cases"]:
            print(f"{case['case_id']}: {case['status']}")
        print("No tests executed. No behavioral coverage or passing results are claimed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
