"""Auditable evaluation of synthetic clinical note claims and citations."""

import json
from pathlib import Path


def evaluate_case(case: dict) -> dict:
    """Score exact structured facts; queue any unsafe result for human review."""
    facts = {fact["id"]: fact for fact in case["facts"]}
    expected = set(case["expected_concepts"])
    found = set()
    unsupported = []
    missing_citations = []
    for claim in case["candidate_claims"]:
        citations = claim.get("citations", [])
        if not citations:
            missing_citations.append(claim["concept"])
        matches = any(
            citation in facts
            and facts[citation]["concept"] == claim["concept"]
            and facts[citation]["value"] == claim["value"]
            for citation in citations
        )
        if matches:
            found.add(claim["concept"])
        else:
            unsupported.append({"concept": claim["concept"], "value": claim["value"]})
    omitted = sorted(expected - found)
    return {
        "case_id": case["id"],
        "supported_claims": len(case["candidate_claims"]) - len(unsupported),
        "total_claims": len(case["candidate_claims"]),
        "unsupported_claims": unsupported,
        "claims_without_citations": missing_citations,
        "omitted_expected_concepts": omitted,
        "requires_human_review": bool(unsupported or missing_citations or omitted),
    }


def evaluate_dataset(cases: list[dict]) -> dict:
    if not cases or len({case["id"] for case in cases}) != len(cases):
        raise ValueError("Dataset needs distinct, nonempty case IDs")
    per_case = [evaluate_case(case) for case in cases]
    claims = sum(item["total_claims"] for item in per_case)
    supported = sum(item["supported_claims"] for item in per_case)
    return {
        "cases": per_case,
        "claim_grounding_rate": round(supported / claims, 3) if claims else 1.0,
        "human_review_cases": sum(item["requires_human_review"] for item in per_case),
        "dataset_size": len(cases),
        "limitations": "Exact structured-fact checks only; clinical correctness still needs expert review",
    }


if __name__ == "__main__":
    data = json.loads(Path(__file__).with_name("synthetic_cases.json").read_text())
    print(json.dumps(evaluate_dataset(data), indent=2))
