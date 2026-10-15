# Full-funnel event model

**Job-post test:** The [OpenAI Machine Learning Engineer, Growth posting](https://openai.com/careers/machine-learning-engineer-growth-san-francisco/) spans consumer and business users, markets, and acquisition through expansion. This small project tests whether those stages can be defined consistently in SQL and Python. It is a synthetic demonstration, not a claim of OpenAI user data or production growth impact.

## Run

From the repository root, with Python 3.10+:

```sh
python3 -m unittest discover -s projects/full-funnel-event-model -p 'test_*.py' -v
python3 projects/full-funnel-event-model/model.py
```

The checked-in [results.json](results.json) is the second command's output. [model.py](model.py) creates seven synthetic users and 23 event versions in memory; [funnel.sql](funnel.sql) computes the cohort table in SQLite.

## Definitions and observed result

The cohort key is signup month, user segment (`consumer` or `business`), and market (`US` or `UK`). Acquisition is the first consented signup. Activation requires a consented core action at or after signup and before day 8. Retention requires activation, at least 60 elapsed days since signup at the report cutoff, and a consented core action from day 30 up to day 60. Expansion requires activation and a later consented upgrade before day 90 after signup. Rates use acquired, retention-eligible, and activated users as denominators respectively. An immature cohort has a `null` retention rate, rather than a misleading zero.

At the April 15 cutoff, the January consumer US cohort has two acquired users but only one activated user. A later correction moves the second user's apparent early activation to day 10. The March consumer US cohort has one acquired and activated user but no user eligible for a 60-day retention observation. Results are deliberately tiny; they demonstrate definitions and edge cases, not meaningful segment comparisons.

The query includes only events whose event and receipt timestamps are at or before the cutoff, selects the newest received version of each event ID, and then excludes a version without analytics consent. Thus a later correction cannot leak backward into an earlier report, and a later consent-off version can suppress an earlier consent-on version. Timestamps are normalized to UTC before SQL ordering or cohort assignment. The input rejects orphan events, extra fields, receipt times before event times, conflicting event identities, and receipt-time ties for one event ID. The tests cover these and the cohort calculations.

## Limits

- The consent flag is scoped to an event ID. This is **not** a complete consent ledger or a global retroactive deletion mechanism. A production pipeline would need subject-level revocation, deletion propagation, and documented retention controls.
- Segment and market are static user attributes in this fixture. Real users may move markets or change account type; production cohorting needs an explicit point-in-time dimension model.
- Only two markets and seven invented users are included. There is no distributed processing, ML framework, causal experiment, online deployment, or measured business result.
- These observational rates do not estimate whether any growth action caused a change. Consent and instrumentation may select which users are visible.
