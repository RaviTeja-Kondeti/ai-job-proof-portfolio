# Eight-week proof plan

Use roughly one focused hour per day. Every role map identifies **all substantive tests**; this schedule chooses the eight projects with the highest shared value across current roles. Each week should end with a reproducible result, a short methods note, and a direct link from the relevant map. Existing toy projects are starting points, not finished claims.

| Week | Ship one reviewable project | Acceptance evidence | Primary role tests |
|---|---|---|---|
| 1 | Growth policy backtester | **Started:** [synthetic delayed-signal comparison](projects/growth-backtest/) with budget and change limits. Still needs uncertainty analysis and defensible off-policy evaluation. | [OpenAI Growth](job-maps/openai-growth.md): allocation, simulation, incrementality |
| 2 | Production-style growth decision service | **Started:** [local versioned decision API](projects/growth-decision-service/) with validation, consent, caps, idempotency, fallback, and counters. Still needs deployment, observability, canary, and rollback. | [OpenAI Growth](job-maps/openai-growth.md): end-to-end ownership, reliability |
| 3 | Trained behavior classifier and evaluation set | **Started:** [real public-data session classifier](projects/shopper-behavior-classifier/) with label guide, month-shift holdout, calibration, bootstrap intervals, failure slices, and hold memo. Still needs event-timestamped features, imperfect-label audit, and deployment evidence. | [OpenAI Implicit Signals](job-maps/openai-implicit-signals.md): supervised learning and rigorous evaluation |
| 4 | Inference performance and safe rollout | Load-test batching/cache variants, p95 latency, throughput, compute/cost estimate, canary gate | [OpenAI Implicit Signals](job-maps/openai-implicit-signals.md): serving and operations |
| 5 | First real public provider benchmark | Independent dated ground truth, frozen sample, fair adapter contract, uncertainty intervals, replayable release | [Firecrawl Benchmarks](job-maps/firecrawl-benchmarks.md): central shipped-work test |
| 6 | Vendor-challenge and leaderboard release | Public methods page, downloadable rows, dispute protocol, correction log, second dated run | [Firecrawl Benchmarks](job-maps/firecrawl-benchmarks.md): scrutiny and weekly publication |
| 7 | Experimentation and stochastic LLM evaluation toolkit | **Started:** [synthetic A/B validity audit](projects/experiment-audit/). Still needs power/intervals, repeated LLM runs, task-level failures, and a written decision. | [Glean Applied Scientist](job-maps/glean-applied-scientist.md) |
| 8 | Post-training data pipeline and grounded agent integration | Provenance, versioned SFT/preference/RL records, quality gates, schema tests, agent evaluation and runbook | [Cohere Data Infrastructure](job-maps/cohere-post-training-data.md) and [WRITER AI Engineer](job-maps/writer-ai-engineer.md) |

## Rules for each weekly release

1. Put the source posting, its date evidence, and the exact test in the project README.
2. Freeze evaluation data before tuning; document any data that a model or provider could have seen.
3. Publish commands, inputs or lawful substitutes, metrics, failure cases, and limitations.
4. Separate synthetic demonstrations from real observations and personal employment claims.
5. Update each affected map from **planned** to **built** only after the project runs and its output is inspected.

## Candidate-supplied evidence still required

The resume, degree, actual job dates, shipped production systems, B2B/GTM work, benchmark releases, distributed-systems scale, work authorization, and desired salary floor cannot be inferred from this repository. These determine which roles are genuinely eligible and which proof projects are worth prioritizing.
