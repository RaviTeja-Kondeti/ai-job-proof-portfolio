"""Synthetic, time-split conversion and 30-day value forecasting."""

import json
import math
import random
from collections import defaultdict


LABEL_MATURITY_DAYS = 30


def make_synthetic_cohorts(seed: int = 27, days: int = 140,
                           signups_per_day: int = 20) -> list[dict]:
    """Invent cohorts with known, deliberately simple segment effects."""
    rng = random.Random(seed)
    rows = []
    for day in range(days):
        for number in range(signups_per_day):
            segment = rng.choice(("consumer", "business"))
            channel = rng.choice(("search", "social"))
            probability = (0.08 if segment == "consumer" else 0.29)
            probability += 0.09 if channel == "search" else -0.02
            converted = int(rng.random() < probability)
            value = (round((55 if segment == "consumer" else 260)
                           * rng.uniform(0.6, 1.4), 2) if converted else 0.0)
            rows.append({"id": f"{day:03d}-{number:02d}", "signup_day": day,
                         "segment": segment, "channel": channel,
                         "converted_7d": converted, "value_30d": value})
    return rows


def validate_rows(rows: list[dict]) -> None:
    if not rows or len({r["id"] for r in rows}) != len(rows):
        raise ValueError("Need nonempty, unique cohort rows")
    for row in rows:
        if (type(row["signup_day"]) is not int or row["signup_day"] < 0 or
                row["segment"] not in ("consumer", "business") or
                row["channel"] not in ("search", "social") or
                type(row["converted_7d"]) is not int or
                row["converted_7d"] not in (0, 1) or
                type(row["value_30d"]) not in (int, float) or
                not math.isfinite(row["value_30d"]) or row["value_30d"] < 0 or
                (row["converted_7d"] == 0 and row["value_30d"] != 0)):
            raise ValueError(f"Invalid cohort row: {row['id']}")


def split_as_of(rows: list[dict], decision_day: int = 100,
                evaluation_day: int = 150) -> tuple[list[dict], list[dict], int]:
    """Train on fully matured rows available at the decision; score future cohorts."""
    validate_rows(rows)
    if decision_day < LABEL_MATURITY_DAYS or evaluation_day <= decision_day:
        raise ValueError("Invalid as-of dates")
    train = [r for r in rows if r["signup_day"] + LABEL_MATURITY_DAYS <= decision_day]
    test = [r for r in rows if (decision_day <= r["signup_day"] and
                              r["signup_day"] + LABEL_MATURITY_DAYS <= evaluation_day)]
    immature = sum(decision_day - LABEL_MATURITY_DAYS < r["signup_day"] < decision_day
                   for r in rows)
    if not train or not test:
        raise ValueError("Need mature training and held-out evaluation cohorts")
    return train, test, immature


def fit(train: list[dict]) -> dict:
    """Fit global and shrinkage-smoothed segment/channel two-part forecasts."""
    if not train:
        raise ValueError("Empty training data")
    n = len(train)
    conversions = sum(r["converted_7d"] for r in train)
    global_probability = conversions / n
    global_positive_value = (sum(r["value_30d"] for r in train) / conversions
                             if conversions else 0.0)
    cells = defaultdict(list)
    for row in train:
        cells[(row["segment"], row["channel"])].append(row)
    estimates = {}
    for key, group in cells.items():
        count = len(group)
        successes = sum(r["converted_7d"] for r in group)
        probability = (successes + 20 * global_probability) / (count + 20)
        positive_value = ((sum(r["value_30d"] for r in group)
                           + 5 * global_positive_value) / (successes + 5))
        estimates[key] = (probability, positive_value)
    return {"global": (global_probability, global_positive_value), "cells": estimates}


def predict(model: dict, row: dict, personalized: bool) -> tuple[float, float]:
    probability, positive_value = (model["cells"].get((row["segment"], row["channel"]),
                                model["global"]) if personalized else model["global"])
    return probability, probability * positive_value


def interval(differences: list[float], seed: int = 17,
             replicates: int = 400) -> list[float]:
    """Paired percentile bootstrap; descriptive, not a guarantee under drift."""
    rng = random.Random(seed)
    n = len(differences)
    draws = sorted(sum(differences[rng.randrange(n)] for _ in range(n)) / n
                   for _ in range(replicates))
    return [round(draws[int(0.025 * replicates)], 6),
            round(draws[int(0.975 * replicates) - 1], 6)]


def evaluate(rows: list[dict], decision_day: int = 100,
             evaluation_day: int = 150) -> dict:
    train, test, immature = split_as_of(rows, decision_day, evaluation_day)
    model = fit(train)
    by_variant = {}
    losses = {}
    for name, personalized in (("global", False), ("segment_channel", True)):
        scored = []
        for row in test:
            probability, expected_value = predict(model, row, personalized)
            scored.append({"segment": row["segment"],
                           "brier": (probability - row["converted_7d"]) ** 2,
                           "value_abs_error": abs(expected_value - row["value_30d"]),
                           "prediction": probability})
        losses[name] = scored
        by_variant[name] = {
            "brier": round(sum(r["brier"] for r in scored) / len(scored), 6),
            "value_mae_usd": round(sum(r["value_abs_error"] for r in scored)
                                   / len(scored), 2),
            "by_segment": {
                segment: {
                    "n": sum(r["segment"] == segment for r in scored),
                    "brier": round(sum(r["brier"] for r in scored
                                       if r["segment"] == segment)
                                   / sum(r["segment"] == segment for r in scored), 6),
                }
                for segment in ("consumer", "business")
            },
        }
    brier_difference = [candidate["brier"] - baseline["brier"]
                        for baseline, candidate in zip(losses["global"],
                                                       losses["segment_channel"])]
    value_difference = [candidate["value_abs_error"] - baseline["value_abs_error"]
                        for baseline, candidate in zip(losses["global"],
                                                       losses["segment_channel"])]
    brier_interval = interval(brier_difference)
    return {
        "decision_day": decision_day, "evaluation_day": evaluation_day,
        "train_n": len(train), "test_n": len(test),
        "excluded_immature_training_rows": immature,
        "variants": by_variant,
        "candidate_minus_baseline_95pct_paired_bootstrap": {
            "brier": brier_interval,
            "value_mae_usd": interval(value_difference),
        },
        "conversion_quality_decision": ("candidate_supported" if brier_interval[1] < 0
                                        else "inconclusive_or_worse"),
        "warning": "Invented data and outcomes; 30-day value is not lifetime value",
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(make_synthetic_cohorts()), indent=2))
