import json
from pathlib import Path
import unittest
from evaluate import evaluate


class RankingTests(unittest.TestCase):
    def setUp(self):
        self.queries = json.loads(Path(__file__).with_name("synthetic_queries.json").read_text())

    def test_permission_violation_blocks_better_headline_ranker(self):
        result = evaluate(self.queries)
        self.assertGreater(result["variants"]["candidate"]["mean_ndcg_at_k"],
                           result["variants"]["baseline"]["mean_ndcg_at_k"])
        self.assertEqual(result["variants"]["candidate"]["permission_violations"], 1)
        self.assertLessEqual(result["variants"]["candidate"]["mean_ndcg_at_k"], 1)
        self.assertFalse(result["candidate_release_gate"])

    def test_perfect_permitted_ranking_has_unit_ndcg(self):
        result = evaluate(self.queries)
        q1 = result["variants"]["candidate"]["queries"][0]
        self.assertEqual(q1["ndcg_at_k"], 1.0)

    def test_duplicate_or_unknown_document_rejected(self):
        changed = json.loads(json.dumps(self.queries))
        changed[0]["candidate"] = ["d1", "d1"]
        with self.assertRaises(ValueError):
            evaluate(changed)
        changed = json.loads(json.dumps(self.queries))
        changed[0]["candidate"] = ["unknown"]
        with self.assertRaises(ValueError):
            evaluate(changed)


if __name__ == "__main__":
    unittest.main()
