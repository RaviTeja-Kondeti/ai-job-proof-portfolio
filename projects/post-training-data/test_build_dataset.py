import json
from pathlib import Path
import unittest
from build_dataset import build_manifest


class DataBuildTests(unittest.TestCase):
    def setUp(self):
        self.rows = json.loads(Path(__file__).with_name("synthetic_records.json").read_text())

    def test_manifest_is_order_independent_and_counts_all_types(self):
        first = build_manifest(self.rows)
        second = build_manifest(list(reversed(self.rows)))
        self.assertEqual(first, second)
        self.assertEqual(first["type_counts"], {"sft": 2, "preference": 2, "rl": 2})

    def test_missing_provenance_and_duplicate_id_block_release(self):
        rows = json.loads(json.dumps(self.rows))
        del rows[0]["source"]
        with self.assertRaises(ValueError):
            build_manifest(rows)
        with self.assertRaises(ValueError):
            build_manifest(self.rows + [self.rows[0]])

    def test_invalid_preference_pair_blocks_release(self):
        rows = json.loads(json.dumps(self.rows))
        rows[2]["rejected"] = rows[2]["chosen"]
        with self.assertRaises(ValueError):
            build_manifest(rows)


if __name__ == "__main__":
    unittest.main()
