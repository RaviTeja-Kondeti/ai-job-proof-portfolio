"""Randomized holdout for distinguishing observed outcomes from incremental lift."""

from dataclasses import dataclass
import json
import math
import random


@dataclass(frozen=True)
class Estimate:
    treatment_rate: float
    control_rate: float
    incremental_rate: float
    standard_error: float
    ci_low: float
    ci_high: float
    treated_users: int
    control_users: int


def simulate(n: int = 50000, baseline_rate: float = 0.08,
             incremental_rate: float = 0.02, seed: int = 11) -> list[tuple[int, int]]:
    """Generate synthetic potential outcomes with randomized treatment."""
    if n < 2 or not 0 <= baseline_rate <= 1 or not 0 <= baseline_rate + incremental_rate <= 1:
        raise ValueError("Invalid simulation parameters")
    rng = random.Random(seed)
    rows = []
    for _ in range(n):
        treated = rng.randrange(2)
        converted = int(rng.random() < baseline_rate + treated * incremental_rate)
        rows.append((treated, converted))
    return rows


def estimate(rows: list[tuple[int, int]]) -> Estimate:
    counts = [0, 0]
    conversions = [0, 0]
    for treated, converted in rows:
        if treated not in (0, 1) or converted not in (0, 1):
            raise ValueError("Rows must contain binary treatment and outcome")
        counts[treated] += 1
        conversions[treated] += converted
    if min(counts) < 2:
        raise ValueError("Each randomized group needs at least two users")
    rates = [conversions[i] / counts[i] for i in (0, 1)]
    standard_error = math.sqrt(sum(rates[i] * (1 - rates[i]) / counts[i] for i in (0, 1)))
    lift = rates[1] - rates[0]
    return Estimate(rates[1], rates[0], lift, standard_error,
                    lift - 1.96 * standard_error, lift + 1.96 * standard_error,
                    counts[1], counts[0])


def demo() -> dict:
    result = estimate(simulate())
    return {
        "assumption": "Synthetic randomized users; 2 percentage points of programmed lift",
        "treated_conversion_rate": round(result.treatment_rate, 4),
        "control_conversion_rate": round(result.control_rate, 4),
        "estimated_incremental_rate": round(result.incremental_rate, 4),
        "approximate_95_percent_ci": [round(result.ci_low, 4), round(result.ci_high, 4)],
        "point": "The treatment group's conversions are not all incremental; use the holdout difference",
    }


if __name__ == "__main__":
    print(json.dumps(demo(), indent=2))
