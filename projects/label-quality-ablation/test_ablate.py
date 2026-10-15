import importlib.util
import unittest
from pathlib import Path

import numpy as np

SPEC = importlib.util.spec_from_file_location("label_ablation", Path(__file__).with_name("ablate.py"))
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class LabelAblationTests(unittest.TestCase):
    def test_swaps_are_deterministic_and_preserve_prevalence(self):
        labels = np.array([1] * 20 + [0] * 80, dtype=float)
        first, counts = module.swap_labels(labels, 0.5, 5)
        second, _ = module.swap_labels(labels, 0.5, 5)
        np.testing.assert_array_equal(first, second)
        self.assertEqual(counts, {"positive_to_negative": 10,
                                  "negative_to_positive": 10, "total_changed": 20})
        self.assertEqual(first.sum(), labels.sum())
        self.assertEqual(int(np.sum(first != labels)), 20)

    def test_zero_fraction_changes_nothing(self):
        labels = np.array([1, 0, 0, 1], dtype=float)
        changed, counts = module.swap_labels(labels, 0, 0)
        np.testing.assert_array_equal(changed, labels)
        self.assertEqual(counts["total_changed"], 0)

    def test_invalid_fraction_and_one_class_fail(self):
        labels = np.array([1, 0], dtype=float)
        with self.assertRaises(ValueError):
            module.swap_labels(labels, -0.1, 0)
        with self.assertRaises(ValueError):
            module.swap_labels(np.ones(3), 0.5, 0)

    def test_metric_direction_for_perfect_vs_reversed_scores(self):
        y = np.array([1, 0, 1, 0], dtype=float)
        good = np.array([0.9, 0.1, 0.8, 0.2])
        bad = 1 - good
        self.assertGreater(module.classifier.average_precision(y, good),
                           module.classifier.average_precision(y, bad))


if __name__ == "__main__":
    unittest.main()
