# Frozen MovieLens 100K run

Run date: October 14, 2026 US Eastern. Input: official [MovieLens 100K archive](https://grouplens.org/datasets/movielens/100k/), SHA-256 `50d2a982c66986937beb9ffb3aa76efe955bf3d5c6b761f4e3a7cd717c6a3229`. Command: `python3 evaluate.py /absolute/path/to/ml-100k.zip` using Python 3.12. No dataset rows are redistributed here. See [methods and license](README.md).

The global 80th-percentile time cutoff was Unix UTC `889237269`. There were 79,999 earlier training ratings and 20,001 later test ratings.

| Test group | Users | Ratings | Item-mean baseline RMSE | Personalized RMSE | Candidate minus baseline 95% user-bootstrap interval | Observed-item NDCG@10: baseline → candidate |
|---|---:|---:|---:|---:|---:|---:|
| Overall | 301 | 20,001 | 1.02926 | 1.02424 | −0.01227 to +0.00200 | 0.79177 → 0.79341 (265 users) |
| Warm user | 109 | 2,953 | 1.03106 | 0.99660 | −0.08449 to +0.00765 | 0.80845 → 0.81439 (73 users) |
| Cold user | 192 | 17,048 | 1.02895 | 1.02895 | 0 to 0 | 0.78544 → 0.78544 (192 users) |

The candidate's point estimate is better overall and for warm users, but both bootstrap intervals include zero. This run does **not** establish a reliable quality improvement. Cold users account for 85.2% of the test ratings; no personalization is available for them under this temporal split. A production design would require a stronger cold-start strategy and a genuinely prospective, exposure-aware evaluation.

The NDCG calculation ranks only items that each test user chose to rate. It cannot measure full-catalog recommendation quality, novelty, exposure bias, long-term satisfaction, or online lift. It should not be interpreted as evidence that the method would improve Suno's product.
