import unittest

from forecast import (evaluate, fit, make_synthetic_cohorts, predict,
                      split_as_of)


class ForecastTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = make_synthetic_cohorts()

    def test_as_of_cutoff_prevents_delayed_label_leakage(self):
        train, test, immature = split_as_of(self.rows)
        self.assertTrue(all(r["signup_day"] + 30 <= 100 for r in train))
        self.assertTrue(all(r["signup_day"] >= 100 for r in test))
        self.assertTrue(all(r["signup_day"] + 30 <= 150 for r in test))
        self.assertGreater(immature, 0)

    def test_predictions_valid_for_sparse_unseen_cell(self):
        train, _, _ = split_as_of(self.rows)
        model = fit(train)
        example = {"segment": "consumer", "channel": "search"}
        probability, value = predict(model, example, True)
        self.assertTrue(0 <= probability <= 1)
        self.assertGreaterEqual(value, 0)

    def test_historical_missingness_does_not_change_training_model(self):
        train, _, _ = split_as_of(self.rows)
        model = fit(train)
        altered_future = [dict(row) for row in self.rows]
        for row in altered_future:
            if row["signup_day"] > 70:
                row["value_30d"] = 999999 if row["converted_7d"] else 0
        changed_train, _, _ = split_as_of(altered_future)
        self.assertEqual(model, fit(changed_train))

    def test_reports_paired_uncertainty_not_just_point_scores(self):
        report = evaluate(self.rows)
        self.assertGreater(report["test_n"], 0)
        bounds = report["candidate_minus_baseline_95pct_paired_bootstrap"]["brier"]
        self.assertEqual(len(bounds), 2)
        self.assertLessEqual(bounds[0], bounds[1])

    def test_invalid_cohort_rejected(self):
        bad = [dict(row) for row in self.rows]
        bad[0]["value_30d"] = -10
        with self.assertRaises(ValueError):
            evaluate(bad)


if __name__ == "__main__":
    unittest.main()
