"""Evaluate synthetic enterprise search rankings with permission checks."""

import json
import math
from pathlib import Path


def dcg(relevance: list[int]) -> float:
    return sum((2 ** grade - 1) / math.log2(rank + 2)
               for rank, grade in enumerate(relevance))


def evaluate(queries: list[dict], k: int = 3) -> dict:
    if k < 1 or not queries or len({q["id"] for q in queries}) != len(queries):
        raise ValueError("Need unique query IDs and positive k")
    report = {}
    for variant in ("baseline", "candidate"):
        rows = []
        for query in queries:
            relevance = query["relevance"]
            allowed = set(query["allowed"])
            ranking = query[variant]
            if not allowed <= relevance.keys() or len(ranking) != len(set(ranking)):
                raise ValueError(f"Invalid documents for {query['id']}")
            if not set(ranking) <= relevance.keys():
                raise ValueError(f"Unknown ranked document for {query['id']}")
            if any(type(value) is not int or value < 0 or value > 3
                   for value in relevance.values()):
                raise ValueError("Relevance labels must be integers 0–3")
            top = ranking[:k]
            violations = [doc for doc in top if doc not in allowed]
            # A restricted document is never a valid gain, even if relevant.
            grades = [relevance[doc] if doc in allowed else 0 for doc in top]
            ideal = sorted((relevance[doc] for doc in allowed), reverse=True)[:k]
            denominator = dcg(ideal)
            ndcg = dcg(grades) / denominator if denominator else 0
            first_relevant_rank = next((i + 1 for i, doc in enumerate(top)
                                        if relevance[doc] > 0 and doc in allowed), None)
            rows.append({
                "id": query["id"], "slice": query["slice"],
                "ndcg_at_k": round(ndcg, 4),
                "mrr_at_k": round(1 / first_relevant_rank if first_relevant_rank else 0, 4),
                "permission_violations": violations,
            })
        report[variant] = {
            "mean_ndcg_at_k": round(sum(row["ndcg_at_k"] for row in rows) / len(rows), 4),
            "permission_violations": sum(len(row["permission_violations"]) for row in rows),
            "by_slice": {
                group: round(sum(row["ndcg_at_k"] for row in rows if row["slice"] == group)
                             / sum(row["slice"] == group for row in rows), 4)
                for group in sorted({row["slice"] for row in rows})
            },
            "queries": rows,
        }
    return {
        "k": k, "variants": report,
        "candidate_release_gate": (report["candidate"]["permission_violations"] == 0
                                   and report["candidate"]["mean_ndcg_at_k"]
                                   >= report["baseline"]["mean_ndcg_at_k"]),
        "warning": "Synthetic labels and rankings; no real search model or customer data",
    }


if __name__ == "__main__":
    queries = json.loads(Path(__file__).with_name("synthetic_queries.json").read_text())
    print(json.dumps(evaluate(queries), indent=2))
