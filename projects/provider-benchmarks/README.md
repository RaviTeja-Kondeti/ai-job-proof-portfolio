# Project 6: public provider benchmark harness

**Job-post test:** Can I define a defensible method for comparing data providers and choose different providers for different tasks?

`synthetic_tasks.json` is a fully inspectable set of invented company, person, and job lookups. `benchmark.py` scores exact-match accuracy, coverage, p95 latency, and cost by domain, then applies a fixed provider-selection rule. `python3 benchmark.py` prints every score and decision; `python3 -m unittest test_benchmark.py` checks selection, task coverage, missing data, and percentile calculation.

This is a methodological prototype, **not a ranking of real vendors**. Nine invented tasks cannot establish external validity, freshness, entity matching quality, or performance under adversarial challenge. A credible public benchmark would need independently sourced ground truth, versioned sampling, confidence intervals, documented dispute handling, weekly reproducible releases, and separate evaluation tasks from provider-routing development.
