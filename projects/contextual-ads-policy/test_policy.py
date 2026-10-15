import importlib.util
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("contextual_policy", Path(__file__).with_name("policy.py"))
module = importlib.util.module_from_spec(SPEC)
import sys
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.catalog = module.synthetic_catalog()
        self.counters = module.AggregateCounters()
        self.request = {"topic": "coding", "measurement_consent": False, "max_ads": 1}

    def test_personal_fields_are_rejected(self):
        for name in ("user_id", "age", "gender", "browsing_history", "location"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                module.choose({**self.request, name: "private"}, self.catalog, self.counters)

    def test_consent_does_not_change_ranking_or_count_denied_requests(self):
        denied = module.choose(self.request, self.catalog, self.counters)
        self.assertEqual(self.counters.snapshot(), {"consenting_requests": 0, "served_ads": 0})
        accepted = module.choose({**self.request, "measurement_consent": True},
                                 self.catalog, self.counters)
        self.assertEqual(denied, accepted)
        self.assertEqual(self.counters.snapshot(), {"consenting_requests": 1, "served_ads": 1})

    def test_sensitive_context_fails_closed(self):
        for topic in ("health", "politics", "religion", "finance", "general"):
            with self.subTest(topic=topic):
                self.assertEqual(module.choose({**self.request, "topic": topic},
                                               self.catalog, self.counters), [])

    def test_unsafe_exhausted_and_irrelevant_ads_are_filtered(self):
        coding = module.choose(self.request, self.catalog, self.counters)
        music = module.choose({**self.request, "topic": "music", "max_ads": 3},
                              self.catalog, self.counters)
        self.assertNotIn("unsafe-coding", [ad.ad_id for ad in coding])
        self.assertNotIn("no-budget-music", [ad.ad_id for ad in music])
        self.assertTrue(all(module.relevance("music", ad) >= module.MIN_RELEVANCE
                            for ad in music))

    def test_contextual_relevance_gain_is_measured_with_bid_tradeoff(self):
        report = module.evaluate()["policies"]
        self.assertGreater(report["contextual"]["mean_relevance"],
                           report["bid_only"]["mean_relevance"])
        self.assertLess(report["contextual"]["mean_bid"],
                        report["bid_only"]["mean_bid"])

    def test_invalid_type_and_budget_are_rejected(self):
        with self.assertRaises(ValueError):
            module.choose({**self.request, "measurement_consent": 1},
                          self.catalog, self.counters)
        with self.assertRaises(ValueError):
            module.Ad("bad", "x", "coding", 1, 0.9, -1, True)


if __name__ == "__main__":
    unittest.main()
