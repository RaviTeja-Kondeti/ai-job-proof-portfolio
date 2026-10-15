"""Toy abuse triage, human review, enforcement, and audit trail."""

import json
from pathlib import Path


def validate(cases: list[dict], truth: dict[str, bool]) -> None:
    if not cases or len({case["id"] for case in cases}) != len(cases):
        raise ValueError("Need nonempty unique case IDs")
    if set(truth) != {case["id"] for case in cases} or any(
            type(label) is not bool for label in truth.values()):
        raise ValueError("Need one evaluation label per case")
    for case in cases:
        if (type(case["score"]) not in (int, float) or
                not 0 <= case["score"] <= 1 or
                type(case["severity"]) is not int or
                not 1 <= case["severity"] <= 5 or
                not case["account"] or not case["signals"]):
            raise ValueError(f"Invalid case: {case['id']}")


def propose(cases: list[dict], capacity: int, risk_weighted: bool) -> list[str]:
    """The selection path never reads evaluation labels or reviewer decisions."""
    if type(capacity) is not int or capacity < 1:
        raise ValueError("Review capacity must be positive")
    eligible = [case for case in cases if case["score"] >= 0.65]
    if risk_weighted:
        eligible.sort(key=lambda case: (-case["score"] * case["severity"], case["id"]))
    else:
        eligible.sort(key=lambda case: (-case["score"], case["id"]))
    return [case["id"] for case in eligible[:capacity]]


class EnforcementLedger:
    """Only a named human reviewer can enact a queued case's bound account."""

    def __init__(self, queue_accounts: dict[str, str]):
        self.queue_accounts = queue_accounts
        self.reviewed = {}
        self.restricted_cases = set()
        self.restricted_accounts = set()
        self.events = []

    def apply_review(self, case_id: str, decision: str, reviewer: str) -> None:
        if case_id not in self.queue_accounts:
            raise ValueError("Case was not queued for review")
        if decision not in ("restrict", "clear") or not reviewer.strip():
            raise ValueError("Need explicit human decision and reviewer")
        if case_id in self.reviewed:
            if self.reviewed[case_id] != decision:
                raise ValueError("Conflicting review requires a separate appeal")
            return  # Idempotent retry of the same completed review.
        self.reviewed[case_id] = decision
        account = self.queue_accounts[case_id]
        if decision == "restrict":
            self.restricted_cases.add(case_id)
            self.restricted_accounts.add(account)
        self.events.append({"case_id": case_id, "decision": decision,
                            "account": account, "reviewer": reviewer})


def evaluate(data: dict, capacity: int = 3) -> dict:
    cases, truth = data["cases"], data["truth"]
    validate(cases, truth)
    report = {}
    for name, risk_weighted in (("score_only", False), ("severity_weighted", True)):
        queue = propose(cases, capacity, risk_weighted)
        accounts = {case["id"]: case["account"] for case in cases}
        ledger = EnforcementLedger({case_id: accounts[case_id] for case_id in queue})
        for case_id in queue:
            decision = data["human_decisions"].get(case_id)
            if decision is None:
                raise ValueError(f"Missing human review for {case_id}")
            ledger.apply_review(case_id, decision, reviewer="synthetic_reviewer")
        true_positive = sum(truth[case_id] for case_id in queue)
        report[name] = {
            "review_queue": queue,
            "queue_precision": round(true_positive / len(queue), 4) if queue else 0,
            "queue_recall": round(true_positive / sum(truth.values()), 4),
            "restricted_accounts_after_review": sorted(ledger.restricted_accounts),
            "false_restrictions": sorted(case_id for case_id in ledger.restricted_cases
                                         if not truth[case_id]),
            "missed_abuse": sorted(case_id for case_id, label in truth.items()
                                   if label and case_id not in queue),
            "audit_events": ledger.events,
        }
    return {
        "capacity": capacity,
        "policies": report,
        "candidate_release_gate": (
            not report["severity_weighted"]["false_restrictions"] and
            report["severity_weighted"]["queue_recall"] >= 0.8),
        "warning": "All cases, severities, truth, and human decisions are synthetic",
    }


if __name__ == "__main__":
    data = json.loads(Path(__file__).with_name("synthetic_cases.json").read_text())
    print(json.dumps(evaluate(data), indent=2))
