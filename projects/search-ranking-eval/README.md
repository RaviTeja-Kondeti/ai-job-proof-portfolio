# Project 14: enterprise search ranking evaluation

**Job-post test:** Can a new ranker improve relevance while protecting document permissions and exposing performance by user slice?

`python3 evaluate.py` reports NDCG@3, MRR@3, permission violations, and slice scores for two invented rankers. The candidate deliberately has better average ranking quality but puts a restricted document in one top result, so its release gate fails. `python3 -m unittest test_evaluate.py` verifies this failure, a perfect ranking case, and malformed inputs.

This is an evaluation method, not a trained personalization model or a real enterprise-search deployment. It does not measure query understanding, corpus adaptation, latency, online lift, access-control enforcement before ranking, or customer outcomes. Labels and rankings are synthetic.
