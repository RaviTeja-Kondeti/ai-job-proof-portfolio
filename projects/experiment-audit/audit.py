"""A small, reproducible A/B experiment quality audit using only stdlib."""

import hashlib
import json
import math
import random
from pathlib import Path
from statistics import mean, variance


def assign(user_id: str, salt: str) -> str:
    digest = hashlib.sha256(f"{salt}:{user_id}".encode()).digest()
    return "treatment" if int.from_bytes(digest[:8], "big") % 2 else "control"


def synthetic_experiment(n: int = 1000, effect: float = 2.0) -> list[dict]:
    """Invented randomized users; treatment affects outcome, not pre-period."""
    rng = random.Random(20261014)
    rows = []
    for i in range(n):
        pre = rng.gauss(100, 15)
        variant = assign(str(i), "frozen-experiment-1")
        outcome = 25 + 0.75 * pre + rng.gauss(0, 9)
        if variant == "treatment":
            outcome += effect
        rows.append({"user_id": str(i), "variant": variant,
                     "pre": round(pre, 6), "outcome": round(outcome, 6),
                     "guardrail_failure": int(rng.random() < 0.04)})
    return rows


def _difference(rows: list[dict], key: str) -> tuple[float, float]:
    groups = {v: [row[key] for row in rows if row["variant"] == v]
              for v in ("control", "treatment")}
    if min(map(len, groups.values())) < 2:
        raise ValueError("Each variant needs at least two observations")
    diff = mean(groups["treatment"]) - mean(groups["control"])
    se = math.sqrt(sum(variance(values) / len(values) for values in groups.values()))
    return diff, se


def audit(rows: list[dict], planned_looks: int = 5,
          max_guardrail_increase: float = 0.01) -> dict:
    if planned_looks < 1 or not 0 <= max_guardrail_increase < 1:
        raise ValueError("Invalid preregistered settings")
    if len(rows) < 4 or len({row["user_id"] for row in rows}) != len(rows):
        raise ValueError("Rows must have unique users")
    if any(row["variant"] not in ("control", "treatment") for row in rows):
        raise ValueError("Unknown assignment")
    if any(row["guardrail_failure"] not in (0, 1) for row in rows):
        raise ValueError("Guardrail must be binary")
    if any(not all(math.isfinite(row[k]) for k in ("pre", "outcome")) for row in rows):
        raise ValueError("Metrics must be finite")

    n_t = sum(row["variant"] == "treatment" for row in rows)
    n_c = len(rows) - n_t
    # Two-sided normal approximation to a 50/50 sample-ratio test.
    srm_z = abs(n_t - n_c) / math.sqrt(len(rows))
    srm_p = math.erfc(srm_z / math.sqrt(2))

    raw_diff, raw_se = _difference(rows, "outcome")
    xbar = mean(row["pre"] for row in rows)
    ybar = mean(row["outcome"] for row in rows)
    var_x = sum((row["pre"] - xbar) ** 2 for row in rows)
    theta = (sum((row["pre"] - xbar) * (row["outcome"] - ybar)
                 for row in rows) / var_x) if var_x else 0
    adjusted = [{**row, "adjusted": row["outcome"] - theta * (row["pre"] - xbar)}
                for row in rows]
    cuped_diff, cuped_se = _difference(adjusted, "adjusted")
    # Bonferroni protects the familywise false-positive rate across planned looks.
    alpha_per_look = 0.05 / planned_looks
    p_value = math.erfc(abs(cuped_diff / cuped_se) / math.sqrt(2)) if cuped_se else 1.0
    guardrail_diff, _ = _difference(rows, "guardrail_failure")
    checks = {
        "sample_ratio_ok": srm_p >= 0.001,
        "effect_significant_at_planned_look": p_value < alpha_per_look,
        "guardrail_ok_by_point_estimate": guardrail_diff <= max_guardrail_increase,
    }
    return {
        "n": len(rows), "control_n": n_c, "treatment_n": n_t,
        "sample_ratio_p": round(srm_p, 6),
        "raw_effect": round(raw_diff, 4), "raw_se": round(raw_se, 4),
        "cuped_theta": round(theta, 4), "cuped_effect": round(cuped_diff, 4),
        "cuped_se": round(cuped_se, 4), "variance_reduction_fraction":
            round(1 - (cuped_se / raw_se) ** 2, 4) if raw_se else 0,
        "planned_looks": planned_looks, "alpha_per_look": alpha_per_look,
        "effect_p": round(p_value, 6), "guardrail_failure_rate_diff": round(guardrail_diff, 4),
        "checks": checks,
        "ship": all(checks.values()),
        "warning": "Synthetic experiment; normal approximations and a point-estimate guardrail are illustrative",
    }


if __name__ == "__main__":
    output = audit(synthetic_experiment())
    print(json.dumps(output, indent=2))
