import copy
import random
import unittest

from estimate import estimate, simulate


class MarginalReturnTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = simulate()

    def test_randomized_spend_steps_support_a_constrained_decision(self):
        result = estimate(self.rows)
        self.assertIn(result["recommended_next_channel"], result["channels"])
        for channel in result["channels"].values():
            self.assertEqual([step["from"] for step in channel["marginal_steps"]],
                             [0, 100, 200])

    def test_input_order_does_not_change_estimates(self):
        shuffled = copy.deepcopy(self.rows)
        random.Random(9).shuffle(shuffled)
        self.assertEqual(estimate(self.rows), estimate(shuffled))

    def test_missing_or_duplicate_arm_is_rejected(self):
        with self.assertRaises(ValueError):
            estimate(self.rows[1:])
        duplicated = self.rows + [dict(self.rows[0])]
        with self.assertRaises(ValueError):
            estimate(duplicated)

    def test_noiseless_curves_show_diminishing_marginal_return(self):
        result = estimate(simulate(noise_sd=0))
        for channel in result["channels"].values():
            means = [s["mean_incremental_outcome"] for s in channel["marginal_steps"]]
            self.assertGreater(means[0], means[1])
            self.assertGreater(means[1], means[2])

    def test_abstains_when_every_next_step_is_negative(self):
        rows = [dict(row, outcome=20 - row["assigned_spend"] / 100)
                for row in self.rows]
        self.assertIsNone(estimate(rows)["recommended_next_channel"])


if __name__ == "__main__":
    unittest.main()
