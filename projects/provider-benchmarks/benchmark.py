"""Reproducible benchmark for synthetic data providers across task domains."""

from collections import defaultdict
import json
import math
from pathlib import Path


def percentile_95(values: list[float]) -> float:
    if not values:
        raise ValueError("Latency series cannot be empty")
    ordered = sorted(values)
    return ordered[math.ceil(0.95 * len(ordered)) - 1]


def evaluate(cases: list[dict]) -> dict:
    if not cases or len({case["id"] for case in cases}) != len(cases):
        raise ValueError("Benchmark tasks must have unique IDs")
    grouped = defaultdict(list)
    domains = set()
    for case in cases:
        domain = case["domain"]
        domains.add(domain)
        providers = case["providers"]
        if not providers:
            raise ValueError(f"No providers for {case['id']}")
        for provider, result in providers.items():
            if result["latency_ms"] < 0 or result["cost_usd"] < 0:
                raise ValueError("Latency and cost must be nonnegative")
            grouped[(domain, provider)].append({
                "correct": result["answer"] == case["ground_truth"],
                "answered": bool(result["answer"]),
                "latency_ms": result["latency_ms"],
                "cost_usd": result["cost_usd"],
            })
    expected_counts = {domain: sum(case["domain"] == domain for case in cases)
                       for domain in domains}
    report = {}
    for (domain, provider), rows in sorted(grouped.items()):
        if len(rows) != expected_counts[domain]:
            raise ValueError(f"Provider {provider} missing a response in {domain}")
        report.setdefault(domain, {})[provider] = {
            "tasks": len(rows),
            "accuracy": round(sum(row["correct"] for row in rows) / len(rows), 3),
            "coverage": round(sum(row["answered"] for row in rows) / len(rows), 3),
            "p95_latency_ms": percentile_95([row["latency_ms"] for row in rows]),
            "mean_cost_usd": round(sum(row["cost_usd"] for row in rows) / len(rows), 4),
        }
    # Fix the decision rule before looking at provider names or outcomes.
    selected = {}
    for domain, providers in report.items():
        selected[domain] = max(
            providers,
            key=lambda name: (providers[name]["accuracy"],
                              providers[name]["coverage"],
                              -providers[name]["p95_latency_ms"],
                              -providers[name]["mean_cost_usd"], name),
        )
    return {"results": report, "selected_provider_by_domain": selected,
            "selection_rule": "Highest accuracy, then coverage, then lower p95 latency and cost",
            "warning": "Synthetic providers and tiny task sets; no claim about real vendor performance"}


if __name__ == "__main__":
    cases = json.loads(Path(__file__).with_name("synthetic_tasks.json").read_text())
    print(json.dumps(evaluate(cases), indent=2))
