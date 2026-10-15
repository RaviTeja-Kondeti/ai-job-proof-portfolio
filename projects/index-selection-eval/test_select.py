import copy
import json
from pathlib import Path
import unittest

from index_policy import evaluate, select


class IndexSelectionTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(Path(__file__).with_name("synthetic_pages.json").read_text())

    def test_downstream_coverage_and_budget(self):
        result = evaluate(self.data)
        base = result["policies"]["value_threshold"]
        candidate = result["policies"]["freshness_dedup_budget"]
        self.assertGreater(candidate["weighted_query_coverage"],
                           base["weighted_query_coverage"])
        self.assertLessEqual(candidate["cost"], self.data["budget"])
        self.assertEqual(candidate["duplicate_pages"], 0)
        self.assertGreater(base["duplicate_pages"], 0)

    def test_ground_truth_does_not_leak_into_selection(self):
        before = select(self.data["pages"], self.data["budget"], True)
        changed = copy.deepcopy(self.data)
        for page in changed["pages"]:
            page["true_query_coverage"] = ["q4"]
        after = select(changed["pages"], changed["budget"], True)
        self.assertEqual(before, after)

    def test_bad_labels_and_cost_rejected(self):
        changed = copy.deepcopy(self.data)
        changed["pages"][0]["true_query_coverage"] = ["unknown"]
        with self.assertRaises(ValueError):
            evaluate(changed)
        changed = copy.deepcopy(self.data)
        changed["pages"][0]["cost"] = 0
        with self.assertRaises(ValueError):
            evaluate(changed)


if __name__ == "__main__":
    unittest.main()
