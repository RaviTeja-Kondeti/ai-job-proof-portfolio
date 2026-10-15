import unittest
from allocate import Campaign, allocate, round_robin, portfolio_value, demo


class AllocationTests(unittest.TestCase):
    def setUp(self):
        self.campaigns = [
            Campaign("a", "US", "search", 100, 0.02, 5, 100, 800),
            Campaign("b", "EU", "social", 50, 0.005, 2, 100, 800),
        ]

    def test_budget_and_bounds_hold(self):
        result = allocate(self.campaigns, 900, step=100)
        self.assertEqual(sum(result.values()), 900)
        for campaign in self.campaigns:
            self.assertGreaterEqual(result[campaign.name], campaign.minimum)
            self.assertLessEqual(result[campaign.name], campaign.maximum)

    def test_optimized_value_beats_uninformed_baseline_on_assumed_curves(self):
        chosen = allocate(self.campaigns, 900)
        baseline = round_robin(self.campaigns, 900)
        self.assertGreater(portfolio_value(self.campaigns, chosen),
                           portfolio_value(self.campaigns, baseline))

    def test_more_uncertainty_can_change_selection(self):
        campaigns = [
            Campaign("uncertain", "US", "a", 110, 0.01, 100, 0, 500),
            Campaign("stable", "US", "b", 95, 0.01, 1, 0, 500),
        ]
        self.assertGreater(allocate(campaigns, 100)["uncertain"],
                           allocate(campaigns, 100, uncertainty_weight=1)["uncertain"])

    def test_infeasible_budget_rejected(self):
        with self.assertRaises(ValueError):
            allocate(self.campaigns, 1700)

    def test_demo_is_deterministic(self):
        self.assertEqual(demo(), demo())


if __name__ == "__main__":
    unittest.main()
