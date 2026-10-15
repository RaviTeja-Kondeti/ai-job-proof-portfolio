# Project 3: incrementality holdout

**Job-post test:** Can I show whether a marketing or product change caused extra outcomes, rather than counting all conversions after exposure as impact?

`experiment.py` randomly assigns synthetic users to treatment and control, estimates the conversion-rate difference, and reports an approximate 95% confidence interval. Run `python3 experiment.py` and `python3 -m unittest test_experiment.py`.

The example demonstrates a randomized holdout. It does not solve delayed outcomes, interference between users, noncompliance, repeated testing, or heterogeneous effects. A real analysis would pre-register the success metric and guardrails, verify randomization and sample ratio, and inspect outcome latency before making a launch decision.
