import copy
import json
from pathlib import Path
import unittest

from evaluate import evaluate, rank


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(Path(__file__).with_name("synthetic_music.json").read_text())

    def test_personalization_improves_synthetic_heldout_ranking(self):
        report = evaluate(self.data)
        self.assertGreater(report["variants"]["personalized"]["mean_ndcg_at_k"],
                           report["variants"]["popular"]["mean_ndcg_at_k"])
        self.assertTrue(report["offline_quality_gate"])

    def test_cold_start_falls_back_to_popularity(self):
        cold = self.data["users"][-1]
        self.assertEqual(rank(cold, self.data["tracks"], True),
                         rank(cold, self.data["tracks"], False))

    def test_rejects_training_holdout_leakage(self):
        changed = copy.deepcopy(self.data)
        changed["users"][0]["heldout_relevance"]["j3"] = 3
        with self.assertRaises(ValueError):
            evaluate(changed)

    def test_rejects_unknown_history_and_bad_label(self):
        changed = copy.deepcopy(self.data)
        changed["users"][0]["heard"] = ["missing"]
        with self.assertRaises(ValueError):
            evaluate(changed)
        changed = copy.deepcopy(self.data)
        changed["users"][0]["heldout_relevance"]["j1"] = 4
        with self.assertRaises(ValueError):
            evaluate(changed)


if __name__ == "__main__":
    unittest.main()
