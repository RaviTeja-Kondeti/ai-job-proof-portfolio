# Retrospective behavior classifier: train, shift test, and hold decision

**Job-post test:** [OpenAI Machine Learning Engineer, Implicit Signals](https://jobs.ashbyhq.com/openai/a01fc9ed-de08-4326-9206-4ee3f08000dc) asks for classification, rigorous evaluation, calibration, generalization, and production judgment. This project proves a narrow part of that test: a reproducible classifier trained on **real public data**, with a separate month-shift test and an explicit decision. It does not model LLM behavior or establish production ownership.

## Source and label guide

[UCI Online Shoppers Purchasing Intention Dataset](https://archive.ics.uci.edu/dataset/468/online%2Bshoppers%2Bpurchasing%2Bintention%2Bdataset), Sakar and Kastro (2018), [DOI 10.24432/C5F88Q](https://doi.org/10.24432/C5F88Q), CC BY 4.0. The archive has 12,330 sessions; 1,908 ended with shopping. UCI says each session belongs to a different user in the sampled year. The raw data are downloaded by the reviewer and are not copied into this repository.

- **Unit:** one website session, with no claim that records are independent across calendar periods.
- **Positive label:** `Revenue=TRUE`, meaning a session ended in a purchase. It is **not** a direct measurement of purchase intent or model quality.
- **Population:** this one site's historical sessions. Applicability to other sites, times, or LLM products is unknown.
- **Features:** page-category counts and durations, special-day proximity, operating system, browser, region, traffic type, visitor type, and weekend. Numeric scaling and category vocabulary are fit on training months only; unseen categories use a reserved `UNKNOWN` column.
- **Excluded:** `PageValues`, `BounceRates`, and `ExitRates` because their point-in-time availability is unclear or transaction related; `Month` is excluded so the classifier cannot directly memorize the split. `Revenue` is never a feature.
- **Critical time limitation:** UCI supplies session-level aggregates, not per-event timestamps. Even included page durations may include actions after a useful intervention point. This is **retrospective completed-session classification**, not evidence of valid live, pre-purchase inference.

## Frozen evaluation protocol

The split and model recipe are in [train.py](train.py). Train on February, March, May, June, July, August (6,608 sessions, 731 positives); select a decision threshold on September–October (997, 201); evaluate once on November–December (4,725, 976). The latter is a calendar-shift stress test. The source has no year or event timestamps, so it is not a full chronological holdout.

Fit an L2-regularized logistic regression with the parameters fixed in code. Compare to a constant score equal to **training** prevalence. Choose threshold by validation F1 from 0.05–0.95 in 0.01 steps, breaking ties toward fewer alerts. Report average precision (AP), Brier loss, 10-bin expected calibration error (ECE), confusion counts, and session bootstrap percentile intervals. Bootstrapping sessions does not capture month-level dependence.

## Reproduce

Python 3.11+ with [requirements.txt](requirements.txt) (`numpy==2.3.5`) is used for the frozen numbers below.

```sh
python3 -m pip install -r projects/shopper-behavior-classifier/requirements.txt
curl -L 'https://archive.ics.uci.edu/static/public/468/online%2Bshoppers%2Bpurchasing%2Bintention%2Bdataset.zip' -o /tmp/online-shoppers.zip
python3 -m unittest discover -s projects/shopper-behavior-classifier -p 'test_*.py'
python3 projects/shopper-behavior-classifier/train.py /tmp/online-shoppers.zip --output /tmp/shopper-report.json
```

Run commands from the repository root. The script checks the archive SHA-256 (`2972e6184d3ad7beaaa831d9fc2b059dc3ee29df69d1ec593c466a5cd8485d14`) before reading it. [Frozen machine-readable output](results.json) contains all counts and slices.

## Observed result and decision

| Split / system | AP ↑ | Brier ↓ | ECE ↓ | Precision | Recall | False positives |
|---|---:|---:|---:|---:|---:|---:|
| Train / model | 0.233 | 0.091 | 0.021 | 0.141 | 0.985 | 4,385 |
| Validation / model | 0.220 | 0.168 | 0.066 | 0.200 | 0.935 | 754 |
| Held-out Nov–Dec / model | 0.360 | 0.154 | 0.061 | 0.232 | 0.987 | 3,183 |
| Held-out / prevalence baseline | 0.207 | 0.173 | 0.096 | 0.207 | 1.000 | 3,749 |

Threshold is 0.05, chosen on validation. The held-out AP 95% session-bootstrap interval is **0.335–0.390**. The Brier improvement over the constant-score baseline is **0.0191** (95% session-bootstrap interval **0.0167–0.0217**). These intervals quantify row resampling only; they do not establish future-month reliability.

**Failure slices:** December precision is **0.142** (1,282 false positives among 1,727 sessions), versus **0.283** in November. Returning visitors have **0.222** precision (2,607 false positives). The `Other` visitor group has only 84 examples, so its apparent AP is too fragile to use as an acceptance claim. Purchase prevalence changes from **0.111** in training to **0.207** in held-out months; that contributes to calibration and threshold instability.

**Decision: hold for any user-facing action.** The ranking signal is measurable, but the selected threshold alerts on most non-purchasers, calibration shifts, and the dataset cannot verify feature availability at decision time. Next experiment: collect event-timestamped labels and features, define a pre-action prediction time, compare month-blocked holdouts, agree on an alert-cost or precision floor with a stakeholder, and rerun the gate. The decision criteria here are a post-analysis judgment, not a preregistered release gate.
