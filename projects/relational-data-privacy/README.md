# Remove direct identifiers while preserving relational joins

**Posting test:** [Handshake AI, Member of Technical Staff, AI Engineering](https://jobs.ashbyhq.com/handshake/08651bf1-c977-49d4-9a82-e8a770bb9970) asks for systems that make acquired data safer by removing personal information **while preserving the structure that makes it useful**. This project supplies a narrow, runnable demonstration using wholly synthetic customer and order tables. It does not establish production privacy engineering or compliance.

## Contract

- Strictly validate the two input schemas, unique IDs, nonnegative integer-cent amounts, and every order's customer foreign key. Unknown columns and orphan orders fail closed.
- Replace customer and order IDs with separate HMAC-SHA256 tokens; use the same customer token in both output tables so joins still work. Remove names and email addresses entirely.
- Coarsen state and age decade until every released **state × age cell, ignoring tokens and orders**, contains at least two customers. If a rare-cell pool remains too small, suppress both fields for every row.
- Report join integrity, exact total-revenue preservation, minimum quasi-cell size, and fractions of state and age bands retained. [Frozen synthetic output](results.json) has nine customers and twelve orders, no orphan, exact revenue, a minimum quasi-cell of two, 7/9 states retained, and 4/9 age bands retained.

The public demo key in [deidentify.py](deidentify.py) exists only for reproducible synthetic data. A real pipeline needs secret management, access control, rotation, deletion, legal review, and a tested release process. **These rows are pseudonymized, not anonymous.** Stable tokens, unique amounts, relational patterns, and external knowledge can re-identify people even when the coarse demographic cells contain two records. The cell count is a diagnostic for two quasi fields, **not a k-anonymity guarantee for the dataset**. Do not use this script to publish real personal data.

## Reproduce

From the repository root with Python 3.10+ standard library:

```sh
python3 -m unittest discover -s projects/relational-data-privacy -p 'test_*.py'
python3 projects/relational-data-privacy/deidentify.py
```

The six tests check direct-identifier removal, unchanged joins and revenue, domain-separated tokens, small-cell suppression, orphan/extra-field rejection, and key/ID validation. A useful next test would measure re-identification risk using a realistic attacker model and inspect whether a trained model retains its utility after masking. Neither is claimed here.
