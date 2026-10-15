"""A minimal policy-gradient demonstration of reward proxy exploitation."""

from __future__ import annotations

import json
import math
import random
from statistics import mean

DATA_SEED = 20261014
TRAINING_STEPS = 1200
LEARNING_RATE = 0.20
RUN_SEEDS = tuple(range(30))


def frozen_tasks() -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    pairs = [(a, b) for a in range(1, 31) for b in range(1, 31)]
    random.Random(DATA_SEED).shuffle(pairs)
    return pairs[:200], pairs[200:300]


def response(task: tuple[int, int], exploit: bool) -> str:
    a, b = task
    return f"reason: {a + b + 1}" if exploit else str(a + b)


def proxy_reward(answer: str) -> float:
    # A deliberately bad metric: the policy can satisfy the requested format
    # while returning an incorrect answer.
    return float(answer.startswith("reason:"))


def verifier_reward(task: tuple[int, int], answer: str) -> float:
    return float(answer.strip() == str(sum(task)))


def sigmoid(value: float) -> float:
    return 1.0 / (1.0 + math.exp(-max(-30.0, min(30.0, value))))


def train(tasks: list[tuple[int, int]], reward_kind: str, seed: int) -> float:
    if not tasks or reward_kind not in {"proxy", "verifier"}:
        raise ValueError("Need training tasks and a known reward")
    rng = random.Random(seed)
    logit = 0.0  # initial probability of exploiting is 0.5
    for _ in range(TRAINING_STEPS):
        task = rng.choice(tasks)
        p_exploit = sigmoid(logit)
        exploit = rng.random() < p_exploit
        answer = response(task, exploit)
        reward = (proxy_reward(answer) if reward_kind == "proxy"
                  else verifier_reward(task, answer))
        # REINFORCE for a Bernoulli policy: grad log pi(a) = a - p.
        logit += LEARNING_RATE * reward * (float(exploit) - p_exploit)
    return sigmoid(logit)


def evaluate(tasks: list[tuple[int, int]], p_exploit: float, seed: int) -> dict:
    if not tasks or not 0 <= p_exploit <= 1:
        raise ValueError("Invalid evaluation inputs")
    rng = random.Random(seed)
    failures = 0
    proxy_hits = 0
    for task in tasks:
        answer = response(task, rng.random() < p_exploit)
        failures += int(verifier_reward(task, answer) == 0)
        proxy_hits += int(proxy_reward(answer) == 1)
    return {"tasks": len(tasks), "true_success": 1 - failures / len(tasks),
            "proxy_score": proxy_hits / len(tasks), "wrong_answers": failures}


def summarize(values: list[dict], probabilities: list[float]) -> dict:
    return {
        "runs": len(values),
        "mean_exploit_probability": mean(probabilities),
        "mean_heldout_true_success": mean(v["true_success"] for v in values),
        "mean_heldout_proxy_score": mean(v["proxy_score"] for v in values),
        "minimum_heldout_true_success": min(v["true_success"] for v in values),
        "maximum_heldout_true_success": max(v["true_success"] for v in values),
    }


def report() -> dict:
    train_tasks, test_tasks = frozen_tasks()
    policies = {}
    for name in ("untrained", "proxy", "verifier"):
        probabilities = [0.5 if name == "untrained" else train(train_tasks, name, seed)
                         for seed in RUN_SEEDS]
        observations = [evaluate(test_tasks, p, 10_000 + seed)
                        for seed, p in zip(RUN_SEEDS, probabilities)]
        policies[name] = summarize(observations, probabilities)
    return {
        "setup": {
            "data": "synthetic integer-addition tasks, disjoint train and held-out pairs",
            "train_tasks": len(train_tasks), "heldout_tasks": len(test_tasks),
            "data_seed": DATA_SEED, "run_seeds": list(RUN_SEEDS),
            "training_steps": TRAINING_STEPS, "learning_rate": LEARNING_RATE,
            "actions": "correct plain answer, or incorrect answer prefixed with 'reason:'",
            "proxy": "1 if answer starts with 'reason:', otherwise 0",
            "verifier": "1 if answer exactly equals the arithmetic solution",
        },
        "policies": policies,
    }


if __name__ == "__main__":
    print(json.dumps(report(), indent=2, sort_keys=True))
