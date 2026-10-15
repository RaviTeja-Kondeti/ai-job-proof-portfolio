"""Blocked synthetic experiment for marginal marketing-return decisions."""

import json
import math
import random
from collections import defaultdict


CHANNEL_PARAMETERS = {
    "search": (12.0, 0.015),
    "social": (10.0, 0.020),
    "video": (8.0, 0.030),
}
SPEND_LEVELS = (0, 100, 200, 300)


def response(spend: int, scale: float, rate: float) -> float:
    """Simulator-only truth; the estimator never uses these parameters."""
    return scale * math.log1p(rate * spend)


def simulate(blocks: int = 60, seed: int = 31,
             noise_sd: float = 3.0) -> list[dict]:
    if blocks < 2 or noise_sd < 0:
        raise ValueError("Need at least two blocks and nonnegative noise")
    rng = random.Random(seed)
    rows = []
    for channel, (scale, rate) in CHANNEL_PARAMETERS.items():
        for block in range(blocks):
            shared_baseline = rng.gauss(25, 6)
            arms = list(SPEND_LEVELS)
            rng.shuffle(arms)  # Each comparable subunit gets one assigned arm.
            for subunit, spend in enumerate(arms):
                rows.append({"channel": channel, "block": block,
                             "subunit": subunit, "assigned_spend": spend,
                             "outcome": round(shared_baseline + response(spend, scale, rate)
                                              + rng.gauss(0, noise_sd), 5)})
    return rows


def validate(rows: list[dict]) -> dict[str, dict[int, dict[int, float]]]:
    if not rows:
        raise ValueError("Empty experiment")
    groups = defaultdict(lambda: defaultdict(dict))
    seen_subunits = set()
    for row in rows:
        channel, block, spend = row["channel"], row["block"], row["assigned_spend"]
        key = (channel, block, row["subunit"])
        if (channel not in CHANNEL_PARAMETERS or type(block) is not int or block < 0 or
                type(row["subunit"]) is not int or row["subunit"] < 0 or
                type(spend) is not int or spend not in SPEND_LEVELS or
                type(row["outcome"]) not in (int, float) or
                not math.isfinite(row["outcome"]) or key in seen_subunits or
                spend in groups[channel][block]):
            raise ValueError("Invalid, duplicated, or non-finite experiment row")
        seen_subunits.add(key)
        groups[channel][block][spend] = row["outcome"]
    for channel in CHANNEL_PARAMETERS:
        if channel not in groups or len(groups[channel]) < 2:
            raise ValueError(f"Missing blocks for {channel}")
        for arms in groups[channel].values():
            if set(arms) != set(SPEND_LEVELS):
                raise ValueError("Every block needs all randomized spend arms")
    return groups


def bootstrap_interval(values: list[float], seed: int,
                       replicates: int = 400) -> list[float]:
    rng = random.Random(seed)
    size = len(values)
    draws = sorted(sum(values[rng.randrange(size)] for _ in range(size)) / size
                   for _ in range(replicates))
    return [round(draws[int(0.025 * replicates)], 5),
            round(draws[int(0.975 * replicates) - 1], 5)]


def estimate(rows: list[dict], current_spend: int = 100) -> dict:
    if current_spend not in SPEND_LEVELS[:-1]:
        raise ValueError("Current spend must have a next tested level")
    groups = validate(rows)
    report = {}
    for channel in sorted(CHANNEL_PARAMETERS):
        blocks = groups[channel]
        increments = []
        for index, (low, high) in enumerate(zip(SPEND_LEVELS, SPEND_LEVELS[1:])):
            differences = [blocks[block][high] - blocks[block][low]
                           for block in sorted(blocks)]
            increments.append({
                "from": low, "to": high,
                "mean_incremental_outcome": round(sum(differences) / len(differences), 5),
                "blocked_95pct_bootstrap": bootstrap_interval(differences,
                                                                seed=100 + index),
            })
        report[channel] = {"blocks": len(blocks), "marginal_steps": increments}
    next_step_index = SPEND_LEVELS.index(current_spend)
    eligible = [(channel, report[channel]["marginal_steps"][next_step_index])
                for channel in report]
    lower_bound, selected = max((step["blocked_95pct_bootstrap"][0], channel)
                                for channel, step in eligible)
    return {
        "current_spend_per_channel": current_spend,
        "next_budget_step": 100,
        "channels": report,
        "recommended_next_channel": selected if lower_bound > 0 else None,
        "decision_rule": "Largest positive bootstrap lower bound for the next $100 step; else abstain",
        "warning": "Synthetic blocked assignments; no real ad auction, causal lift, or lifetime value",
    }


if __name__ == "__main__":
    print(json.dumps(estimate(simulate()), indent=2))
