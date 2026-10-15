# Project 15: synthetic music discovery evaluation

**Posting test:** [Suno's Content Discovery MLE role](https://jobs.ashbyhq.com/suno/e94b6a03-6315-45c2-a439-51630af15f05) asks for models of user taste, sparse feedback, ranking, relevance, diversity, and experiments. Can a simple personalized ranker beat popularity on a frozen toy holdout while exposing its tradeoffs?

Run `python3 evaluate.py` and `python3 -m unittest test_evaluate.py` from this directory. The program compares a popularity ranking with a smoothed genre-affinity ranking and a small diversity term. It reports NDCG@3, distinct-genre fraction, and catalog coverage for five invented users. The cold-start user has no interaction history, so both methods make the same ranking. Tests cover that fallback and reject train/holdout overlap.

All users, tracks, popularity values, and relevance labels were invented for this exercise. The data were shaped to demonstrate a method, so the score difference is **not** evidence of real recommender lift. There is no trained model, real user experiment, latency/load measurement, streaming preference update, long-term satisfaction measure, or production deployment. An online release would need genuine held-out interactions, uncertainty and bias analysis, guardrails, and a controlled experiment.
