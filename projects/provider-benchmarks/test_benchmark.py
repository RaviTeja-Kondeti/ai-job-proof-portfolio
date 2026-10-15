import json
from pathlib import Path
import unittest
from benchmark import evaluate, percentile_95


class BenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.cases = json.loads(Path(__file__).with_name("synthetic_tasks.json").read_text())

    def test_domain_winners_follow_published_rule(self):
        result = evaluate(self.cases)
        self.assertEqual(result["selected_provider_by_domain"],
                         {"company": "A", "person": "B", "job": "C"})

    def test_all_domain_provider_pairs_have_full_task_coverage(self):
        result = evaluate(self.cases)
        for providers in result["results"].values():
            self.assertEqual({row["tasks"] for row in providers.values()}, {3})

    def test_missing_provider_response_rejected(self):
        cases = json.loads(json.dumps(self.cases))
        del cases[0]["providers"]["A"]
        with self.assertRaises(ValueError):
            evaluate(cases)

    def test_nearest_rank_p95(self):
        self.assertEqual(percentile_95([10, 20, 30, 40, 50]), 50)


if __name__ == "__main__":
    unittest.main()
