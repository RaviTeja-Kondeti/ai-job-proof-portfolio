"""Evaluate a synthetic binary classifier with explicit deployment gates."""

from collections import defaultdict
import json
from pathlib import Path


def evaluate(rows: list[dict], threshold: float = 0.5, bins: int = 5) -> dict:
    if not rows or len({row["id"] for row in rows}) != len(rows):
        raise ValueError("Rows need unique IDs")
    if not 0 < threshold < 1 or bins < 2:
        raise ValueError("Invalid evaluation settings")
    for row in rows:
        if row["label"] not in (0, 1) or not 0 <= row["score"] <= 1:
            raise ValueError("Labels must be binary and scores must be probabilities")
        if not row.get("slice"):
            raise ValueError("Every row needs an evaluation slice")

    predictions = [int(row["score"] >= threshold) for row in rows]
    labels = [row["label"] for row in rows]
    tp = sum(p == y == 1 for p, y in zip(predictions, labels))
    fp = sum(p == 1 and y == 0 for p, y in zip(predictions, labels))
    fn = sum(p == 0 and y == 1 for p, y in zip(predictions, labels))
    tn = len(rows) - tp - fp - fn
    accuracy = (tp + tn) / len(rows)
    brier = sum((row["score"] - row["label"]) ** 2 for row in rows) / len(rows)

    bucketed = defaultdict(list)
    for row in rows:
        index = min(int(row["score"] * bins), bins - 1)
        bucketed[index].append(row)
    calibration = []
    ece = 0
    for index, group in sorted(bucketed.items()):
        mean_score = sum(row["score"] for row in group) / len(group)
        positive_rate = sum(row["label"] for row in group) / len(group)
        ece += len(group) / len(rows) * abs(mean_score - positive_rate)
        calibration.append({"bin": index, "n": len(group),
                            "mean_score": round(mean_score, 4),
                            "positive_rate": round(positive_rate, 4)})

    slices = {}
    for name in sorted({row["slice"] for row in rows}):
        subset = [row for row in rows if row["slice"] == name]
        slices[name] = {
            "n": len(subset),
            "accuracy": round(sum(int((row["score"] >= threshold) == row["label"])
                                  for row in subset) / len(subset), 4),
            "brier": round(sum((row["score"] - row["label"]) ** 2 for row in subset)
                           / len(subset), 4),
        }
    # These thresholds are illustrative release criteria, not production policy.
    gates = {
        "minimum_sample_size": len(rows) >= 20,
        "overall_accuracy": accuracy >= 0.8,
        "maximum_ece": ece <= 0.15,
        "each_slice_sample_size": all(result["n"] >= 5 for result in slices.values()),
        "worst_slice_accuracy": min(result["accuracy"] for result in slices.values()) >= 0.7,
    }
    return {
        "n": len(rows), "threshold": threshold,
        "confusion": {"tp": tp, "fp": fp, "fn": fn, "tn": tn},
        "accuracy": round(accuracy, 4), "brier": round(brier, 4),
        "ece": round(ece, 4), "calibration": calibration,
        "slices": slices, "gates": gates, "release_ready": all(gates.values()),
        "warning": "Tiny synthetic set: gate results cannot establish production fitness",
    }


if __name__ == "__main__":
    rows = json.loads(Path(__file__).with_name("synthetic_predictions.json").read_text())
    print(json.dumps(evaluate(rows), indent=2))
