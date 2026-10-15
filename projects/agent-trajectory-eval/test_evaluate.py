import json
from pathlib import Path
import unittest
from evaluate import evaluate


class AgentTrajectoryTests(unittest.TestCase):
    def setUp(self):
        self.tasks = json.loads(Path(__file__).with_name("synthetic_trajectories.json").read_text())

    def test_correct_final_answer_cannot_hide_wrong_arguments(self):
        result = {row["id"]: row for row in evaluate(self.tasks)["results"]}
        self.assertTrue(result["wrong-argument"]["final_state_ok"])
        self.assertFalse(result["wrong-argument"]["arguments_ok"])
        self.assertFalse(result["wrong-argument"]["passed"])

    def test_unauthorized_side_effect_blocks_pass(self):
        result = {row["id"]: row for row in evaluate(self.tasks)["results"]}
        self.assertTrue(result["unauthorized-side-effect"]["final_state_ok"])
        self.assertFalse(result["unauthorized-side-effect"]["policy_ok"])
        self.assertFalse(result["unauthorized-side-effect"]["passed"])

    def test_recovery_requires_action_after_error(self):
        result = {row["id"]: row for row in evaluate(self.tasks)["results"]}
        self.assertTrue(result["recovered-timeout"]["recovery_ok"])
        self.assertFalse(result["unrecovered-timeout"]["recovery_ok"])

    def test_missing_trace_and_duplicate_tasks_rejected(self):
        changed = json.loads(json.dumps(self.tasks))
        changed[0]["steps"] = []
        with self.assertRaises(ValueError):
            evaluate(changed)
        with self.assertRaises(ValueError):
            evaluate(self.tasks + [self.tasks[0]])


if __name__ == "__main__":
    unittest.main()
