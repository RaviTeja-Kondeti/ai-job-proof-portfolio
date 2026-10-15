# Project 17: temporal recommendation evaluation on public ratings

**Suno posting test:** [Content Discovery MLE](https://jobs.ashbyhq.com/suno/e94b6a03-6315-45c2-a439-51630af15f05) calls for preference learning, ranking evaluation, sparse-user behavior, and deployed recommendation judgment. This project tests a narrow **offline** piece on real historical interactions from a different domain.

Data: [GroupLens MovieLens 100K](https://grouplens.org/datasets/movielens/100k/), 100,000 historical movie ratings. Follow [GroupLens's usage license](https://files.grouplens.org/datasets/movielens/ml-100k/README): research use, attribution, and **no dataset redistribution without permission**. The dataset is not in this repository. It is movies from 1997–98, not Suno users, generated music, or a current product dataset. Dataset citation: F. Maxwell Harper and Joseph A. Konstan, “The MovieLens Datasets: History and Context,” *ACM TiiS* 5(4), 2015, [DOI 10.1145/2827872](https://doi.org/10.1145/2827872).

Download `ml-100k.zip` from the [official GroupLens page](https://grouplens.org/datasets/movielens/100k/) into a local scratch directory. The evaluated archive's SHA-256 is `50d2a982c66986937beb9ffb3aa76efe955bf3d5c6b761f4e3a7cd717c6a3229`. Then run:

```sh
python3 evaluate.py /absolute/path/to/ml-100k.zip
python3 -m unittest test_evaluate.py
```

The split uses a **global timestamp cutoff** at the 80th percentile. Training uses only earlier ratings; evaluation uses later ratings. The baseline shrinks each item's average rating toward the global mean. The candidate adds a shrunk user bias and a user-genre residual; unseen users fall back exactly to the baseline. The report gives RMSE for all, warm, and cold users; an observed-item NDCG@10; and a paired bootstrap interval that samples users rather than treating each rating as independent.

**Critical limit:** Test candidates are only items that users chose to rate. Unrated items are neither assumed negative nor evaluated. Thus NDCG here is **not** full-catalog recommendation quality, a counterfactual estimate, or causal product lift. The data lack exposure and listen logs, so this cannot test the Suno posting's real-time serving, novelty, long-term satisfaction, or large-scale experiments. See [frozen run results](RESULTS.md).
