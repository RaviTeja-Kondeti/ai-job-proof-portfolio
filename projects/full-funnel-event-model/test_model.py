import importlib.util
import sys
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("funnel_model", Path(__file__).with_name("model.py"))
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


class FunnelTests(unittest.TestCase):
    def setUp(self):
        self.users, self.events = module.fixture()
        self.report = module.run(self.users, self.events, "2026-04-15T00:00:00Z")
        self.rows = {(x["cohort_month"], x["segment"], x["market"]): x
                     for x in self.report["cohorts"]}

    def test_corrected_event_not_early_activation(self):
        group = self.rows[("2026-01", "consumer", "US")]
        self.assertEqual((group["acquired"], group["activated"],
                          group["retention_eligible"], group["retained"],
                          group["expanded"]), (2, 1, 1, 1, 1))

    def test_consent_excludes_unconsented_signup_and_retention(self):
        business = self.rows[("2026-01", "business", "US")]
        self.assertEqual(business["acquired"], 1)  # u7 is excluded
        uk = self.rows[("2026-01", "consumer", "UK")]
        self.assertEqual((uk["retention_eligible"], uk["retained"]), (1, 0))
        self.assertEqual(self.report["input_audit"]["events_without_analytics_consent"], 3)

    def test_immature_cohort_has_null_retention_rate(self):
        group = self.rows[("2026-03", "consumer", "US")]
        self.assertEqual((group["acquired"], group["activated"],
                          group["retention_eligible"]), (1, 1, 0))
        self.assertIsNone(group["eligible_retention_rate"])

    def test_segment_and_market_are_not_collapsed(self):
        self.assertEqual(len(self.rows), 5)
        self.assertEqual(self.rows[("2026-02", "business", "UK")]["expanded"], 1)

    def test_invalid_or_orphan_event_fails(self):
        with self.assertRaises(ValueError):
            module.run(self.users, self.events + [{**self.events[0], "user_id": "absent"}],
                       "2026-04-15T00:00:00Z")
        with self.assertRaises(ValueError):
            module.run(self.users, self.events + [{**self.events[0], "email": "x"}],
                       "2026-04-15T00:00:00Z")
        with self.assertRaises(ValueError):
            module.run(self.users, self.events + [dict(self.events[0])],
                       "2026-04-15T00:00:00Z")

    def test_late_correction_is_not_seen_before_receipt(self):
        delayed = [dict(event) for event in self.events]
        correction = [event for event in delayed if event["event_id"] == "a2"
                      and event["event_at"].startswith("2026-01-15")][0]
        correction["received_at"] = "2026-04-16T00:00:00Z"
        rows = module.run(self.users, delayed, "2026-04-15T00:00:00Z")["cohorts"]
        group = [x for x in rows if (x["cohort_month"], x["segment"], x["market"])
                 == ("2026-01", "consumer", "US")][0]
        self.assertEqual(group["activated"], 2)

    def test_newer_consent_revocation_suppresses_event(self):
        revoked = self.events + [{**self.events[0], "received_at": "2026-04-01T00:00:00Z",
                                  "consent": False}]
        rows = module.run(self.users, revoked, "2026-04-15T00:00:00Z")["cohorts"]
        group = [x for x in rows if (x["cohort_month"], x["segment"], x["market"])
                 == ("2026-01", "consumer", "US")][0]
        self.assertEqual((group["acquired"], group["activated"]), (1, 0))

    def test_equivalent_timezone_offsets_do_not_change_cohorts(self):
        shifted = [dict(event) for event in self.events]
        shifted[0]["event_at"] = "2025-12-31T19:00:00-05:00"
        shifted[0]["received_at"] = "2026-01-01T07:00:00-05:00"
        result = module.run(self.users, shifted, "2026-04-14T20:00:00-04:00")
        self.assertEqual(result["cohorts"], self.report["cohorts"])


if __name__ == "__main__":
    unittest.main()
