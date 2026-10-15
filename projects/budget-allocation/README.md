# Project 1: constrained budget allocation

**Job-post test:** Can I distribute a paid marketing budget across channels and markets while accounting for diminishing returns, uncertainty, and hard business limits?

`allocate.py` implements a discrete greedy allocator for separable concave response curves. Each campaign has a minimum, maximum, market, channel, estimated response curve, and uncertainty. A conservative response estimate changes the decision without relaxing the budget or spend caps. `round_robin` is an uninformed baseline.

Run `python3 allocate.py` and `python3 -m unittest test_allocate.py` in this folder. The output reports assumed value under the synthetic curves; it is **not a measured causal lift**. A real deployment would estimate response from consented historical data, backtest across time and markets, validate incrementality with randomized experiments, and add data quality and operational monitoring.

The tests cover the binding constraints, baseline comparison, uncertainty response, infeasible input, and reproducibility.
