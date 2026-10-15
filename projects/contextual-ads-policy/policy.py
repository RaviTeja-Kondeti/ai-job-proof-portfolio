"""A local, synthetic contextual ads policy with no user-level features."""

from __future__ import annotations

import json
from dataclasses import dataclass

ALLOWED_TOPICS = frozenset({"coding", "education", "music", "travel", "general"})
REQUEST_FIELDS = frozenset({"topic", "measurement_consent", "max_ads"})
MIN_RELEVANCE = 0.60


@dataclass(frozen=True)
class Ad:
    ad_id: str
    advertiser: str
    topic: str
    bid: float
    quality: float
    remaining_budget: float
    approved: bool

    def __post_init__(self) -> None:
        if not self.ad_id or not self.advertiser or self.topic not in ALLOWED_TOPICS:
            raise ValueError("Invalid ad identity or topic")
        if not all(isinstance(x, (float, int)) and not isinstance(x, bool)
                   for x in (self.bid, self.quality, self.remaining_budget)):
            raise ValueError("Numeric ad fields required")
        if not (0 <= self.bid <= 100 and 0 <= self.quality <= 1
                and 0 <= self.remaining_budget <= 1_000_000):
            raise ValueError("Ad fields outside allowed ranges")
        if not isinstance(self.approved, bool):
            raise ValueError("Approval must be Boolean")


def validate_request(request: dict) -> None:
    if set(request) != REQUEST_FIELDS:
        raise ValueError("Only topic, measurement_consent, and max_ads are accepted")
    if not isinstance(request["topic"], str):
        raise ValueError("Topic must be a string")
    if not isinstance(request["measurement_consent"], bool):
        raise ValueError("Measurement consent must be Boolean")
    if (not isinstance(request["max_ads"], int)
            or isinstance(request["max_ads"], bool)
            or not 1 <= request["max_ads"] <= 3):
        raise ValueError("max_ads must be an integer from 1 to 3")


def relevance(topic: str, ad: Ad) -> float:
    if ad.topic == topic:
        return ad.quality
    if ad.topic == "general":
        return 0.65 * ad.quality
    return 0.0


def eligible(topic: str, ad: Ad) -> bool:
    return ad.approved and ad.remaining_budget >= ad.bid and ad.bid > 0


class AggregateCounters:
    """Counters have no request IDs, timestamps, profiles, or per-user rows."""

    def __init__(self) -> None:
        self.consenting_requests = 0
        self.served_ads = 0

    def record(self, count: int) -> None:
        self.consenting_requests += 1
        self.served_ads += count

    def snapshot(self) -> dict[str, int]:
        return {"consenting_requests": self.consenting_requests,
                "served_ads": self.served_ads}


def choose(request: dict, ads: list[Ad], counters: AggregateCounters,
           policy: str = "contextual") -> list[Ad]:
    validate_request(request)
    if policy not in {"contextual", "bid_only"}:
        raise ValueError("Unknown policy")
    topic = request["topic"]
    # A contextual target outside the approved taxonomy includes sensitive
    # categories. We do not infer or store why it was suppressed.
    if topic not in ALLOWED_TOPICS or topic == "general":
        chosen: list[Ad] = []
    else:
        candidates = [ad for ad in ads if eligible(topic, ad)]
        if policy == "contextual":
            candidates = [ad for ad in candidates if relevance(topic, ad) >= MIN_RELEVANCE]
            candidates.sort(key=lambda ad: (-relevance(topic, ad), -ad.bid, ad.ad_id))
        else:
            candidates.sort(key=lambda ad: (-ad.bid, ad.ad_id))
        chosen = candidates[:request["max_ads"]]
    if request["measurement_consent"]:
        counters.record(len(chosen))
    return chosen


def synthetic_catalog() -> list[Ad]:
    return [
        Ad("a-coding", "small-dev", "coding", 1.1, 0.90, 100, True),
        Ad("b-coding", "dev-tools", "coding", 1.8, 0.70, 100, True),
        Ad("a-education", "small-edu", "education", 1.2, 0.86, 100, True),
        Ad("a-music", "small-music", "music", 1.3, 0.88, 100, True),
        Ad("a-travel", "small-travel", "travel", 1.4, 0.84, 100, True),
        Ad("high-bid-generic", "large-brand", "general", 5.0, 0.90, 100, True),
        Ad("unsafe-coding", "unsafe", "coding", 90.0, 0.99, 100, False),
        Ad("no-budget-music", "exhausted", "music", 9.0, 0.99, 0, True),
    ]


def evaluate() -> dict:
    catalog = synthetic_catalog()
    cases = ["coding", "education", "music", "travel"]
    report = {"data": "fixed synthetic catalog and four synthetic topics",
              "privacy_contract": "context-only request; no user ID, history, demographic, or denied-consent measurement",
              "policies": {}}
    for name in ("bid_only", "contextual"):
        counters = AggregateCounters()
        output = []
        for topic in cases:
            request = {"topic": topic, "measurement_consent": True, "max_ads": 1}
            selected = choose(request, catalog, counters, policy=name)
            if selected:
                ad = selected[0]
                output.append({"topic": topic, "ad_id": ad.ad_id,
                               "relevance": relevance(topic, ad), "bid": ad.bid})
        report["policies"][name] = {
            "cases": output,
            "mean_relevance": sum(x["relevance"] for x in output) / len(cases),
            "mean_bid": sum(x["bid"] for x in output) / len(cases),
            "aggregate_counters": counters.snapshot(),
        }
    return report


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
