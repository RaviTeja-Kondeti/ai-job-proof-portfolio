# OpenRouter — Software Engineer, Trust & Safety

[Employer posting](https://jobs.ashbyhq.com/openrouter/cd5340a1-e787-4916-abb8-a08ab1bb229b) · Ashby last published: 2026-09-21 · Remote US annual base: **$215k–$285k** plus equity. This is a hands-on **production software engineering** role with React/TypeScript/Next.js and live abuse operations. General DS/ML/LLM experience does not establish those requirements.

Every candidate-facing statement is treated as a test. Each row names one small proof project. **Built** links show a limited demonstration; **planned** rows have no completed proof; real production and employment claims require candidate evidence.

| Posting signal | Test | One small project / state |
|---|---|---|
| Route many LLM providers without lock-in | Can abuse controls remain consistent across providers? | **Planned:** provider-independent policy adapter test. |
| Support research, product, and production traffic | Can risk rules distinguish different legitimate usage patterns? | **Planned:** multi-tenant usage-pattern benchmark. |
| Millions of daily requests and payments | Can detection/decision latency and capacity scale? | **Planned:** high-volume event replay and p95 load test. |
| Keep abuse, fraud, malicious users, and illegal content off platform | Are separate harms represented with distinct labels and escalation paths? | **Planned:** abuse taxonomy and enforcement matrix. |
| Detection systems | Can a signal catch abuse at an acceptable false-positive cost? | **Built, toy:** [classifier evaluation](../projects/classifier-evaluation/) and [triage queue](../projects/abuse-review-workflow/); real detection unverified. |
| Automated action heuristics | Does automation stop before an unsupported harmful action? | **Built, toy:** [human-review enforcement boundary](../projects/abuse-review-workflow/). |
| Reviewer tooling | Can reviewers inspect evidence and record a reasoned decision? | **Built, backend-only:** [case/decision audit event](../projects/abuse-review-workflow/); reviewer UI planned. |
| Avoid acting on the wrong account | Is enforcement bound to the reviewed case's account? | **Built, toy:** [queued-case account binding](../projects/abuse-review-workflow/); identity-system integration planned. |
| Prevent novel abuse before patterns stabilize | Does a detector generalize beyond known examples? | **Built, negative example:** [novel low-score abuse remains missed](../projects/abuse-review-workflow/); adaptive detection planned. |
| Limit friction for legitimate developers/enterprises | Are false restrictions and review burden measured? | **Built, synthetic:** [review precision, false restriction, and capacity report](../projects/abuse-review-workflow/). |
| Protect provider relationships and enterprise trust | Can intervention policy be explained and audited? | **Planned:** partner-facing safeguards decision memo. |
| Inference path, payments path, review tools, data platform | Do signals reconcile across systems without identity mistakes? | **Planned:** multi-source event join and data contract. |
| Small team, rapid shipping, high judgment | Can an uncertain incident be handled with traceable decisions? | **Planned:** incident decision log with review and retrospective. |
| Detect early at signup | Can risky signups be separated from legitimate new accounts? | **Planned:** signup-abuse cohort evaluation. |
| Detect payments fraud | Can a fraud model handle delayed chargebacks and base rates? | **Existing partial notebook:** [FraudGuard-ML at audited commit](https://github.com/RaviTeja-Kondeti/FraudGuard-ML/tree/4aeeb0d6b619d3f88b4f368d5d391dc5c7ec9dce); [audit](../EXISTING_WORK_AUDIT.md) notes missing CSVs and reproducibility limits. **Planned:** delayed-label fraud benchmark. |
| Detect usage abuse | Can request patterns be measured across accounts and time? | **Planned:** windowed usage anomaly detector. |
| Detection→human review→restriction pipeline | Can action be traced and replayed safely? | **Built, local toy:** [human-review ledger](../projects/abuse-review-workflow/); production workflow planned. |
| Case queues and evidence summaries | Can reviewer priority reflect risk within limited capacity? | **Built, synthetic:** [score-versus-severity queue](../projects/abuse-review-workflow/); evidence-summary UI planned. |
| Bulk review and enactment | Can bulk actions retain individual case provenance? | **Planned:** bulk-review idempotency and rollback test. |
| Alerting triggers investigations | Are alerts timely and low-noise? | **Planned:** alert precision/latency replay. |
| Content safety on inference path | Can unsafe content be detected with user-impact and appeal safeguards? | **Built, narrow method:** [prompt-injection screening baseline](../projects/prompt-injection-screen/); actual inference content safety planned. |
| KYC or external intelligence sources | Are third-party signals validated, consented, and expiry-aware? | **Planned:** external-risk-source ingestion audit. |
| Make abuse uneconomical | Do interventions change adversary cost without excess user friction? | **Planned:** adversarial cost/response simulation. |
| Investigate incidents directly in data | Can a spike be scoped and separated from false positives? | **Planned:** incident SQL notebook on synthetic events. |
| Analytics plane | Are base rates, cohorts, and causes visible during an incident? | **Planned:** abuse metric layer and incident dashboard. |
| Monitor risk/abuse spikes and fraud | Is drift detected before an enforcement surge? | **Planned:** risk-spike and false-positive monitor. |
| Set technical direction as threats evolve | Can principles and failure modes guide future engineers? | **Planned:** threat-model and architecture decision record. |
| Work with data scientists on risk-model features/training | Are features available at decision time and evaluated out of sample? | **Planned:** time-safe risk-feature pipeline and model comparison. |
| 4+ years operating production systems | Is past ownership documented? | **Candidate verification:** actual employment history and operating metrics. |
| React, TypeScript, Next.js, JS runtimes | Can a reviewer workflow be built in the requested stack? | **Planned:** accessible case-review web UI; these skills are unverified. |
| SQL on large event datasets | Can base rates and false-positive cohorts be queried correctly? | **Planned:** event-warehouse query benchmark. |
| Precision, recall, wrong-decision cost | Can thresholds be chosen under asymmetric harms? | **Built, toy:** [queue precision/recall and failed release gate](../projects/abuse-review-workflow/); calibrated real costs planned. |
| Judgment with incomplete evidence | Can the system abstain and require review? | **Built, small:** [no automatic restriction](../projects/abuse-review-workflow/); appeal process planned. |
| High agency, iterate without tickets | What real initiative was taken and shipped? | **Candidate verification:** actual shipped examples; **planned:** decision/iteration case study. |
| AI-forward coding workflow | Can AI assistance be checked against tests and review? | **Planned:** AI-assisted development log with independent validation. |
| Fluid team boundaries and communication | Can incident findings be explained to technical and nontechnical peers? | **Planned:** cross-team incident report. |
| Discretion with sensitive/disturbing material | Are data access, minimization, and reviewer wellbeing handled? | **Planned:** sensitive-data access and retention design. |
| Adversary adapts | Does a new pattern break the detector and trigger revision? | **Built, synthetic failure:** [missed novel pattern](../projects/abuse-review-workflow/); adaptive red-team exercise planned. |
| Payment tooling/KYC is a plus | Can third-party payment/identity alerts be reconciled? | **Planned:** payment-risk adapter and audit trail. |
| LLM abuse, jailbreaks, injection, key theft, credential misuse | Are attack classes separated and evaluated? | **Built, narrow:** [prompt-injection screening](../projects/prompt-injection-screen/); remaining abuse classes planned. |
| Large analytical stores and observability are a plus | Can event queries and traces support investigations? | **Planned:** ClickHouse/BigQuery-style incident query and trace report. |
| Hosted-AI reporting/provider policy obligations | Are obligations mapped to events and actions? | **Planned:** reporting control matrix reviewed against current policy. |
| Side projects or active AI-infrastructure use are a plus | Is original work inspectable? | **Existing supporting work:** [agent runtime at audited commit](https://github.com/RaviTeja-Kondeti/Twitter-for-AI-Agents/tree/ac297faa87caf90e11f8be0519ac5192840f451b) and [audit of its limits](../EXISTING_WORK_AUDIT.md). |
| Remote US and equal-opportunity terms | Are application facts accurate and acceptable? | **Candidate decision:** location is acceptable; work authorization and terms must be checked privately. |

The posting invites applicants who do not meet every preference, but the full-stack production experience remains a major fit check. The listed salary can exceed $250k only in its upper portion. The synthetic review workflow fails its own recall gate and cannot be presented as production trust-and-safety experience.
