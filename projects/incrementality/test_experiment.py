import unittest
from experiment import estimate, simulate


class ExperimentTests(unittest.TestCase):
    def test_recovers_programmed_lift_with_large_sample(self):
        result = estimate(simulate(n=50000, incremental_rate=0.02, seed=11))
        self.assertAlmostEqual(result.incremental_rate, 0.02, delta=0.006)
        self.assertLess(result.ci_low, 0.02)
        self.assertGreater(result.ci_high, 0.02)

    def test_manual_holdout_difference(self):
        rows = [(0, 0), (0, 0), (0, 1), (0, 0),
                (1, 1), (1, 1), (1, 0), (1, 0)]
        self.assertEqual(estimate(rows).incremental_rate, 0.25)

    def test_empty_arm_rejected(self):
        with self.assertRaises(ValueError):
            estimate([(1, 1), (1, 0)])

    def test_reproducible_randomization(self):
        self.assertEqual(simulate(n=100, seed=7), simulate(n=100, seed=7))


if __name__ == "__main__":
    unittest.main()
