"""Test the question-first API surface and indexed test-case contracts."""

import json
import tempfile
import unittest
from pathlib import Path

from qa_toolkit.cases import cases_from_file, cases_markdown, compile_cases
from qa_toolkit.surface import extract_surface, surface_from_file, surface_markdown

ROOT = Path(__file__).resolve().parents[1]
OPENAPI = ROOT / "examples" / "synthetic-api" / "openapi.json"
ANSWERS = ROOT / "examples" / "synthetic-api" / "answers.json"


class SurfaceCaseTests(unittest.TestCase):
    def test_surface_discovers_methods_and_contract_questions(self):
        surface = surface_from_file(OPENAPI)
        self.assertEqual(len(surface["operations"]), 2)
        op = surface["operations"][0]
        self.assertEqual(op["method"], "POST")
        self.assertEqual(op["path"], "/v1/jobs")
        self.assertIn("allowed", {q["key"] for q in op["questions"]})
        self.assertIn("forbidden", {q["key"] for q in op["questions"]})
        self.assertIn("observables", {q["key"] for q in op["questions"]})
        self.assertEqual(op["stories"], [])
        self.assertIn("Testable API surface", surface_markdown(surface))

    def test_case_compilation_is_stable_and_auditable(self):
        source = json.loads(ANSWERS.read_text())
        result = compile_cases(source)
        self.assertEqual(len(result["cases"]), 4)
        self.assertEqual(
            [c["case_id"] for c in result["cases"]],
            [c["case_id"] for c in cases_from_file(ANSWERS)["cases"]],
        )
        self.assertTrue(all(c["status"] == "specified_unverified" for c in result["cases"]))
        md = cases_markdown(result)
        for case in result["cases"]:
            self.assertIn(case["case_id"], md)
        self.assertIn("## Test stories", md)

    def test_unanswered_operation_must_be_explicitly_excluded(self):
        data = surface_from_file(OPENAPI)
        with self.assertRaisesRegex(ValueError, "add stories"):
            compile_cases(data)

    def test_no_story_returns_error_even_if_excluded(self):
        data = surface_from_file(OPENAPI)
        for op in data["operations"]:
            op["out_of_scope"] = "Not reviewed for current iteration"
        with self.assertRaisesRegex(ValueError, "no test stories"):
            compile_cases(data)

    def test_empty_contract_sources_cannot_generate_tests(self):
        data = json.loads(ANSWERS.read_text())
        data["operations"][0]["contract"]["sources"] = []
        with self.assertRaisesRegex(ValueError, "sources"):
            compile_cases(data)

    def test_duplicate_story_key_rejected(self):
        data = json.loads(ANSWERS.read_text())
        data["operations"][0]["stories"].append(data["operations"][0]["stories"][0])
        with self.assertRaisesRegex(ValueError, "duplicate story key"):
            compile_cases(data)

    def test_openapi_is_not_security_truth(self):
        spec = json.loads(OPENAPI.read_text())
        spec["security"] = [{"BearerAuth": []}]
        result = extract_surface(spec)
        self.assertEqual(result["operations"][0]["contract"]["allowed"], [])
        self.assertEqual(result["operations"][0]["declared_security"], [{"BearerAuth": []}])

    def test_invalid_openapi_and_missing_operation(self):
        with self.assertRaises(ValueError):
            extract_surface({"openapi": "3.1.0", "paths": {}})
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d) / "bad.json"
            tmp.write_text("not json")
            with self.assertRaisesRegex(ValueError, "UTF-8 JSON"):
                surface_from_file(tmp)


if __name__ == "__main__":
    unittest.main()
