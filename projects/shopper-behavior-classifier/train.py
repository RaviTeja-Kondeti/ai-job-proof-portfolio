"""Reproducible retrospective session classifier on the UCI Online Shoppers data."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import sys
import zipfile
from pathlib import Path

import numpy as np

DATA_SHA256 = "2972e6184d3ad7beaaa831d9fc2b059dc3ee29df69d1ec593c466a5cd8485d14"
CSV_NAME = "online_shoppers_intention.csv"
SPLITS = {
    "train": frozenset(("Feb", "Mar", "May", "June", "Jul", "Aug")),
    "validation": frozenset(("Sep", "Oct")),
    "test": frozenset(("Nov", "Dec")),
}
NUMERIC = (
    "Administrative", "Administrative_Duration", "Informational",
    "Informational_Duration", "ProductRelated", "ProductRelated_Duration",
    "SpecialDay",
)
CATEGORICAL = (
    "OperatingSystems", "Browser", "Region", "TrafficType",
    "VisitorType", "Weekend",
)
# PageValues directly reflects transaction-related page value. BounceRates and
# ExitRates have ambiguous availability at a pre-purchase decision point.
EXCLUDED = ("PageValues", "BounceRates", "ExitRates", "Month")


def read_rows(path: Path, verify_checksum: bool = True) -> list[dict[str, str]]:
    raw = path.read_bytes()
    if verify_checksum and hashlib.sha256(raw).hexdigest() != DATA_SHA256:
        raise ValueError("Dataset checksum differs from the frozen UCI download")
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        with archive.open(CSV_NAME) as stream:
            rows = list(csv.DictReader(io.TextIOWrapper(stream, encoding="utf-8")))
    required = set(NUMERIC + CATEGORICAL + EXCLUDED + ("Revenue",))
    if not rows or not required.issubset(rows[0]):
        raise ValueError("Missing rows or expected dataset columns")
    if any(set(row) != set(rows[0]) or any(value == "" for value in row.values()) for row in rows):
        raise ValueError("Missing values or inconsistent row schema")
    if any(row["Revenue"] not in ("TRUE", "FALSE") for row in rows):
        raise ValueError("Revenue must be TRUE or FALSE")
    if any(row["Month"] not in set().union(*SPLITS.values()) for row in rows):
        raise ValueError("Unknown month in frozen split")
    return rows


def split_rows(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    return {name: [row for row in rows if row["Month"] in months]
            for name, months in SPLITS.items()}


def labels(rows: list[dict[str, str]]) -> np.ndarray:
    return np.array([row["Revenue"] == "TRUE" for row in rows], dtype=float)


class Encoder:
    def __init__(self, train: list[dict[str, str]]):
        if not train:
            raise ValueError("Empty training set")
        raw = np.array([[math.log1p(float(row[col])) if col != "SpecialDay"
                         else float(row[col]) for col in NUMERIC] for row in train])
        if not np.isfinite(raw).all():
            raise ValueError("Nonfinite or negative numeric input")
        self.mean = raw.mean(axis=0)
        self.scale = raw.std(axis=0)
        self.scale[self.scale == 0] = 1.0
        self.categories = {col: sorted({row[col] for row in train}) for col in CATEGORICAL}
        self.names = ["intercept"] + list(NUMERIC)
        for col in CATEGORICAL:
            self.names.extend(f"{col}={v}" for v in self.categories[col])
            self.names.append(f"{col}=UNKNOWN")

    def transform(self, rows: list[dict[str, str]]) -> np.ndarray:
        output = np.zeros((len(rows), len(self.names)), dtype=float)
        output[:, 0] = 1.0
        if not rows:
            return output
        raw = np.array([[math.log1p(float(row[col])) if col != "SpecialDay"
                         else float(row[col]) for col in NUMERIC] for row in rows])
        if not np.isfinite(raw).all():
            raise ValueError("Nonfinite or negative numeric input")
        output[:, 1:1 + len(NUMERIC)] = (raw - self.mean) / self.scale
        offset = 1 + len(NUMERIC)
        for col in CATEGORICAL:
            lookup = {v: i for i, v in enumerate(self.categories[col])}
            for i, row in enumerate(rows):
                output[i, offset + lookup.get(row[col], len(lookup))] = 1.0
            offset += len(lookup) + 1
        return output


def sigmoid(z: np.ndarray) -> np.ndarray:
    z = np.clip(z, -35.0, 35.0)
    return 1.0 / (1.0 + np.exp(-z))


def fit_logistic(x: np.ndarray, y: np.ndarray, l2: float = 0.01,
                 steps: int = 900, learning_rate: float = 0.25) -> np.ndarray:
    if len(y) == 0 or len(np.unique(y)) != 2:
        raise ValueError("Training requires both classes")
    weights = np.zeros(x.shape[1], dtype=float)
    for _ in range(steps):
        error = sigmoid(x @ weights) - y
        gradient = (x.T @ error) / len(y)
        gradient[1:] += l2 * weights[1:]
        weights -= learning_rate * gradient
    return weights


def average_precision(y: np.ndarray, scores: np.ndarray) -> float:
    positives = int(y.sum())
    if positives == 0:
        return float("nan")
    order = np.argsort(-scores, kind="stable")
    sorted_y = y[order]
    sorted_scores = scores[order]
    # All identical scores form one threshold. Otherwise AP depends on the
    # arbitrary input order of tied examples (especially the constant baseline).
    ends = np.r_[np.flatnonzero(np.diff(sorted_scores)) + 1, len(y)]
    tp = np.cumsum(sorted_y)[ends - 1]
    precision = tp / ends
    recall_gain = np.diff(np.r_[0, tp]) / positives
    return float(np.sum(precision * recall_gain))


def ece(y: np.ndarray, scores: np.ndarray, bins: int = 10) -> float:
    bucket = np.minimum((scores * bins).astype(int), bins - 1)
    total = 0.0
    for b in range(bins):
        mask = bucket == b
        if mask.any():
            total += int(mask.sum()) / len(y) * abs(float(y[mask].mean() - scores[mask].mean()))
    return total


def metrics(y: np.ndarray, scores: np.ndarray, threshold: float) -> dict:
    prediction = scores >= threshold
    tp = int(np.sum(prediction & (y == 1)))
    fp = int(np.sum(prediction & (y == 0)))
    fn = int(np.sum(~prediction & (y == 1)))
    tn = len(y) - tp - fp - fn
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return {
        "n": len(y), "positives": int(y.sum()), "prevalence": float(y.mean()),
        "average_precision": average_precision(y, scores),
        "brier": float(np.mean((y - scores) ** 2)),
        "ece_10_bins": ece(y, scores),
        "threshold": threshold, "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "precision": precision, "recall": recall,
        "f1": 2 * precision * recall / (precision + recall) if precision + recall else 0.0,
    }


def select_threshold(y: np.ndarray, scores: np.ndarray) -> float:
    # Specified before examining the test set. Tie breaks toward fewer alerts.
    choices = np.arange(0.05, 0.951, 0.01)
    return float(max(choices, key=lambda t: (metrics(y, scores, float(t))["f1"], t)))


def bootstrap_ci(y: np.ndarray, scores: np.ndarray, baseline: np.ndarray,
                 seed: int = 20261014, replicates: int = 400) -> dict:
    rng = np.random.default_rng(seed)
    ap, brier_gain = [], []
    for _ in range(replicates):
        sample = rng.integers(0, len(y), len(y))
        ys, ps, bs = y[sample], scores[sample], baseline[sample]
        if ys.sum() == 0:
            continue
        ap.append(average_precision(ys, ps))
        brier_gain.append(float(np.mean((ys - bs) ** 2) - np.mean((ys - ps) ** 2)))
    return {
        "replicates": len(ap),
        "average_precision_95pct": np.quantile(ap, [0.025, 0.975]).tolist(),
        "brier_gain_vs_train_prevalence_95pct": np.quantile(brier_gain, [0.025, 0.975]).tolist(),
    }


def evaluate(rows: list[dict[str, str]]) -> dict:
    groups = split_rows(rows)
    if any(not group for group in groups.values()):
        raise ValueError("All frozen splits must contain rows")
    encoder = Encoder(groups["train"])
    x = {name: encoder.transform(group) for name, group in groups.items()}
    y = {name: labels(group) for name, group in groups.items()}
    weights = fit_logistic(x["train"], y["train"])
    scores = {name: sigmoid(matrix @ weights) for name, matrix in x.items()}
    threshold = select_threshold(y["validation"], scores["validation"])
    prevalence = float(y["train"].mean())
    test_base = np.full(len(y["test"]), prevalence)
    test = metrics(y["test"], scores["test"], threshold)
    slices = {}
    for field in ("Month", "VisitorType", "Weekend"):
        slices[field] = {}
        for value in sorted({row[field] for row in groups["test"]}):
            mask = np.array([row[field] == value for row in groups["test"]])
            slices[field][value] = metrics(y["test"][mask], scores["test"][mask], threshold)
    return {
        "protocol": {
            "dataset_sha256": DATA_SHA256,
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "target": "Revenue at completed-session level; TRUE means transaction occurred",
            "split_months": {name: sorted(months) for name, months in SPLITS.items()},
            "features": encoder.names,
            "excluded": list(EXCLUDED),
            "model": "logistic regression; L2=0.01, 900 full-batch steps, rate=0.25",
            "threshold_rule": "max validation F1 over 0.05..0.95 step 0.01; higher threshold wins ties",
            "baseline": "constant training purchase prevalence",
            "bootstrap": "400 independent session resamples, seed 20261014; percentile intervals",
        },
        "train": metrics(y["train"], scores["train"], threshold),
        "validation": metrics(y["validation"], scores["validation"], threshold),
        "test": test,
        "test_baseline": metrics(y["test"], test_base, threshold),
        "test_intervals": bootstrap_ci(y["test"], scores["test"], test_base),
        "test_slices": slices,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("zip_path", type=Path, help="original UCI dataset zip")
    parser.add_argument("--output", type=Path, help="write JSON to this path; otherwise stdout")
    args = parser.parse_args()
    report = evaluate(read_rows(args.zip_path))
    rendered = json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
