import sqlite3
import unittest
from metrics import account_metrics, database


class B2BMetricsTests(unittest.TestCase):
    def test_preaggregation_avoids_cross_product_fanout(self):
        with database() as conn:
            rows = {row["account_id"]: row for row in account_metrics(conn)}
            self.assertEqual(rows["a1"]["event_count"], 2)
            self.assertEqual(rows["a1"]["open_pipeline_usd"], 10000)
            self.assertEqual(rows["a1"]["paid_revenue_usd"], 6000)
            self.assertEqual(rows["a2"]["open_pipeline_usd"], 40000)
            self.assertEqual(rows["a2"]["paid_revenue_usd"], 20000)

    def test_account_with_no_events_or_revenue_remains_in_metric_layer(self):
        with database() as conn:
            row = next(row for row in account_metrics(conn) if row["account_id"] == "a3")
            self.assertEqual(row["event_count"], 0)
            self.assertEqual(row["paid_revenue_usd"], 0)

    def test_duplicate_and_orphan_events_rejected(self):
        with database() as conn:
            with self.assertRaises(sqlite3.IntegrityError):
                conn.execute("INSERT INTO product_events VALUES ('e1','a1','agent_run','2026-09-05')")
            with self.assertRaises(sqlite3.IntegrityError):
                conn.execute("INSERT INTO product_events VALUES ('e6','missing','agent_run','2026-09-05')")


if __name__ == "__main__":
    unittest.main()
