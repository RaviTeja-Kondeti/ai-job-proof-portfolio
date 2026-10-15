"""Synthetic backtest of a delayed-feedback marketing allocation policy."""

import json
import math
from pathlib import Path


CHANNELS = ("search", "social")
BUDGET = 100
MIN_SPEND = 20
MAX_SPEND = 80
MAX_WEEKLY_CHANGE = 20


def reward(spend: int, rate: float) -> float:
    """Invented saturating incremental value; rate is known only to simulator."""
    return rate * 40 * math.log1p(spend / 40)


def choose_allocation(previous: dict[str, float] | None,
                      prior_allocation: dict[str, int]) -> dict[str, int]:
    """Policy receives only the preceding week's noisy rate estimates."""
    if previous is None:
        return {"search": 50, "social": 50}
    best = max(CHANNELS, key=lambda channel: (previous[channel], channel))
    other = next(channel for channel in CHANNELS if channel != best)
    new_best = min(MAX_SPEND, prior_allocation[best] + MAX_WEEKLY_CHANGE)
    new_other = BUDGET - new_best
    if new_other < MIN_SPEND:
        new_other = MIN_SPEND
        new_best = BUDGET - new_other
    return {best: new_best, other: new_other}


def backtest(weeks: list[dict]) -> dict:
    if not weeks or len({row["week"] for row in weeks}) != len(weeks):
        raise ValueError("History needs unique week IDs")
    prior_signals = None
    prior_allocation = {"search": 50, "social": 50}
    rows = []
    for week in sorted(weeks, key=lambda row: row["week"]):
        if set(week["true_rates"]) != set(CHANNELS) or set(week["observed_rates"]) != set(CHANNELS):
            raise ValueError("Each week needs both channels")
        if any(value < 0 or not math.isfinite(value)
               for section in ("true_rates", "observed_rates")
               for value in week[section].values()):
            raise ValueError("Rates must be finite and nonnegative")
        allocation = choose_allocation(prior_signals, prior_allocation)
        if sum(allocation.values()) != BUDGET:
            raise AssertionError("Policy exceeded budget")
        policy_value = sum(reward(allocation[c], week["true_rates"][c]) for c in CHANNELS)
        baseline_value = sum(reward(50, week["true_rates"][c]) for c in CHANNELS)
        rows.append({
            "week": week["week"],
            "allocation": allocation,
            "observed_input_from_previous_week": prior_signals,
            "policy_incremental_value": round(policy_value, 3),
            "fixed_split_incremental_value": round(baseline_value, 3),
        })
        prior_signals = week["observed_rates"]
        prior_allocation = allocation
    policy_total = sum(row["policy_incremental_value"] for row in rows)
    baseline_total = sum(row["fixed_split_incremental_value"] for row in rows)
    return {
        "weeks": rows,
        "policy_total": round(policy_total, 3),
        "fixed_split_total": round(baseline_total, 3),
        "difference": round(policy_total - baseline_total, 3),
        "warning": "Synthetic response curves reveal counterfactuals; observational data would not",
    }


if __name__ == "__main__":
    weeks = json.loads(Path(__file__).with_name("synthetic_history.json").read_text())
    print(json.dumps(backtest(weeks), indent=2))
