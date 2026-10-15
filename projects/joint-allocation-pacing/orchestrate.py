"""Compose a bounded spend controller with a constrained marginal-return allocator."""

from dataclasses import replace
import importlib.util
import json
import math
from pathlib import Path
import sys


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ROOT = Path(__file__).resolve().parents[1]
allocator = _load("joint_budget_allocator", ROOT / "budget-allocation" / "allocate.py")
pacer = _load("joint_spend_pacer", ROOT / "spend-pacing" / "pacing.py")


def _grid_floor(value, step):
    return math.floor(value / step + 1e-9) * step


def _grid_ceil(value, step):
    return math.ceil(value / step - 1e-9) * step


def plan_day(campaigns, previous, observations, remaining_budget, target_roi=1.2,
             step=100, max_daily_change=0.2, uncertainty_weight=1.0):
    names = {campaign.name for campaign in campaigns}
    if (not campaigns or len(names) != len(campaigns)
            or set(previous) != names or set(observations) != names
            or not isinstance(remaining_budget, int) or remaining_budget < 0
            or step <= 0 or remaining_budget % step
            or not 0 < max_daily_change < 1):
        raise ValueError("Invalid campaign, feedback, or budget contract")
    if any(not isinstance(previous[name], int) or previous[name] < 0
           or previous[name] % step for name in names):
        raise ValueError("Previous spend must be a nonnegative grid amount")

    envelopes = []
    signals = {}
    for campaign in campaigns:
        name = campaign.name
        obs = observations[name]
        if not isinstance(obs, pacer.Observation):
            raise ValueError("Observations must have ROI and age")
        decision = pacer.next_spend(previous[name], obs, target_roi,
                                    campaign.maximum, remaining_budget,
                                    max_daily_change=max_daily_change)
        stale = decision.reason == "safe_fallback_stale_or_invalid_feedback"
        if stale:
            fallback = _grid_ceil(previous[name] * (1-max_daily_change), step)
            lower = max(campaign.minimum, fallback)
            upper = min(campaign.maximum, fallback)
        else:
            lower = max(campaign.minimum,
                        _grid_ceil(previous[name] * (1-max_daily_change), step))
            upper = min(campaign.maximum,
                        _grid_floor(previous[name] * (1+max_daily_change), step))
        if lower > upper:
            return {"status": "paused_infeasible", "reason": f"{name}: floor exceeds safe cap",
                    "allocation": {item.name: 0 for item in campaigns}}
        envelopes.append(replace(campaign, minimum=lower, maximum=upper))
        signals[name] = {"observed_roi": obs.roi, "feedback_age_days": obs.age_days,
                         "raw_pacing_proposal": decision.spend, "reason": decision.reason,
                         "minimum": lower, "maximum": upper}

    floor_total = sum(c.minimum for c in envelopes)
    ceiling_total = min(remaining_budget, sum(c.maximum for c in envelopes))
    if floor_total > ceiling_total:
        return {"status": "paused_infeasible", "reason": "budget below safe campaign floors",
                "allocation": {item.name: 0 for item in campaigns}}
    proposed_total = round(sum(item["raw_pacing_proposal"] for item in signals.values()) / step) * step
    target_total = max(floor_total, min(ceiling_total, proposed_total))
    selected = allocator.allocate(envelopes, target_total, step=step,
                                  uncertainty_weight=uncertainty_weight)
    return {"status": "allocated", "allocation": selected, "total_spend": sum(selected.values()),
            "remaining_after": remaining_budget-sum(selected.values()),
            "signals": signals,
            "risk_adjusted_assumed_value": round(sum(
                campaign.value(selected[campaign.name], uncertainty_weight)
                for campaign in campaigns), 4)}


def demo():
    campaigns = [
        allocator.Campaign("search_us", "US", "search", 180, .003, 12, 300, 2000),
        allocator.Campaign("social_us", "US", "social", 145, .002, 18, 300, 2000),
        allocator.Campaign("search_eu", "EU", "search", 130, .004, 8, 300, 2000),
    ]
    previous = {campaign.name: 1000 for campaign in campaigns}
    feedback = [
        {"search_us": pacer.Observation(1.4, 0),
         "social_us": pacer.Observation(1.0, 0), "search_eu": pacer.Observation(1.1, 0)},
        {"search_us": pacer.Observation(1.5, 1),
         "social_us": pacer.Observation(None, 3), "search_eu": pacer.Observation(1.2, 1)},
        {"search_us": pacer.Observation(1.3, 0),
         "social_us": pacer.Observation(1.2, 0), "search_eu": pacer.Observation(1.4, 0)},
    ]
    budget = 10000
    trace = []
    for day, observations in enumerate(feedback, 1):
        result = plan_day(campaigns, previous, observations, budget)
        trace.append({"day": day, **result})
        if result["status"] != "allocated":
            break
        previous = result["allocation"]
        budget = result["remaining_after"]
    return {"assumption": "Synthetic ROI and response curves; no causal or real ad impact",
            "initial_budget": 10000, "trace": trace, "unspent_budget": budget}


if __name__ == "__main__":
    print(json.dumps(demo(), indent=2, sort_keys=True))
