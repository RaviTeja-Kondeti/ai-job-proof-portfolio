import importlib.util
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("reward_stress", Path(__file__).with_name("stress.py"))
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class RewardProxyTests(unittest.TestCase):
    def test_train_and_heldout_pairs_are_disjoint(self):
        train, heldout = module.frozen_tasks()
        self.assertEqual((len(train), len(heldout)), (200, 100))
        self.assertFalse(set(train) & set(heldout))

    def test_proxy_can_be_satisfied_by_wrong_answer(self):
        task = (7, 9)
        exploit = module.response(task, True)
        honest = module.response(task, False)
        self.assertEqual(module.proxy_reward(exploit), 1)
        self.assertEqual(module.verifier_reward(task, exploit), 0)
        self.assertEqual(module.proxy_reward(honest), 0)
        self.assertEqual(module.verifier_reward(task, honest), 1)

    def test_proxy_training_increases_exploitation(self):
        train, _ = module.frozen_tasks()
        self.assertGreater(module.train(train, "proxy", 0), 0.9)

    def test_verifier_training_decreases_exploitation(self):
        train, _ = module.frozen_tasks()
        self.assertLess(module.train(train, "verifier", 0), 0.1)

    def test_heldout_result_exposes_reward_hacking(self):
        report = module.report()["policies"]
        self.assertLess(report["proxy"]["mean_heldout_true_success"],
                        report["untrained"]["mean_heldout_true_success"])
        self.assertGreater(report["proxy"]["mean_heldout_proxy_score"],
                           report["untrained"]["mean_heldout_proxy_score"])
        self.assertGreater(report["verifier"]["mean_heldout_true_success"],
                           report["untrained"]["mean_heldout_true_success"])

    def test_invalid_evaluation_is_rejected(self):
        with self.assertRaises(ValueError):
            module.evaluate([(1, 2)], 1.1, 0)
        with self.assertRaises(ValueError):
            module.train([(1, 2)], "unknown", 0)


if __name__ == "__main__":
    unittest.main()
