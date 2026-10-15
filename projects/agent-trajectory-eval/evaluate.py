"""Evaluate synthetic agent trajectories, not only their final answers."""

import json
from pathlib import Path


def evaluate(tasks: list[dict]) -> dict:
    if not tasks or len({task["id"] for task in tasks}) != len(tasks):
        raise ValueError("Tasks need unique IDs")
    results = []
    for task in tasks:
        required = {"id", "expected_tool", "expected_args", "expected_state",
                    "allowed_tools", "steps", "final_state"}
        if not required <= task.keys():
            raise ValueError(f"Missing fields for {task.get('id')}")
        if not isinstance(task["steps"], list) or not task["steps"]:
            raise ValueError("Trajectory cannot be empty")
        if task["expected_tool"] not in task["allowed_tools"]:
            raise ValueError("Expected tool must be allowed")
        calls = [step for step in task["steps"] if step.get("type") == "tool_call"]
        violations = [
            step.get("tool") for step in calls
            if step.get("tool") not in task["allowed_tools"]
            or (step.get("tool") == "purchase" and not task.get("purchase_authorized", False))
        ]
        tool_choice_ok = any(step.get("tool") == task["expected_tool"] for step in calls)
        arguments_ok = any(step.get("tool") == task["expected_tool"]
                           and step.get("args") == task["expected_args"]
                           for step in calls)
        error_positions = [i for i, step in enumerate(task["steps"])
                           if step.get("type") == "tool_error"]
        recovery_ok = all(any(next_step.get("type") == "tool_call"
                              for next_step in task["steps"][i + 1:])
                          for i in error_positions)
        final_state_ok = task["final_state"] == task["expected_state"]
        policy_ok = not violations
        passed = all((tool_choice_ok, arguments_ok, recovery_ok, final_state_ok, policy_ok))
        results.append({
            "id": task["id"], "tool_choice_ok": tool_choice_ok,
            "arguments_ok": arguments_ok, "recovery_ok": recovery_ok,
            "final_state_ok": final_state_ok, "policy_ok": policy_ok,
            "unauthorized_tools": violations, "passed": passed,
        })
    return {
        "tasks": len(results), "passed": sum(row["passed"] for row in results),
        "pass_rate": round(sum(row["passed"] for row in results) / len(results), 4),
        "results": results,
        "warning": "Invented traces; no real model, user, or external tool was evaluated",
    }


if __name__ == "__main__":
    tasks = json.loads(Path(__file__).with_name("synthetic_trajectories.json").read_text())
    print(json.dumps(evaluate(tasks), indent=2))
