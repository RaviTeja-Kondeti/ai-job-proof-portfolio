# Project 11: account-grain B2B metrics

**Job-post test:** Can product usage, sales pipeline, and paid revenue be joined into a coherent account view without multiplying amounts through one-to-many joins?

`python3 metrics.py` runs a SQLite account-level model on invented data. `python3 -m unittest test_metrics.py` verifies that multiple events, opportunities, and invoices do not inflate each other; zero-activity accounts remain visible; and duplicate/orphan events are rejected. The SQL files are readable and reusable.

This is a data-modeling proof, not a commercial recommendation or employer experience. A production metrics layer would need source freshness, late-arrival handling, identity resolution, time zones, currency conversion, event instrumentation QA, access controls, dbt/warehouse deployment, and reconciliation to finance.
