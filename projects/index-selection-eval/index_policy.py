"""Synthetic budgeted web-index selection with a hidden downstream outcome."""

import json
from pathlib import Path


def validate(data: dict) -> None:
    pages = data["pages"]
    if not pages or len({p["id"] for p in pages}) != len(pages):
        raise ValueError("Need unique, nonempty page IDs")
    if type(data["budget"]) is not int or data["budget"] < 1:
        raise ValueError("Budget must be a positive integer")
    queries = data["query_weights"]
    if not queries or any(type(w) not in (int, float) or w <= 0
                          for w in queries.values()):
        raise ValueError("Need positive query weights")
    for page in pages:
        if (type(page["cost"]) is not int or page["cost"] < 1 or
                type(page["predicted_value"]) not in (int, float) or
                page["predicted_value"] < 0 or
                type(page["freshness"]) not in (int, float) or
                not 0 <= page["freshness"] <= 1 or
                not page["duplicate_cluster"] or
                not set(page["true_query_coverage"]) <= queries.keys()):
            raise ValueError(f"Invalid page: {page['id']}")


def select(pages: list[dict], budget: int, candidate: bool) -> list[str]:
    """Use predicted signals only; ground-truth coverage never enters selection."""
    if candidate:
        ordered = sorted(pages, key=lambda p: (-p["predicted_value"]
                                                * p["freshness"] / p["cost"], p["id"]))
    else:
        ordered = sorted(pages, key=lambda p: (-p["predicted_value"], p["id"]))
    selected = []
    used_clusters = set()
    spent = 0
    for page in ordered:
        if spent + page["cost"] > budget:
            continue
        if candidate and page["duplicate_cluster"] in used_clusters:
            continue
        selected.append(page["id"])
        spent += page["cost"]
        used_clusters.add(page["duplicate_cluster"])
    return selected


def evaluate(data: dict) -> dict:
    validate(data)
    by_id = {page["id"]: page for page in data["pages"]}
    total_weight = sum(data["query_weights"].values())
    report = {}
    for name, candidate in (("value_threshold", False), ("freshness_dedup_budget", True)):
        selected = select(data["pages"], data["budget"], candidate)
        pages = [by_id[page_id] for page_id in selected]
        covered = set().union(*(p["true_query_coverage"] for p in pages))
        report[name] = {
            "selected": selected,
            "cost": sum(p["cost"] for p in pages),
            "duplicate_pages": len(pages) - len({p["duplicate_cluster"] for p in pages}),
            "weighted_query_coverage": round(sum(data["query_weights"][q] for q in covered)
                                             / total_weight, 4),
            "covered_queries": sorted(covered),
        }
    return {
        "budget": data["budget"], "policies": report,
        "candidate_improves_coverage": (
            report["freshness_dedup_budget"]["weighted_query_coverage"] >
            report["value_threshold"]["weighted_query_coverage"]),
        "warning": "Invented signals and outcomes; no web-scale or live-search evidence",
    }


if __name__ == "__main__":
    data = json.loads(Path(__file__).with_name("synthetic_pages.json").read_text())
    print(json.dumps(evaluate(data), indent=2))
