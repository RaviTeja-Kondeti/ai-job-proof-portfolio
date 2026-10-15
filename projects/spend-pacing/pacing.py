"""Synthetic paid-marketing pacing controller with explicit safe fallback."""

from dataclasses import dataclass
import json
import math


@dataclass(frozen=True)
class Observation:
    roi: float | None
    age_days: int


@dataclass(frozen=True)
class Decision:
    spend: float
    reason: str


def next_spend(previous: float, observation: Observation, target_roi: float,
               daily_cap: float, remaining_budget: float, gain: float = 0.4,
               max_daily_change: float = 0.2, stale_after_days: int = 2) -> Decision:
    """Update spend gradually; reduce it when the feedback is missing or stale."""
    if min(previous, target_roi, daily_cap, remaining_budget, gain,
           max_daily_change) < 0 or target_roi == 0:
        raise ValueError("Spend controls must be nonnegative and target ROI positive")
    if observation.age_days < 0:
        raise ValueError("Feedback age cannot be negative")
    if (observation.roi is None or not math.isfinite(observation.roi)
            or observation.roi < 0 or observation.age_days > stale_after_days):
        proposed = previous * (1 - max_daily_change)
        reason = "safe_fallback_stale_or_invalid_feedback"
    else:
        error = (observation.roi - target_roi) / target_roi
        change = max(-max_daily_change, min(max_daily_change, gain * error))
        proposed = previous * (1 + change)
        reason = "controlled_roi_response"
    return Decision(round(max(0.0, min(proposed, daily_cap, remaining_budget)), 2), reason)


def demo() -> dict:
    observations = [Observation(1.1, 0), Observation(1.5, 1), Observation(None, 3),
                    Observation(0.7, 1), Observation(1.3, 0)]
    spend = 1000.0
    budget = 5000.0
    trace = []
    for day, observation in enumerate(observations, start=1):
        decision = next_spend(spend, observation, 1.2, 1300, budget)
        trace.append({"day": day, "observed_roi": observation.roi,
                      "feedback_age_days": observation.age_days,
                      "spend": decision.spend, "reason": decision.reason})
        spend = decision.spend
        budget -= spend
    return {"assumption": "Synthetic ROI feedback, not real campaign performance",
            "unspent_budget": round(budget, 2), "trace": trace}


if __name__ == "__main__":
    print(json.dumps(demo(), indent=2))
