"""Tests for the conservative reference discovery contract."""

import tempfile
import unittest
from pathlib import Path

from qa_toolkit.audit import audit_case_references, extract_plan_ids
from qa_toolkit.mcp_server import _within_root


class AuditTests(unittest.TestCase):
    def test_extract_ids_only_from_markdown_table_first_column(self):
        source = (
            "# Requirements\n"
            "Mention AUTH-999 in prose.\n"
            "| Case | Meaning |\n|---|---|\n"
            "| `AUTH-001` | First |\n"
            "| `QUEUE-002`, `QUEUE-003` | More |\n"
        )
        self.assertEqual(
            extract_plan_ids(source), ["AUTH-001", "QUEUE-002", "QUEUE-003"]
        )

    def test_reference_never_counts_as_verified_execution(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "plan.md").write_text(
                "| ID | Contract |\n|---|---|\n"
                "| `AUTH-001` | Protected |\n"
                "| `AUTH-002` | Forbidden |\n",
                encoding="utf-8",
            )
            (root / "tests").mkdir()
            (root / "tests" / "test_auth.py").write_text(
                'def test_example():\n    """Case: AUTH-001."""\n    assert True\n',
                encoding="utf-8",
            )
            result = audit_case_references(root / "plan.md", root / "tests")
            self.assertFalse(result["verified_execution"])
            self.assertEqual(result["test_files_scanned"], 1)
            self.assertEqual(
                [(c["case_id"], c["status"]) for c in result["cases"]],
                [("AUTH-001", "referenced_unverified"), ("AUTH-002", "unreferenced")],
            )

    def test_mcp_path_scope_rejects_traversal(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "project"
            root.mkdir()
            (root / "plan.md").write_text("x", encoding="utf-8")
            (Path(temp) / "outside.md").write_text("x", encoding="utf-8")
            self.assertEqual(_within_root(root, "plan.md"), (root / "plan.md").resolve())
            with self.assertRaises(ValueError):
                _within_root(root, "../outside.md")


if __name__ == "__main__":
    unittest.main()
