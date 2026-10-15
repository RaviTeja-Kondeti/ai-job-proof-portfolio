"""Constrained, uncertainty-aware allocation of a synthetic marketing budget."""

from dataclasses import dataclass
import json
import math


@dataclass(frozen=True)
class Campaign:
    name: str
    market: str
    channel: str
    response_scale: float
    response_rate: float
    scale_uncertainty: float
    minimum: int
    maximum: int

    def value(self, spend: int, uncertainty_weight: float = 0.0) -> float:
        conservative_scale = max(0.0, self.response_scale - uncertainty_weight * self.scale_uncertainty)
        return conservative_scale * math.log1p(self.response_rate * spend)


def _validate(campaigns: list[Campaign], budget: int, step: int) -> None:
    if not campaigns or step <= 0 or budget < 0 or budget % step:
        raise ValueError("Campaigns, budget, and step must define a nonempty discrete allocation")
    if len({c.name for c in campaigns}) != len(campaigns):
        raise ValueError("Campaign names must be unique")
    for campaign in campaigns:
        if (campaign.minimum < 0 or campaign.maximum < campaign.minimum
                or campaign.minimum % step or campaign.maximum % step
                or campaign.response_scale < 0 or campaign.response_rate < 0
                or campaign.scale_uncertainty < 0):
            raise ValueError(f"Invalid parameters for {campaign.name}")
    if sum(c.minimum for c in campaigns) > budget or sum(c.maximum for c in campaigns) < budget:
        raise ValueError("Budget cannot be allocated within campaign bounds")


def allocate(campaigns: list[Campaign], budget: int, step: int = 100,
             uncertainty_weight: float = 0.0) -> dict[str, int]:
    """Maximize separable concave value on a spend grid, respecting hard bounds."""
    _validate(campaigns, budget, step)
    if uncertainty_weight < 0:
        raise ValueError("uncertainty_weight cannot be negative")
    spend = {c.name: c.minimum for c in campaigns}
    remaining = budget - sum(spend.values())
    while remaining:
        eligible = [c for c in campaigns if spend[c.name] + step <= c.maximum]
        if not eligible:
            raise RuntimeError("No eligible campaign despite a feasible budget")
        chosen = max(
            eligible,
            key=lambda c: (
                c.value(spend[c.name] + step, uncertainty_weight)
                - c.value(spend[c.name], uncertainty_weight),
                c.name,
            ),
        )
        spend[chosen.name] += step
        remaining -= step
    return spend


def round_robin(campaigns: list[Campaign], budget: int, step: int = 100) -> dict[str, int]:
    """Feasible allocation baseline that ignores response curves."""
    _validate(campaigns, budget, step)
    spend = {c.name: c.minimum for c in campaigns}
    remaining = budget - sum(spend.values())
    while remaining:
        for campaign in campaigns:
            if remaining and spend[campaign.name] + step <= campaign.maximum:
                spend[campaign.name] += step
                remaining -= step
    return spend


def portfolio_value(campaigns: list[Campaign], spend: dict[str, int]) -> float:
    return sum(c.value(spend[c.name]) for c in campaigns)


def demo() -> dict:
    campaigns = [
        Campaign("search_us", "US", "search", 180, 0.003, 12, 1000, 7000),
        Campaign("social_us", "US", "social", 145, 0.002, 18, 500, 6000),
        Campaign("search_eu", "EU", "search", 130, 0.004, 8, 500, 5500),
        Campaign("video_eu", "EU", "video", 105, 0.001, 20, 0, 5000),
    ]
    budget = 12000
    baseline = round_robin(campaigns, budget)
    selected = allocate(campaigns, budget, uncertainty_weight=1.0)
    return {
        "assumption": "Synthetic response curves; value is an arbitrary unit, not real conversions or dollars",
        "budget": budget,
        "baseline_spend": baseline,
        "risk_adjusted_spend": selected,
        "baseline_value_under_assumed_curves": round(portfolio_value(campaigns, baseline), 2),
        "selected_value_under_assumed_curves": round(portfolio_value(campaigns, selected), 2),
    }


if __name__ == "__main__":
    print(json.dumps(demo(), indent=2))
