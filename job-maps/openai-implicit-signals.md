# OpenAI — Machine Learning Engineer, Implicit Signals

[Employer posting](https://jobs.ashbyhq.com/openai/a01fc9ed-de08-4326-9206-4ee3f08000dc) · Ashby last published: 2026-10-13 · posted base: $381k–$510k.

Every candidate-evaluating statement in the posting is paraphrased as a test and a separate small project. **Built** links are runnable; **planned** rows have no completed proof. Public synthetic work cannot establish actual production ownership or employment history.

| Posting signal | What it tests | One project / state |
|---|---|---|
| Research teams need fast, reliable behavior feedback | Can measurements support an actual research decision? | **Planned:** model-change feedback dashboard with decision cases. |
| Classification and evaluation systems are the team's core | Can you build a classifier and a valid evaluation around it? | **Built, partial:** [trained session classifier and frozen evaluation](../projects/shopper-behavior-classifier/) and [synthetic release gate](../projects/classifier-evaluation/); production lifecycle unproven. |
| Accuracy, efficiency, and scale all matter | Can quality be traded against compute honestly? | **Planned:** quality-latency-cost Pareto study. |
| Work closely with researchers to make measurements useful | Can an open-ended concern become a measurable target? | **Planned:** researcher-to-metric requirements memo and signoff. |
| Span development, rigorous evaluation, and production inference | Can you own the full path to reliable serving? | **Planned:** deployed classifier service with evaluation gate. |
| Own experimentation through deployment and iteration | Is each model version traceable after release? | **Planned:** versioned training-to-rollback workflow. |
| Turn open-ended behavior questions into ML problems | Are labels, target population, and errors precisely defined? | **Built, partial:** [label and target-population guide](../projects/shopper-behavior-classifier/README.md); real researcher requirements remain unverified. |
| Develop new classification/evaluation methods | Is a method better than a simple baseline on held-out data? | **Planned:** baseline-versus-new-method comparison. |
| Combine traditional ML, evaluation, and real-time engineering | Does the classifier work under service constraints? | **Planned:** low-latency API with measured quality and throughput. |
| Supervised fine-tuning | Can a labeled dataset improve a model without leakage? | **Planned:** supervised fine-tuning experiment with frozen test set. |
| Distillation | Can a smaller student preserve teacher quality? | **Planned:** teacher-student distillation and error comparison. |
| Deployment and production inference | Can an artifact be served, monitored, and rolled back? | **Planned:** classifier serving deployment with rollback rehearsal. |
| Build, deploy, and operate production feedback systems | Does the system remain useful after release? | **Planned:** feedback service with operations runbook and synthetic incident. |
| Optimize serving and batching | What batch size improves throughput without harming tail latency? | **Planned:** batching benchmark under varied traffic. |
| Optimize caching | Does cache reuse reduce cost without serving stale answers? | **Planned:** cache hit/staleness experiment. |
| Optimize throughput, latency, utilization, and cost | What is the feasible operating frontier? | **Planned:** load-test report with p50/p95, QPS, GPU/CPU utilization, and cost. |
| Validate model quality and efficiency before deployment | Can a release gate reject an attractive but weak model? | **Built, partial:** [slice-aware release gate](../projects/classifier-evaluation/); **planned:** efficiency gate. |
| Reliability and observability after deployment | Can you spot data, model, or service regressions? | **Planned:** production-style telemetry and alert rules. |
| Diagnose issues and improve performance | Can you reproduce a failure and validate the fix? | **Planned:** classifier incident and corrective-action case study. |
| Rigorous accuracy measurement | Are confusion counts and decision thresholds explicit? | **Built, partial:** [held-out confusion counts and validation-selected threshold](../projects/shopper-behavior-classifier/results.json); no production measurement. |
| Calibration | Do predicted probabilities reflect observed frequencies? | **Built, partial:** [real-data Brier and ECE diagnostics](../projects/shopper-behavior-classifier/results.json); month-shift ECE remains high. |
| Generalization | Does performance hold on a shifted population? | **Built, partial:** [November–December shift test and bootstrap intervals](../projects/shopper-behavior-classifier/); another year and live traffic untested. |
| Measurement bias | Could labels or evaluation slices hide systematic errors? | **Built, partial:** [month and visitor-type failure slices](../projects/shopper-behavior-classifier/README.md); **planned:** independent label-bias audit. |
| Production tradeoffs from evaluation | Can a report lead to a clear ship/hold decision? | **Built, partial:** [hold decision tied to false positives, calibration, and feature timing](../projects/shopper-behavior-classifier/README.md); no deployed release gate. |
| Engineer reliable integration and safe rollout | Are canary, shadow, and rollback paths tested? | **Planned:** integration contract and canary rollout simulator. |
| Reusable training, evaluation, and deployment tools | Can others rerun and extend the workflow? | **Built, partial:** [reproducible training, evaluation, and tests](../projects/shopper-behavior-classifier/); deployment tool and CI unbuilt. |
| Translate researcher and data-scientist needs into objectives | Are success criteria agreed before modeling? | **Planned:** stakeholder brief, metric contract, and acceptance test. |
| ML projects from formulation to production | What real deployment did the candidate own? | **History verification:** obtain actual shipped system evidence; portfolio demo is insufficient. |
| Supervised learning, statistics, experimental design | Can methods withstand a baseline and uncertainty check? | **Built, partial:** [trained model against frozen prevalence baseline with bootstrap intervals](../projects/shopper-behavior-classifier/); no randomized experiment. |
| Imperfect labels and systematic errors | Do label disagreements change conclusions? | **Planned:** double-label audit and disagreement sensitivity study. |
| Maintainable production ML software | Can code be tested, observed, and changed safely? | **Planned:** typed package, CI, service tests, and runbook. |
| Quality, latency, compute-cost reasoning | Can the candidate choose an operating point explicitly? | **Planned:** Pareto decision memo backed by load tests. |
| Scientific judgment plus shipping | Can a limited result be released with transparent caveats? | **Built, partial:** [published negative deployment decision](../projects/shopper-behavior-classifier/README.md); no preregistered production release. |
| Open-ended researcher/engineer collaboration | Can disagreement become a better experiment? | **Planned:** cross-functional review and decision log. |
| AI agents used fluently across workstreams | Is the AI-assisted workflow auditable and correct? | **Planned:** agent-assisted build log with human checks. |
| Distillation, representation learning, calibration, efficient inference are a plus | Is there depth in at least one advanced topic? | **Built, narrow:** [real-data calibration and shift diagnostics](../projects/shopper-behavior-classifier/); **planned:** distillation experiment. |
| Research and deployment serve a broad public benefit | Can success include user impact and safety constraints? | **Planned:** classifier harm model and user-impact gate. |
| Diverse perspectives and human needs guide the work | Are edge populations and accessibility part of review? | **Planned:** inclusive evaluation protocol with segment review. |

The posting also contains compensation, benefits, hybrid-work, accommodations, privacy, equal-opportunity, and legal notices. These are application and employer-policy checks, not candidate accomplishments. The candidate's actual degree, past systems, production ownership, and collaborative examples remain unverified.
