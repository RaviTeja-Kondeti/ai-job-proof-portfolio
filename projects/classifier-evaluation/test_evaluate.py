import json
from pathlib import Path
import unittest
from evaluate import evaluate


class ClassifierEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.rows = json.loads(Path(__file__).with_name("synthetic_predictions.json").read_text())

    def test_slice_failure_blocks_release_despite_good_overall_accuracy(self):
        report = evaluate(self.rows)
        self.assertGreaterEqual(report["accuracy"], 0.8)
        self.assertFalse(report["gates"]["worst_slice_accuracy"])
        self.assertFalse(report["release_ready"])

    def test_invalid_and_duplicate_data_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(self.rows + [self.rows[0]])
        bad = json.loads(json.dumps(self.rows))
        bad[0]["score"] = 1.1
        with self.assertRaises(ValueError):
            evaluate(bad)

    def test_calibration_uses_every_observation(self):
        report = evaluate(self.rows)
        self.assertEqual(sum(group["n"] for group in report["calibration"]), len(self.rows))
        self.assertGreaterEqual(report["ece"], 0)


if __name__ == "__main__":
    unittest.main()
