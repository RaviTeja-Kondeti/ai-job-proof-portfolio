import copy
import json
from pathlib import Path
import unittest

from workflow import EnforcementLedger, evaluate, propose


class AbuseReviewTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(Path(__file__).with_name("synthetic_cases.json").read_text())

    def test_review_prioritization_and_remaining_gap(self):
        report = evaluate(self.data)
        base = report["policies"]["score_only"]
        candidate = report["policies"]["severity_weighted"]
        self.assertGreater(candidate["queue_recall"], base["queue_recall"])
        self.assertEqual(candidate["false_restrictions"], [])
        self.assertIn("a7", candidate["missed_abuse"])
        self.assertFalse(report["candidate_release_gate"])

    def test_truth_and_human_choices_do_not_enter_queue_selection(self):
        original = propose(self.data["cases"], 3, True)
        changed = copy.deepcopy(self.data)
        changed["truth"] = {case["id"]: False for case in changed["cases"]}
        changed["human_decisions"] = {}
        self.assertEqual(original, propose(changed["cases"], 3, True))

    def test_no_restriction_without_queued_human_review(self):
        ledger = EnforcementLedger({"a1": "acct_1"})
        with self.assertRaises(ValueError):
            ledger.apply_review("a2", "restrict", "reviewer")
        with self.assertRaises(ValueError):
            ledger.apply_review("a1", "restrict", "")
        self.assertEqual(ledger.restricted_accounts, set())
        ledger.apply_review("a1", "restrict", "reviewer")
        ledger.apply_review("a1", "restrict", "reviewer")
        self.assertEqual(len(ledger.events), 1)
        self.assertEqual(ledger.restricted_accounts, {"acct_1"})
        with self.assertRaises(ValueError):
            ledger.apply_review("a1", "clear", "reviewer")

    def test_missing_review_decision_rejected(self):
        changed = copy.deepcopy(self.data)
        changed["human_decisions"].pop("a1")
        with self.assertRaises(ValueError):
            evaluate(changed)


if __name__ == "__main__":
    unittest.main()
