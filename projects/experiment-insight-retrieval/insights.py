"""Traceable synthetic cross-experiment retrieval with conservative abstention."""

import json
import math
from collections import Counter
from pathlib import Path


def validate(experiments: list[dict]) -> None:
    if not experiments or len({e["id"] for e in experiments}) != len(experiments):
        raise ValueError("Need nonempty, unique experiment IDs")
    for experiment in experiments:
        if (not experiment["source_ref"] or not experiment["dataset_version"] or
                type(experiment["end_day"]) is not int or
                type(experiment["effect"]) not in (int, float) or
                not math.isfinite(experiment["effect"]) or
                type(experiment["standard_error"]) not in (int, float) or
                not math.isfinite(experiment["standard_error"]) or
                experiment["standard_error"] <= 0 or
                type(experiment["validity_passed"]) is not bool or
                type(experiment["randomized"]) is not bool):
            raise ValueError(f"Invalid experiment: {experiment['id']}")


def summarize(experiments: list[dict], query: dict,
              as_of_day: int = 500, max_age: int = 180) -> dict:
    """Retrieve only authorized, valid, fresh experiments; never auto-act."""
    validate(experiments)
    if max_age < 0 or not query.get("scope"):
        raise ValueError("Need a permission scope and nonnegative max age")
    excluded = Counter()
    eligible = []
    for experiment in experiments:
        if experiment["scope"] != query["scope"]:
            continue  # Do not reveal existence/count of restricted records.
        elif (experiment["intervention"] != query["intervention"] or
              experiment["metric"] != query["metric"] or
              experiment["segment"] != query["segment"]):
            excluded["not_relevant"] += 1
        elif not experiment["validity_passed"] or not experiment["randomized"]:
            excluded["invalid_design"] += 1
        elif not 0 <= as_of_day - experiment["end_day"] <= max_age:
            excluded["stale_or_future"] += 1
        else:
            eligible.append(experiment)
    eligible.sort(key=lambda e: e["id"])
    evidence = [{"id": e["id"], "source_ref": e["source_ref"],
                 "dataset_version": e["dataset_version"],
                 "effect": e["effect"], "standard_error": e["standard_error"]}
                for e in eligible]
    output = {"query": query, "eligible_evidence": evidence,
              "excluded_by_reason": dict(sorted(excluded.items())),
              "requires_human_approval": True,
              "next_action": "abstain", "pooled_effect": None,
              "approx_95pct_interval": None,
              "reason": "Need at least two independent eligible experiments"}
    if len(eligible) < 2:
        return output
    positive = any(e["effect"] - 1.96 * e["standard_error"] > 0 for e in eligible)
    negative = any(e["effect"] + 1.96 * e["standard_error"] < 0 for e in eligible)
    if positive and negative:
        output["reason"] = "Credible effects conflict across historical experiments"
        return output
    weights = [1 / e["standard_error"] ** 2 for e in eligible]
    pooled = sum(e["effect"] * weight for e, weight in zip(eligible, weights)) / sum(weights)
    pooled_se = math.sqrt(1 / sum(weights))
    low, high = pooled - 1.96 * pooled_se, pooled + 1.96 * pooled_se
    output["pooled_effect"] = round(pooled, 5)
    output["approx_95pct_interval"] = [round(low, 5), round(high, 5)]
    if low > 0:
        output["next_action"] = "propose_live_experiment_for_review"
        output["reason"] = "Historical evidence suggests positive effect; causal transfer unverified"
    else:
        output["reason"] = "Historical evidence too uncertain for a directional hypothesis"
    return output


if __name__ == "__main__":
    fixture = json.loads(Path(__file__).with_name("synthetic_experiments.json").read_text())
    for query in fixture["queries"]:
        print(json.dumps(summarize(fixture["experiments"], query), indent=2))
