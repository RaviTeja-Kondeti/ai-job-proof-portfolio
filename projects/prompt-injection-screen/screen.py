"""Small, inspectable prompt-injection screening baseline for untrusted text."""

from collections import Counter
import json
import math
from pathlib import Path
import re


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z]+", text.lower())


class WordNaiveBayes:
    def fit(self, rows: list[dict]) -> "WordNaiveBayes":
        if not rows or {row["label"] for row in rows} != {"benign", "injection"}:
            raise ValueError("Training data needs benign and injection labels")
        self.counts = {label: Counter() for label in ("benign", "injection")}
        self.docs = Counter()
        for row in rows:
            self.counts[row["label"]].update(tokens(row["text"]))
            self.docs[row["label"]] += 1
        self.vocabulary = set().union(*(set(counts) for counts in self.counts.values()))
        self.totals = {label: sum(counts.values()) for label, counts in self.counts.items()}
        return self

    def probability(self, text: str) -> float:
        scores = {}
        for label in ("benign", "injection"):
            score = math.log(self.docs[label] / sum(self.docs.values()))
            for token in tokens(text):
                if token in self.vocabulary:
                    score += math.log((self.counts[label][token] + 1)
                                      / (self.totals[label] + len(self.vocabulary)))
            scores[label] = score
        difference = scores["benign"] - scores["injection"]
        return 1 / (1 + math.exp(min(700, max(-700, difference))))


def evaluate(train: list[dict], holdout: list[dict], threshold: float = 0.5) -> dict:
    if not 0 < threshold < 1:
        raise ValueError("Threshold must be between zero and one")
    train_ids = {row["id"] for row in train}
    holdout_ids = {row["id"] for row in holdout}
    if train_ids & holdout_ids or len(holdout_ids) != len(holdout):
        raise ValueError("Train and holdout IDs must be disjoint and unique")
    model = WordNaiveBayes().fit(train)
    confusion = {"true_positive": 0, "false_positive": 0,
                 "true_negative": 0, "false_negative": 0}
    failures = []
    for row in holdout:
        probability = model.probability(row["text"])
        predicted = "injection" if probability >= threshold else "benign"
        actual = row["label"]
        key = ("true_" if predicted == actual else "false_")
        key += ("positive" if predicted == "injection" else "negative")
        confusion[key] += 1
        if predicted != actual:
            failures.append({"id": row["id"], "actual": actual,
                             "predicted": predicted, "injection_probability": round(probability, 3)})
    return {"holdout_size": len(holdout), "confusion": confusion,
            "failures": failures,
            "warning": "Toy data and a word model; never use as a sole production safeguard"}


if __name__ == "__main__":
    dataset = json.loads(Path(__file__).with_name("synthetic_dataset.json").read_text())
    print(json.dumps(evaluate(dataset["train"], dataset["holdout"]), indent=2))
