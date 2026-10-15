import copy
import json
from pathlib import Path
import unittest

from insights import summarize


class InsightTests(unittest.TestCase):
    def setUp(self):
        self.fixture = json.loads(Path(__file__).with_name("synthetic_experiments.json").read_text())

    def test_proposal_has_provenance_and_approval_boundary(self):
        result = summarize(self.fixture["experiments"], self.fixture["queries"][0])
        self.assertEqual([e["id"] for e in result["eligible_evidence"]], ["e1", "e2"])
        self.assertEqual(result["next_action"], "propose_live_experiment_for_review")
        self.assertTrue(result["requires_human_approval"])
        self.assertGreater(result["approx_95pct_interval"][0], 0)

    def test_restricted_and_invalid_evidence_cannot_move_the_result(self):
        original = summarize(self.fixture["experiments"], self.fixture["queries"][0])
        changed = copy.deepcopy(self.fixture["experiments"])
        for e in changed:
            if e["id"] in ("e3", "e6", "e7"):
                e["effect"] = -100
        revised = summarize(changed, self.fixture["queries"][0])
        self.assertEqual(original["eligible_evidence"], revised["eligible_evidence"])
        self.assertEqual(original["pooled_effect"], revised["pooled_effect"])
        self.assertNotIn("permission", original["excluded_by_reason"])

    def test_conflicting_or_missing_evidence_abstains(self):
        conflict = summarize(self.fixture["experiments"], self.fixture["queries"][1])
        missing = summarize(self.fixture["experiments"], self.fixture["queries"][2])
        self.assertEqual(conflict["next_action"], "abstain")
        self.assertIn("conflict", conflict["reason"])
        self.assertEqual(missing["next_action"], "abstain")

    def test_weak_directional_evidence_abstains(self):
        changed = copy.deepcopy(self.fixture["experiments"])
        for experiment in changed:
            if experiment["id"] in ("e1", "e2"):
                experiment["effect"] = 0.002
        result = summarize(changed, self.fixture["queries"][0])
        self.assertEqual(result["next_action"], "abstain")
        self.assertLess(result["approx_95pct_interval"][0], 0)

    def test_duplicate_experiment_rejected(self):
        with self.assertRaises(ValueError):
            summarize(self.fixture["experiments"] * 2, self.fixture["queries"][0])


if __name__ == "__main__":
    unittest.main()
