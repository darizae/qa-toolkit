"""Optional local read-only MCP adapter over the same QA core."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .audit import audit_case_references


def _within_root(root: Path, path: str) -> Path:
    """MCP tool requests cannot read outside the explicitly configured project."""
    root = Path(root).resolve(strict=True)
    resolved = (root / path).resolve(strict=True)
    if not resolved.is_relative_to(root):
        raise ValueError("path must stay inside the configured project root")
    return resolved


def serve(project: Path) -> None:
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:
        raise RuntimeError(
            "MCP support is optional. Install: pip install 'evidence-driven-qa[mcp]'"
        ) from exc

    root = Path(project).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("project must be a directory")
    server = FastMCP("Evidence-driven QA")

    @server.tool()
    def qa_capabilities() -> dict:
        """Describe read-only capabilities and evidence limitations."""
        return {
            "version": __version__,
            "mode": "local_read_only",
            "capabilities": ["audit_case_references"],
            "verified_test_execution": False,
            "description": "Only text references are located, never verified as passing tests.",
        }

    @server.tool()
    def qa_audit_case_references(plan_path: str, tests_path: str) -> dict:
        """Locate candidate test references in a Markdown case plan; never run tests."""
        return audit_case_references(
            _within_root(root, plan_path),
            _within_root(root, tests_path),
        )

    server.run(transport="stdio")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="qa-toolkit-mcp")
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="Allowed project root")
    args = parser.parse_args(argv)
    try:
        serve(args.project)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"qa-toolkit-mcp: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
