# Project 7: classifier evaluation and release gate

**Job-post test:** Can a candidate evaluate a classifier beyond headline accuracy and block a risky release?

Run `python3 evaluate.py` and `python3 -m unittest test_evaluate.py`. The synthetic predictions deliberately have a weak rare-case slice, so the gate should fail even when overall accuracy appears good. The report includes confusion counts, Brier score, expected calibration error, per-slice accuracy, and explicit release criteria.

These are invented scores for 24 cases, not a trained model, real user data, or production release. A credible deployment decision would require a larger representative held-out set, confidence intervals, drift monitoring, labeling audits, latency/cost measurement, and review of the errors that matter to users.
