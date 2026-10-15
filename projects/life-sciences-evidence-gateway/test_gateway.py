import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("science_gateway", Path(__file__).with_name("gateway.py"))
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


class GatewayTests(unittest.TestCase):
    def setUp(self):
        self.records = module.load_records()

    def test_cited_answers_have_matching_source(self):
        cases = json.loads((Path(__file__).with_name("cases.json")).read_text())
        for case in cases[:3]:
            result = module.lookup(case["question"], self.records)
            self.assertEqual(result["pmid"], case["expected_pmid"])
            self.assertEqual(result["source_url"],
                             f"https://pubmed.ncbi.nlm.nih.gov/{result['pmid']}/")

    def test_ambiguous_or_unsupported_questions_abstain(self):
        for question in ("What did AlphaFold show?", "What drug should a patient take?"):
            self.assertEqual(module.lookup(question, self.records)["status"], "abstain")

    def test_false_source_url_and_duplicate_pmid_rejected(self):
        bad = [dict(record) for record in self.records]
        bad[0]["url"] = "https://example.com/unsupported"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "records.json"
            path.write_text(json.dumps(bad))
            with self.assertRaises(ValueError):
                module.load_records(path)
            path.write_text(json.dumps(self.records + [self.records[0]]))
            with self.assertRaises(ValueError):
                module.load_records(path)

    def test_benchmark_keeps_abstention_cases(self):
        report = module.evaluate()
        self.assertEqual(report["case_count"], 5)
        self.assertEqual(report["accuracy"], 1.0)
        self.assertEqual(sum(row["actual_pmid"] is None for row in report["cases"]), 2)


if __name__ == "__main__":
    unittest.main()
