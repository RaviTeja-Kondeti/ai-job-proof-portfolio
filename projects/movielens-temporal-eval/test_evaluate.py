import unittest

from evaluate import fit, ndcg_at_k, predict, temporal_split


class TemporalEvaluationTests(unittest.TestCase):
    def test_temporal_cutoff_never_trains_on_future_ratings(self):
        rows = [(1, 1, 5, 1), (1, 2, 4, 2), (2, 1, 2, 3),
                (2, 2, 1, 4), (3, 1, 5, 5)]
        train, test, cutoff = temporal_split(rows, 0.6)
        self.assertEqual(cutoff, 4)
        self.assertTrue(all(t < cutoff for *_, t in train))
        self.assertTrue(all(t >= cutoff for *_, t in test))

    def test_unseen_user_uses_exact_item_baseline(self):
        genres = {1: (1,), 2: (2,)}
        model = fit([(1, 1, 5, 1), (1, 2, 2, 2)], genres)
        self.assertEqual(predict(model, 99, 1, genres, True),
                         predict(model, 99, 1, genres, False))

    def test_observed_item_ranking_needs_mixed_relevance(self):
        self.assertIsNone(ndcg_at_k([(0.7, 5)] * 6))
        result = ndcg_at_k([(0.9, 5), (0.8, 4), (0.7, 3),
                            (0.6, 2), (0.5, 1)])
        self.assertAlmostEqual(result, 1.0)

    def test_invalid_split_rejected(self):
        with self.assertRaises(ValueError):
            temporal_split([], 0.8)
        with self.assertRaises(ValueError):
            temporal_split([(1, 1, 5, 1)], 1)


if __name__ == "__main__":
    unittest.main()
