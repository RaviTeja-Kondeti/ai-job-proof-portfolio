import importlib.util
import sys
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("task_queue", Path(__file__).with_name("queue.py"))
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


class QueueTests(unittest.TestCase):
    def test_idempotent_same_payload_and_conflict(self):
        q = module.TaskQueue()
        self.assertTrue(q.enqueue("a", {"x": 1}, 0))
        self.assertFalse(q.enqueue("a", {"x": 1}, 0))
        with self.assertRaises(ValueError):
            q.enqueue("a", {"x": 2}, 0)
        self.assertEqual(q.snapshot()["status_counts"], {"queued": 1})

    def test_backpressure_retry_and_cost(self):
        result = module.demo()
        self.assertTrue(result["events"][1]["backpressure"])
        self.assertEqual(result["events"][2]["failure"],
                         {"status": "retry", "retry_at": 2})
        self.assertEqual(result["final"], {"status_counts": {"done": 2},
                                           "tokens": 22, "cost_microusd": 440})

    def test_stale_worker_cannot_commit_after_reclaim(self):
        q = module.TaskQueue(max_inflight=1, lease_seconds=5)
        q.enqueue("a", {}, 0)
        old = q.claim(0)
        new = q.claim(5)
        self.assertEqual(new["attempt"], 2)
        with self.assertRaises(ValueError):
            q.complete("a", old["attempt"], {}, 1, 1, 6)
        q.complete("a", new["attempt"], {}, 1, 1, 6)
        self.assertEqual(q.snapshot()["status_counts"], {"done": 1})

    def test_retry_waits_until_due(self):
        q = module.TaskQueue()
        q.enqueue("a", {}, 0)
        lease = q.claim(0)
        q.fail("a", lease["attempt"], "temporary", 1)
        self.assertIsNone(q.claim(1))
        self.assertEqual(q.claim(2)["attempt"], 2)

    def test_exhausted_attempts_dead_letter(self):
        q = module.TaskQueue(max_attempts=2)
        q.enqueue("a", {}, 0)
        first = q.claim(0)
        q.fail("a", first["attempt"], "temporary", 1)
        second = q.claim(2)
        self.assertEqual(q.fail("a", second["attempt"], "persistent", 3),
                         {"status": "dead", "retry_at": None})
        self.assertIsNone(q.claim(100))
        self.assertEqual(q.snapshot()["status_counts"], {"dead": 1})

    def test_expired_final_lease_dead_letters(self):
        q = module.TaskQueue(max_attempts=1, lease_seconds=5)
        q.enqueue("a", {}, 0)
        q.claim(0)
        self.assertIsNone(q.claim(5))
        self.assertEqual(q.snapshot()["status_counts"], {"dead": 1})

    def test_invalid_lease_cannot_double_charge(self):
        q = module.TaskQueue()
        q.enqueue("a", {}, 0)
        lease = q.claim(0)
        q.complete("a", lease["attempt"], {}, 3, 20, 1)
        with self.assertRaises(ValueError):
            q.complete("a", lease["attempt"], {}, 3, 20, 1)
        self.assertEqual(q.snapshot()["cost_microusd"], 60)


if __name__ == "__main__":
    unittest.main()
