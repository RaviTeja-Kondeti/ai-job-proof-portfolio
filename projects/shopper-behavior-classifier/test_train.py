import importlib.util
import unittest
from pathlib import Path

import numpy as np

SPEC = importlib.util.spec_from_file_location("shopper_train", Path(__file__).with_name("train.py"))
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def row(month="Mar", visitor="Returning_Visitor", revenue="FALSE", product=2):
    item = {col: "0" for col in module.NUMERIC}
    item.update({col: "1" for col in module.CATEGORICAL})
    item.update({"Month": month, "VisitorType": visitor, "Revenue": revenue,
                 "ProductRelated": str(product), "Weekend": "FALSE",
                 "PageValues": "0", "BounceRates": "0", "ExitRates": "0"})
    return item


class ShopperClassifierTests(unittest.TestCase):
    def test_frozen_months_are_disjoint_and_cover_dataset_months(self):
        months = [month for group in module.SPLITS.values() for month in group]
        self.assertEqual(len(months), len(set(months)))
        self.assertEqual(set(months), {"Feb", "Mar", "May", "June", "Jul", "Aug",
                                       "Sep", "Oct", "Nov", "Dec"})
        groups = module.split_rows([row("Mar"), row("Sep"), row("Nov")])
        self.assertEqual([len(groups[name]) for name in module.SPLITS], [1, 1, 1])

    def test_encoder_does_not_read_target_or_excluded_fields(self):
        training = [row(product=1), row(product=10, revenue="TRUE")]
        encoder = module.Encoder(training)
        original = encoder.transform(training)
        changed = [dict(training[0]), dict(training[1])]
        for item in changed:
            item.update({"Revenue": "TRUE" if item["Revenue"] == "FALSE" else "FALSE",
                         "PageValues": "99999", "BounceRates": "1", "ExitRates": "1",
                         "Month": "Dec"})
        np.testing.assert_array_equal(original, encoder.transform(changed))
        self.assertFalse(set(module.EXCLUDED + ("Revenue",)) & set(encoder.names))

    def test_unknown_category_has_reserved_column(self):
        encoder = module.Encoder([row(visitor="Returning_Visitor")])
        encoded = encoder.transform([row(visitor="Never_Seen")])
        self.assertEqual(encoded[0, encoder.names.index("VisitorType=UNKNOWN")], 1)

    def test_tied_scores_do_not_depend_on_input_order(self):
        scores = np.full(4, 0.2)
        for labels in ([1, 0, 0, 0], [0, 0, 0, 1]):
            self.assertAlmostEqual(module.average_precision(np.array(labels), scores), 0.25)

    def test_metrics_and_threshold_rule(self):
        y = np.array([1, 1, 0, 0], dtype=float)
        scores = np.array([0.9, 0.8, 0.2, 0.1])
        self.assertAlmostEqual(module.average_precision(y, scores), 1.0)
        threshold = module.select_threshold(y, scores)
        result = module.metrics(y, scores, threshold)
        self.assertEqual((result["tp"], result["fp"], result["fn"]), (2, 0, 0))

    def test_training_reduces_loss_on_separable_data(self):
        x = np.array([[1, -2], [1, -1], [1, 1], [1, 2]], dtype=float)
        y = np.array([0, 0, 1, 1], dtype=float)
        weights = module.fit_logistic(x, y, steps=200)
        self.assertGreater(float(module.sigmoid(x @ weights)[2]), 0.5)
        self.assertLess(float(module.sigmoid(x @ weights)[1]), 0.5)


if __name__ == "__main__":
    unittest.main()
