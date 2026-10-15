"""Small, synthetic offline evaluation of music discovery rankings."""

import json
import math
from pathlib import Path


def rank(user: dict, tracks: dict, personalized: bool, k: int = 3) -> list[str]:
    if k < 1 or not tracks:
        raise ValueError("Need tracks and positive k")
    heard = set(user["heard"])
    if not heard <= tracks.keys():
        raise ValueError("Unknown track in listening history")
    affinities = {}
    for track_id in heard:
        genre = tracks[track_id]["genre"]
        affinities[genre] = affinities.get(genre, 0) + 1
    candidates = [track_id for track_id in tracks if track_id not in heard]
    ranking = []
    while candidates and len(ranking) < k:
        def score(track_id):
            track = tracks[track_id]
            # Shrink sparse preference evidence toward the popularity baseline.
            affinity = affinities.get(track["genre"], 0)
            preference = 2.5 * affinity / (affinity + 2) if personalized else 0
            # Small diversification term rewards a new genre in the top-k list.
            diversity = (0.35 if personalized and affinities and
                         track["genre"] not in {tracks[x]["genre"] for x in ranking}
                         else 0)
            return (preference + math.log1p(track["popularity"]) / 5 + diversity,
                    track_id)
        best = max(candidates, key=score)
        ranking.append(best)
        candidates.remove(best)
    return ranking


def ndcg_at_k(ranking: list[str], relevance: dict, k: int) -> float:
    def dcg(gains):
        return sum((2 ** value - 1) / math.log2(position + 2)
                   for position, value in enumerate(gains))
    gains = [relevance.get(track_id, 0) for track_id in ranking[:k]]
    ideal = sorted(relevance.values(), reverse=True)[:k]
    denominator = dcg(ideal)
    return dcg(gains) / denominator if denominator else 0.0


def evaluate(data: dict, k: int = 3) -> dict:
    tracks, users = data["tracks"], data["users"]
    if k < 1 or not tracks or not users:
        raise ValueError("Need tracks, users, and positive k")
    if any(type(t["popularity"]) is not int or t["popularity"] < 0 or
           not t["genre"] for t in tracks.values()):
        raise ValueError("Invalid track metadata")
    if len({u["id"] for u in users}) != len(users):
        raise ValueError("User IDs must be unique")
    report = {}
    for name, personalized in (("popular", False), ("personalized", True)):
        rows = []
        exposed = set()
        for user in users:
            heldout = user["heldout_relevance"]
            if not set(heldout) <= tracks.keys() or any(
                    type(value) is not int or value not in (0, 1, 2, 3)
                    for value in heldout.values()):
                raise ValueError("Invalid held-out labels")
            if set(heldout) & set(user["heard"]):
                raise ValueError("Training and held-out tracks overlap")
            ranking = rank(user, tracks, personalized, k)
            exposed.update(ranking)
            genres = {tracks[t]["genre"] for t in ranking}
            rows.append({
                "user": user["id"],
                "ranking": ranking,
                "ndcg_at_k": round(ndcg_at_k(ranking, heldout, k), 4),
                "genre_diversity": round(len(genres) / len(ranking), 4) if ranking else 0,
            })
        report[name] = {
            "mean_ndcg_at_k": round(sum(r["ndcg_at_k"] for r in rows) / len(rows), 4),
            "mean_genre_diversity": round(sum(r["genre_diversity"] for r in rows) / len(rows), 4),
            "catalog_coverage": round(len(exposed) / len(tracks), 4),
            "users": rows,
        }
    return {
        "k": k,
        "variants": report,
        "offline_quality_gate": (
            report["personalized"]["mean_ndcg_at_k"] >=
            report["popular"]["mean_ndcg_at_k"] and
            report["personalized"]["mean_genre_diversity"] >= 0.5),
        "warning": "Synthetic users, tracks, and held-out labels; no online or causal evidence",
    }


if __name__ == "__main__":
    data = json.loads(Path(__file__).with_name("synthetic_music.json").read_text())
    print(json.dumps(evaluate(data), indent=2))
