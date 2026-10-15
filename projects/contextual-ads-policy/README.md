# Contextual ads without a user profile

**Posting line:** [OpenAI Monetization AI/ML](https://jobs.ashbyhq.com/openai/80f9f564-d789-47bc-91c3-3babf5a1a33d) says its new group builds user-first, privacy-preserving monetization products, including ads. This small project tests one part of that statement: whether a ranker can choose relevant ads from the current topic while refusing personal fields and honoring measurement consent. It also gives narrow supporting evidence for the privacy and trust wording in [OpenAI MLE Growth](https://openai.com/careers/machine-learning-engineer-growth-san-francisco/).

## Contract and threat model

- The request accepts **only** an approved topic, Boolean measurement consent, and an ad-count limit. Any additional key—including user ID, age, gender, browsing history, or location—is rejected. Unknown or sensitive topics return no ad. There is no session ID or user profile in the ranker.
- Ads must be approved, have remaining budget, and meet a **0.60 contextual relevance floor**. Relevance is a fixed, synthetic function of topic match and creative quality. Bid breaks ties, rather than overruling the relevance floor.
- Consent does not change the ranking. Denied-consent calls leave the aggregate counters untouched. Consenting calls update only total requests and total ads served; there are no per-request rows or timestamps.
- The bid-only comparison uses the same approved and budget-eligible catalog, then picks the highest bid without a relevance floor. It illustrates the objective tradeoff; it is **not** an industry ad-serving baseline.

This reduces obvious profiling and measurement leakage in the local contract. It does **not** establish legal privacy compliance, secure ingestion, differential privacy, deletion, frequency caps, budget concurrency, ad-policy review, or production safety. Topic labels can still reveal interests, so a real system would need privacy review and careful context retention rules.

## Reproduce

From the repository root, using Python 3.10+ standard library:

```sh
python3 -m unittest discover -s projects/contextual-ads-policy -p 'test_*.py'
python3 projects/contextual-ads-policy/policy.py
```

The six tests check personal-field rejection, consent invariance and aggregate counting, sensitive-topic suppression, safety/budget/relevance filtering, measured tradeoff, and invalid inputs. [Code](policy.py) and [frozen output](results.json) contain the exact inputs and results.

## Synthetic result and decision

Across four fixed topics—coding, education, music, and travel—the contextual policy gives **0.870 mean relevance** with **1.25 mean bid**. The bid-only policy gives **0.585 mean relevance** with **5.00 mean bid**. The higher relevance and lower bid are properties of this tiny hand-built catalog; they are **not** estimates of user benefit, advertiser value, revenue, or generalization.

**Decision:** retain this as a privacy-contract prototype only. Before any live experiment, define ad approval rules, a measured user-value metric, budget accounting, privacy and safety review, and an experiment with guardrails. A portfolio demo cannot prove experience deploying ads or collaborating with a real product team.
