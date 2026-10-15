"""Controlled training-label swaps on the public UCI shopper dataset."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

import numpy as np

CLASSIFIER_PATH = Path(__file__).resolve().parents[1] / "shopper-behavior-classifier" / "train.py"
SPEC = importlib.util.spec_from_file_location("shopper_classifier_for_ablation", CLASSIFIER_PATH)
classifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(classifier)

CORRUPTION_LEVELS = (0.20, 0.50)
SEEDS = tuple(range(20))


def swap_labels(labels: np.ndarray, fraction_of_positives: float,
                seed: int) -> tuple[np.ndarray, dict]:
    if not 0 <= fraction_of_positives <= 1:
        raise ValueError("Fraction must be between zero and one")
    positives = np.flatnonzero(labels == 1)
    negatives = np.flatnonzero(labels == 0)
    if not len(positives) or not len(negatives):
        raise ValueError("Both classes required")
    count = round(fraction_of_positives * len(positives))
    if count > len(negatives):
        raise ValueError("Not enough negative labels to swap")
    rng = np.random.default_rng(seed)
    changed = labels.copy()
    changed[rng.choice(positives, count, replace=False)] = 0
    changed[rng.choice(negatives, count, replace=False)] = 1
    assert changed.sum() == labels.sum()
    return changed, {"positive_to_negative": count,
                     "negative_to_positive": count,
                     "total_changed": 2 * count}


def score(x_train: np.ndarray, y_train: np.ndarray,
          x_test: np.ndarray, y_test: np.ndarray) -> dict[str, float]:
    weights = classifier.fit_logistic(x_train, y_train)
    predicted = classifier.sigmoid(x_test @ weights)
    return {
        "average_precision": classifier.average_precision(y_test, predicted),
        "brier": float(np.mean((y_test - predicted) ** 2)),
        "ece_10_bins": classifier.ece(y_test, predicted),
    }


def summarize(records: list[dict], clean: dict) -> dict:
    return {
        "runs": len(records),
        "mean_average_precision": float(np.mean([r["average_precision"] for r in records])),
        "range_average_precision": [float(min(r["average_precision"] for r in records)),
                                    float(max(r["average_precision"] for r in records))],
        "mean_ap_change_vs_clean": float(np.mean([r["average_precision"] - clean["average_precision"]
                                                   for r in records])),
        "mean_brier": float(np.mean([r["brier"] for r in records])),
        "mean_brier_change_vs_clean": float(np.mean([r["brier"] - clean["brier"]
                                                      for r in records])),
        "seed_results": records,
    }


def run(path: Path) -> dict:
    groups = classifier.split_rows(classifier.read_rows(path))
    encoder = classifier.Encoder(groups["train"])
    x_train = encoder.transform(groups["train"])
    y_train = classifier.labels(groups["train"])
    x_test = encoder.transform(groups["test"])
    y_test = classifier.labels(groups["test"])
    clean = score(x_train, y_train, x_test, y_test)
    treatments = {}
    for level in CORRUPTION_LEVELS:
        results = []
        for seed in SEEDS:
            corrupted, counts = swap_labels(y_train, level, seed)
            result = {"seed": seed, **counts,
                      **score(x_train, corrupted, x_test, y_test)}
            results.append(result)
        treatments[str(level)] = summarize(results, clean)
    return {
        "protocol": {
            "source": "UCI Online Shoppers Purchasing Intention Dataset",
            "dataset_sha256": classifier.DATA_SHA256,
            "numpy": np.__version__,
            "train_months": sorted(classifier.SPLITS["train"]),
            "test_months": sorted(classifier.SPLITS["test"]),
            "train_n": len(y_train), "train_positives": int(y_train.sum()),
            "test_n": len(y_test), "test_positives": int(y_test.sum()),
            "intervention": "swap a fixed fraction of positive training labels with an equal number of negative labels",
            "levels_fraction_of_positives": list(CORRUPTION_LEVELS),
            "seeds": list(SEEDS),
            "model": "same train-only preprocessing and fixed logistic recipe as shopper-behavior-classifier",
            "outcome": "same unmodified November-December labels for every arm",
        },
        "clean": clean,
        "treatments": treatments,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("zip_path", type=Path, help="original UCI dataset zip")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(run(args.zip_path), indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
