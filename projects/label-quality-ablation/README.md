# What does corrupted training data do to a fixed model?

**Posting test:** [Mercor Research Scientist, Environments/Data/Post-Training](https://jobs.ashbyhq.com/mercor/1dcab154-b92d-4a5f-aed5-b1b8c049cdbc) asks for methods to measure data quality and its causal impact on model performance. This project runs a controlled label-quality intervention on a real public dataset. It isolates the effect of **this deliberate corruption** on **this fixed training recipe**, not the general value of any dataset for frontier LLM training.

## Source and protocol

The data are the [UCI Online Shoppers Purchasing Intention Dataset](https://archive.ics.uci.edu/dataset/468/online%2Bshoppers%2Bpurchasing%2Bintention%2Bdataset), Sakar and Kastro (2018), [DOI 10.24432/C5F88Q](https://doi.org/10.24432/C5F88Q), CC BY 4.0. Download the original archive yourself; it is not committed here. The script checks its SHA-256 before use.

Use the [shopper classifier](../shopper-behavior-classifier/) train-only feature encoder and fixed logistic-regression recipe. Train on February–August's available months (6,608 sessions, 731 purchases) and evaluate the same unchanged November–December sessions (4,725, 976). The intervention swaps either **20%** or **50% of the positive training labels** with an equal count of negative labels. This keeps training prevalence fixed while deliberately making labels wrong. Each treatment uses 20 specified random seeds; the clean arm is trained once. Features, model settings, and test labels are identical across arms. No threshold is tuned for this project; outcomes are average precision (AP), Brier loss, and ECE.

**Scope limit:** this reuses a test period already inspected in the shopper-classifier project. It is a retrospective, exploratory ablation, not a new blind holdout. The balanced swap is an artificial error mechanism and cannot establish the impact of real annotation errors. November–December also differ sharply in prevalence from training months.

## Observed results

| Training labels | Changed labels | Mean held-out AP ↑ | AP range over seeds | Mean Brier ↓ |
|---|---:|---:|---:|---:|
| Clean | 0 | 0.3596 | — | 0.1540 |
| Swap 20% of positive labels with negatives | 292 | 0.3543 | 0.3468–0.3604 | 0.1575 |
| Swap 50% of positive labels with negatives | 732 | 0.3415 | 0.3190–0.3710 | 0.1633 |

The **average** AP drop is 0.0052 at 20% and 0.0181 at 50%; Brier worsens by 0.0036 and 0.0093. One high-noise seed beats the clean AP, so the direction is **not** guaranteed for an individual corruption draw. The [full result](results.json) lists every seed, metric, and protocol setting. Seed ranges are variability diagnostics, not confidence intervals for future sites or months.

**Decision:** label integrity matters for this recipe on average, but the magnitude is modest relative to the domain shift and varies by which labels are wrong. A real post-training data program should measure its own label-error mechanism, use expert review, and confirm downstream model impact on an untouched future or partner-specific task before changing a data filter.

## Reproduce

From the repository root, with Python 3.11+ and [requirements.txt](requirements.txt) (`numpy==2.3.5`):

```sh
python3 -m pip install -r projects/label-quality-ablation/requirements.txt
curl -L 'https://archive.ics.uci.edu/static/public/468/online%2Bshoppers%2Bpurchasing%2Bintention%2Bdataset.zip' -o /tmp/online-shoppers.zip
python3 -m unittest discover -s projects/label-quality-ablation -p 'test_*.py'
python3 projects/label-quality-ablation/ablate.py /tmp/online-shoppers.zip --output /tmp/label-ablation.json
```

The four tests check deterministic balanced swaps, unchanged prevalence, zero-treatment identity, invalid input rejection, and metric direction. [Code](ablate.py) contains the exact intervention and draws.
