"""Temporal recommendation evaluation on a locally supplied MovieLens 100K zip."""

import json
import math
import random
import sys
from collections import defaultdict
from pathlib import Path
from zipfile import ZipFile


def load_movielens(path: Path) -> tuple[list[tuple[int, int, int, int]], dict[int, tuple[int, ...]]]:
    with ZipFile(path) as archive:
        ratings = [tuple(map(int, line.split()))
                   for line in archive.read("ml-100k/u.data").decode("ascii").splitlines()]
        genres = {}
        for line in archive.read("ml-100k/u.item").decode("latin-1").splitlines():
            fields = line.split("|")
            genres[int(fields[0])] = tuple(index for index, flag in enumerate(fields[5:24])
                                             if flag == "1")
    if not ratings or len({(u, i) for u, i, _, _ in ratings}) != len(ratings):
        raise ValueError("Expected nonempty, unique user-item ratings")
    if any(rating < 1 or rating > 5 or item not in genres
           for _, item, rating, _ in ratings):
        raise ValueError("Invalid rating or missing item metadata")
    return ratings, genres


def temporal_split(ratings: list[tuple[int, int, int, int]],
                   fraction: float = 0.8) -> tuple[list, list, int]:
    if not ratings or not 0 < fraction < 1:
        raise ValueError("Need ratings and a fraction in (0,1)")
    timestamps = sorted(row[3] for row in ratings)
    cutoff = timestamps[int(fraction * len(timestamps))]
    train = [row for row in ratings if row[3] < cutoff]
    test = [row for row in ratings if row[3] >= cutoff]
    if not train or not test:
        raise ValueError("Temporal split left an empty side")
    return train, test, cutoff


def fit(train: list[tuple[int, int, int, int]],
        genres: dict[int, tuple[int, ...]]) -> dict:
    if not train:
        raise ValueError("Empty training data")
    global_mean = sum(r for _, _, r, _ in train) / len(train)
    item_ratings = defaultdict(list)
    for _, item, rating, _ in train:
        item_ratings[item].append(rating)
    item_mean = {item: (sum(values) + 10 * global_mean) / (len(values) + 10)
                 for item, values in item_ratings.items()}
    user_residual = defaultdict(list)
    for user, item, rating, _ in train:
        user_residual[user].append(rating - item_mean[item])
    user_bias = {user: sum(values) / (len(values) + 10)
                 for user, values in user_residual.items()}
    user_genre = defaultdict(list)
    for user, item, rating, _ in train:
        residual = rating - item_mean[item] - user_bias[user]
        for genre in genres[item]:
            user_genre[(user, genre)].append(residual)
    genre_bias = {key: sum(values) / (len(values) + 15)
                  for key, values in user_genre.items()}
    return {"global_mean": global_mean, "item_mean": item_mean,
            "user_bias": user_bias, "genre_bias": genre_bias}


def predict(model: dict, user: int, item: int,
            genres: dict[int, tuple[int, ...]], personalized: bool) -> float:
    baseline = model["item_mean"].get(item, model["global_mean"])
    if not personalized:
        return baseline
    # No learned user representation means an exact item-baseline fallback.
    if user not in model["user_bias"]:
        return baseline
    genre_terms = [model["genre_bias"].get((user, genre), 0.0)
                   for genre in genres[item]]
    genre_effect = sum(genre_terms) / len(genre_terms) if genre_terms else 0.0
    return min(5.0, max(1.0, baseline + model["user_bias"][user] +
                        0.5 * genre_effect))


def ndcg_at_k(scored: list[tuple[float, int]], k: int = 10) -> float | None:
    if len(scored) < 5 or len({int(r >= 4) for _, r in scored}) < 2:
        return None
    ranked = sorted(scored, key=lambda pair: pair[0], reverse=True)[:k]
    ideal = sorted((int(r >= 4) for _, r in scored), reverse=True)[:k]
    def dcg(labels):
        return sum(label / math.log2(index + 2)
                   for index, label in enumerate(labels))
    denominator = dcg(ideal)
    return dcg(int(r >= 4) for _, r in ranked) / denominator


def user_bootstrap_interval(per_user: dict[int, dict], seed: int = 37,
                            replicates: int = 400) -> list[float]:
    """Cluster bootstrap users for candidate-minus-baseline RMSE."""
    users = sorted(per_user)
    rng = random.Random(seed)
    draws = []
    for _ in range(replicates):
        selected = [users[rng.randrange(len(users))] for _ in users]
        counts = sum(per_user[user]["count"] for user in selected)
        base = math.sqrt(sum(per_user[user]["base_sse"] for user in selected) / counts)
        candidate = math.sqrt(sum(per_user[user]["candidate_sse"]
                                  for user in selected) / counts)
        draws.append(candidate - base)
    draws.sort()
    return [round(draws[int(0.025 * replicates)], 5),
            round(draws[int(0.975 * replicates) - 1], 5)]


def evaluate(ratings: list[tuple[int, int, int, int]],
             genres: dict[int, tuple[int, ...]]) -> dict:
    train, test, cutoff = temporal_split(ratings)
    model = fit(train, genres)
    per_user = defaultdict(lambda: {"count": 0, "base_sse": 0.0,
                                    "candidate_sse": 0.0, "base_rank": [],
                                    "candidate_rank": []})
    for user, item, rating, _ in test:
        baseline = predict(model, user, item, genres, False)
        candidate = predict(model, user, item, genres, True)
        row = per_user[user]
        row["count"] += 1
        row["base_sse"] += (baseline - rating) ** 2
        row["candidate_sse"] += (candidate - rating) ** 2
        row["base_rank"].append((baseline, rating))
        row["candidate_rank"].append((candidate, rating))
    warm = {user: result for user, result in per_user.items()
            if user in model["user_bias"]}
    cold = {user: result for user, result in per_user.items()
            if user not in model["user_bias"]}
    def metrics(group):
        count = sum(r["count"] for r in group.values())
        if not count:
            return None
        base = math.sqrt(sum(r["base_sse"] for r in group.values()) / count)
        candidate = math.sqrt(sum(r["candidate_sse"] for r in group.values()) / count)
        base_ndcg, candidate_ndcg = [], []
        for row in group.values():
            b = ndcg_at_k(row["base_rank"])
            c = ndcg_at_k(row["candidate_rank"])
            if b is not None:
                base_ndcg.append(b)
                candidate_ndcg.append(c)
        return {
            "users": len(group), "ratings": count,
            "item_mean_baseline_rmse": round(base, 5),
            "personalized_rmse": round(candidate, 5),
            "candidate_minus_baseline_rmse_95pct_user_bootstrap":
                user_bootstrap_interval(group),
            "observed_item_ndcg_at_10_users": len(base_ndcg),
            "item_mean_baseline_observed_item_ndcg_at_10":
                round(sum(base_ndcg) / len(base_ndcg), 5) if base_ndcg else None,
            "personalized_observed_item_ndcg_at_10":
                round(sum(candidate_ndcg) / len(candidate_ndcg), 5)
                if candidate_ndcg else None,
        }
    return {
        "time_cutoff_unix_utc": cutoff,
        "train_ratings": len(train), "test_ratings": len(test),
        "overall": metrics(per_user), "warm_user": metrics(warm),
        "cold_user": metrics(cold),
        "warning": "Only observed rated items are evaluated; not a full-catalog or online ranking test",
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 evaluate.py /path/to/ml-100k.zip")
    data, item_genres = load_movielens(Path(sys.argv[1]))
    print(json.dumps(evaluate(data, item_genres), indent=2))
