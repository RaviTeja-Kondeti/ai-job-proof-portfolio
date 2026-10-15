# Project 9: delayed-signal growth policy backtest

**Job-post test:** Can a spending policy be compared with a fixed baseline without using future information, while respecting budget and weekly change limits?

`python3 backtest.py` reports six invented weeks of choices and incremental value. In this scenario the adaptive policy **loses 16.21 value units** to the fixed split as the best channel changes before delayed feedback arrives. `python3 -m unittest test_backtest.py` checks the budget, change bound, no future-truth leakage, delayed-signal response, and malformed inputs.

The environment uses invented response curves and exposes counterfactual results for both policies. Real historical spend logs do **not** reveal what would have happened under an unchosen policy. This simulation therefore demonstrates decision logic, not a causal estimate or a production-ready policy. The next release needs randomized exploration or a defensible off-policy evaluation design.
