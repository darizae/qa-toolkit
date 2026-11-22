"""Project-confined, read-only stdio MCP adapter over the QA core."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .audit import audit_case_references
from .cases import cases_from_file
from .surface import surface_from_file


def _within_root(root: Path, path: str) -> Path:
    """Refuse file access outside the configured project, including symlink traversal."""
    root = Path(root).resolve(strict=True)
    resolved = (root / path).resolve(strict=True)
    if not resolved.is_relative_to(root):
        raise ValueError("path must stay inside the configured project root")
    return resolved


def serve(project: Path) -> None:
    try:
        from mcp.server.mcpserver import MCPServer
        from mcp.server.mcpserver.exceptions import ToolError
    except ImportError as exc:
        raise RuntimeError(
            "Install the MCP-enabled package: pip install evidence-driven-qa"
        ) from exc

    root = Path(project).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("project must be a directory")
    server = MCPServer("Evidence-driven QA", version=__version__)

    def permitted(path: str) -> Path:
        try:
            return _within_root(root, path)
        except (OSError, ValueError):
            raise ToolError("Path is unavailable or outside the configured project root") from None

    @server.tool()
    def qa_capabilities() -> dict:
        """Describe available operations and evidence status."""
        return {
            "version": __version__,
            "mode": "local_read_only",
            "capabilities": [
                "discover_api_surface",
                "compile_indexed_cases",
                "audit_case_references",
            ],
            "verified_test_execution": False,
            "description": "Discover, plan and locate QA cases; no test execution or writes.",
        }

    @server.tool()
    def qa_discover_api_surface(openapi_path: str) -> dict:
        """Read a local OpenAPI JSON file and return an endpoint-by-endpoint QA questionnaire."""
        return surface_from_file(permitted(openapi_path))

    @server.tool()
    def qa_compile_indexed_cases(answers_path: str) -> dict:
        """Compile reviewed questionnaire answers into stable, unverified test cases."""
        return cases_from_file(permitted(answers_path))

    @server.tool()
    def qa_audit_case_references(plan_path: str, tests_path: str) -> dict:
        """Locate candidate references to indexed case IDs; never claim tests pass."""
        return audit_case_references(permitted(plan_path), permitted(tests_path))

    server.run(transport="stdio")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="qa-toolkit-mcp")
    parser.add_argument(
        "--project", type=Path, default=Path.cwd(), help="Explicit allowed project root"
    )
    args = parser.parse_args(argv)
    try:
        serve(args.project)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"qa-toolkit-mcp: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
