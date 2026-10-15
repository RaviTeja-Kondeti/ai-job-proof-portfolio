import json
from pathlib import Path
import unittest
from backtest import backtest, BUDGET, MAX_WEEKLY_CHANGE


class BacktestTests(unittest.TestCase):
    def setUp(self):
        self.weeks = json.loads(Path(__file__).with_name("synthetic_history.json").read_text())

    def test_policy_preserves_budget_and_change_limit(self):
        allocations = [row["allocation"] for row in backtest(self.weeks)["weeks"]]
        self.assertTrue(all(sum(a.values()) == BUDGET for a in allocations))
        for before, after in zip(allocations, allocations[1:]):
            self.assertTrue(all(abs(after[c] - before[c]) <= MAX_WEEKLY_CHANGE
                                for c in before))

    def test_current_week_truth_does_not_leak_into_its_decision(self):
        original = backtest(self.weeks)["weeks"][3]["allocation"]
        changed = json.loads(json.dumps(self.weeks))
        changed[3]["true_rates"] = {"search":100, "social":0}
        self.assertEqual(backtest(changed)["weeks"][3]["allocation"], original)

    def test_delayed_signal_changes_next_decision(self):
        changed = json.loads(json.dumps(self.weeks))
        changed[0]["observed_rates"] = {"search":0.2, "social":1.9}
        self.assertNotEqual(backtest(changed)["weeks"][1]["allocation"],
                            backtest(self.weeks)["weeks"][1]["allocation"])

    def test_duplicate_or_invalid_rates_rejected(self):
        with self.assertRaises(ValueError):
            backtest(self.weeks + [self.weeks[0]])
        changed = json.loads(json.dumps(self.weeks))
        changed[1]["observed_rates"]["social"] = -1
        with self.assertRaises(ValueError):
            backtest(changed)


if __name__ == "__main__":
    unittest.main()
