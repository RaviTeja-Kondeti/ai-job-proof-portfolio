import importlib.util
import sys
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("joint_orchestrator", Path(__file__).with_name("orchestrate.py"))
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


class JointDecisionTests(unittest.TestCase):
    def setUp(self):
        self.campaigns = [
            module.allocator.Campaign("a", "US", "search", 180, .003, 12, 300, 2000),
            module.allocator.Campaign("b", "US", "social", 140, .002, 18, 300, 2000),
        ]
        self.previous = {"a": 1000, "b": 1000}

    def test_demo_respects_total_budget_and_stale_fallback(self):
        report = module.demo()
        trace = report["trace"]
        self.assertEqual(len(trace), 3)
        self.assertTrue(all(day["status"] == "allocated" for day in trace))
        self.assertEqual(sum(day["total_spend"] for day in trace) +
                         report["unspent_budget"], report["initial_budget"])
        self.assertLess(trace[1]["allocation"]["social_us"],
                        trace[0]["allocation"]["social_us"])
        self.assertGreaterEqual(trace[1]["allocation"]["social_us"],
                                0.8 * trace[0]["allocation"]["social_us"])
        self.assertEqual(trace[1]["signals"]["social_us"]["reason"],
                         "safe_fallback_stale_or_invalid_feedback")

    def test_healthy_campaigns_stay_within_daily_change_and_caps(self):
        observations = {"a": module.pacer.Observation(1.8, 0),
                        "b": module.pacer.Observation(0.5, 0)}
        result = module.plan_day(self.campaigns, self.previous, observations, 5000)
        for name, spend in result["allocation"].items():
            self.assertGreaterEqual(spend, 800)
            self.assertLessEqual(spend, 1200)
            self.assertEqual(spend % 100, 0)

    def test_budget_below_required_floors_pauses(self):
        observations = {name: module.pacer.Observation(1.2, 0)
                        for name in self.previous}
        result = module.plan_day(self.campaigns, self.previous, observations, 1000)
        self.assertEqual(result["status"], "paused_infeasible")
        self.assertEqual(result["allocation"], {"a": 0, "b": 0})

    def test_invalid_feedback_contract_rejected(self):
        with self.assertRaises(ValueError):
            module.plan_day(self.campaigns, self.previous, {"a": None, "b": None}, 5000)


if __name__ == "__main__":
    unittest.main()
