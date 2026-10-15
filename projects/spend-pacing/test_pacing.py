import unittest
from pacing import Observation, next_spend, demo


class PacingTests(unittest.TestCase):
    def test_spend_increases_when_return_exceeds_target(self):
        result = next_spend(1000, Observation(1.5, 0), 1.2, 2000, 2000)
        self.assertGreater(result.spend, 1000)
        self.assertLessEqual(result.spend, 1200)

    def test_stale_feedback_triggers_safe_fallback(self):
        result = next_spend(1000, Observation(3.0, 3), 1.2, 2000, 2000)
        self.assertEqual(result.spend, 800)
        self.assertIn("fallback", result.reason)

    def test_remaining_budget_is_hard_cap(self):
        result = next_spend(1000, Observation(2.0, 0), 1.2, 2000, 300)
        self.assertEqual(result.spend, 300)

    def test_invalid_feedback_does_not_increase_spend(self):
        result = next_spend(1000, Observation(float("nan"), 0), 1.2, 2000, 2000)
        self.assertLess(result.spend, 1000)

    def test_demo_does_not_overspend(self):
        trace = demo()["trace"]
        self.assertLessEqual(sum(row["spend"] for row in trace), 5000)


if __name__ == "__main__":
    unittest.main()
