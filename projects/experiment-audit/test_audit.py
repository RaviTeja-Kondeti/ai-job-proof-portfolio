import unittest
from audit import assign, audit, synthetic_experiment


class ExperimentAuditTests(unittest.TestCase):
    def setUp(self):
        self.rows = synthetic_experiment()

    def test_assignment_is_stable_and_changes_with_salt(self):
        self.assertEqual(assign("user-42", "a"), assign("user-42", "a"))
        assignments_a = [assign(str(i), "a") for i in range(100)]
        assignments_b = [assign(str(i), "b") for i in range(100)]
        self.assertNotEqual(assignments_a, assignments_b)

    def test_imbalanced_allocation_blocks_ship(self):
        rows = [dict(row, variant="treatment") for row in self.rows[:900]]
        rows += [dict(row, variant="control") for row in self.rows[900:]]
        report = audit(rows)
        self.assertFalse(report["checks"]["sample_ratio_ok"])
        self.assertFalse(report["ship"])

    def test_cuped_reduces_variance_in_correlated_fixture(self):
        report = audit(self.rows)
        self.assertLess(report["cuped_se"], report["raw_se"])
        self.assertGreater(report["variance_reduction_fraction"], 0.1)

    def test_more_planned_looks_raises_decision_bar(self):
        one = audit(self.rows, planned_looks=1)
        five = audit(self.rows, planned_looks=5)
        self.assertEqual(one["effect_p"], five["effect_p"])
        self.assertLess(five["alpha_per_look"], one["alpha_per_look"])

    def test_duplicate_users_rejected(self):
        with self.assertRaises(ValueError):
            audit(self.rows + [self.rows[0]])


if __name__ == "__main__":
    unittest.main()
