"""Exercise the MCP transport over a real local stdio subprocess."""

import sys
import unittest
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[1]
TOOLS = {
    "qa_capabilities",
    "qa_discover_api_surface",
    "qa_compile_indexed_cases",
    "qa_audit_case_references",
}


class MCPStdioTests(unittest.IsolatedAsyncioTestCase):
    async def test_stdio_tools_respond_through_protocol(self):
        config = StdioServerParameters(
            command=sys.executable,
            args=["-m", "qa_toolkit.mcp_server", "--project", str(ROOT)],
        )
        async with (
            stdio_client(config) as (read, write),
            ClientSession(read, write) as client,
        ):
            await client.initialize()
            tools = await client.list_tools()
            self.assertEqual({tool.name for tool in tools.tools}, TOOLS)

            calls = (
                ("qa_capabilities", {}),
                (
                    "qa_discover_api_surface",
                    {"openapi_path": "examples/synthetic-api/openapi.json"},
                ),
                (
                    "qa_compile_indexed_cases",
                    {"answers_path": "examples/synthetic-api/answers.json"},
                ),
                (
                    "qa_audit_case_references",
                    {
                        "plan_path": "examples/synthetic-api/INDEXED_TEST_PLAN.md",
                        "tests_path": "tests",
                    },
                ),
            )
            for name, arguments in calls:
                result = await client.call_tool(name, arguments)
                self.assertFalse(result.is_error, name)
                self.assertTrue(result.content, name)


if __name__ == "__main__":
    unittest.main()
