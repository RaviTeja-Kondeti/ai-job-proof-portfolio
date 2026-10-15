# Baseten — Post-Training Applied Researcher

[Employer posting](https://jobs.ashbyhq.com/baseten/2d18b2aa-b6fc-4f1c-8936-33b03255a090) · Ashby last published October 7, 2026 · San Francisco hybrid · posted compensation $200k–$275k plus equity. Only the upper $25k of the posted salary band exceeds the user's $250k base target; an offer above that target is not guaranteed. The date is last publication activity, not confirmed original creation.

**Fit caution:** the posting explicitly seeks hands-on LLM fine-tuning and RL, production post-training, customer-facing work, and depth in GRPO/PPO. The user has reported five years of broad data science/ML/GenAI/LLM experience, but has not supplied evidence of those specific qualifications. This is a conditional role, not a verified match.

Every substantive employer statement below becomes a distinct small-project test. Built links are narrow evidence; synthetic demonstrations do not establish training frontier models, customers, publication records, or production ownership. Company funding, benefits, equal opportunity, and legal notices are applicant context rather than candidate accomplishments.

| ID | Posting signal, paraphrased | Reviewer test | One project and proof state |
|---|---|---|---|
| B01 | Baseten powers mission-critical inference | Can a model meet a reliability contract under faults? | **Planned:** inference fault-injection benchmark and recovery runbook. |
| B02 | Its customers are frontier AI product companies | Can model quality be measured on customer-specific tasks? | **Planned:** domain-specific eval contract with customer acceptance cases. |
| B03 | Applied research, flexible infrastructure, and developer tooling work together | Can an experiment become an operable tool? | **Planned:** research-to-tool pipeline with API and reproducibility checks. |
| B04 | Models must reach production, not stop at research | Is a training artifact deployable and monitorable? | **Planned:** train-to-inference release trace with rollback. |
| B05 | The company is growing quickly | Can scope and quality be maintained under short iterations? | **Planned:** one-week post-training sprint log with quality gates. |
| B06 | Post-train open models on specialized customer tasks | Does a tuned open model beat a frozen closed-model benchmark fairly? | **Planned:** task-specific open-versus-closed evaluation with cost and contamination notes. |
| B07 | Work directly with stakeholders | Can a customer need become labels, a reward, and acceptance metrics? | **Planned:** customer-requirements-to-curriculum brief; actual stakeholder experience requires work history. |
| B08 | Extract signal from complex domain data | Are noisy examples filtered without erasing hard cases? | **Built, narrow:** [synthetic post-training data checks](../projects/post-training-data/); **planned:** separate real domain-data signal study. |
| B09 | Build reward functions | Does reward correlate with task success and resist shortcuts? | **Planned:** reward-design benchmark with adversarial counterexamples. |
| B10 | Build training environments | Can tool actions and state transitions be replayed? | **Built, narrow:** [synthetic agent trajectory evaluator](../projects/agent-trajectory-eval/); **planned:** distinct multi-turn training environment. |
| B11 | Build evaluation harnesses | Does the harness catch task failures and variance? | **Built, partial:** [LLM evaluation prototype](../projects/llm-evaluation/); **planned:** repeated-run domain eval with confidence intervals. |
| B12 | Build training pipelines | Are data, model version, reward, and checkpoints traceable? | **Planned:** end-to-end post-training pipeline with provenance. |
| B13 | Trained models serve millions | Can throughput, latency, and safety scale together? | **Planned:** production-style load test; real scale needs employment evidence. |
| B14 | Hands-on LLM fine-tuning | Has the candidate run and debugged an actual tuning job? | **Planned:** small open-model fine-tuning run with frozen test and error slices. |
| B15 | Hands-on RL | Can a policy update be implemented and diagnosed? | **Planned:** executable PPO/GRPO experiment with gradients and ablations. |
| B16 | Ship model changes into production | Is a safe deployment plan backed by telemetry? | **Planned:** shadow/canary rollout simulator; real production ownership needs history. |
| B17 | Turn customer requirements into curriculum | Are examples ordered to improve target behavior? | **Planned:** curriculum ordering comparison on a fixed customer-like task. |
| B18 | Balance rigor and iteration speed | Can fast decisions still preserve a frozen evaluation? | **Planned:** two-stage experiment protocol with stop rules. |
| B19 | Recent on-policy research is part of the team's approach | Can on-policy and offline data mixes be compared fairly? | **Planned:** on-policy/offline mixture ablation with provenance. |
| B20 | Long-running agents motivate KV-cache research | Does cache strategy change memory and latency under long interactions? | **Planned:** long-context cache benchmark with quality check. |
| B21 | Black-box distillation is in the research context | Can a student learn from sampled teacher behavior with traceable costs? | **Planned:** teacher-query distillation study with error audit. |
| B22 | SFT pipelines | Does supervised tuning improve held-out task success? | **Built, narrow:** [synthetic SFT record validation](../projects/post-training-data/); **planned:** actual SFT run. |
| B23 | GRPO pipelines | Are group advantages, KL, and update stability correct? | **Planned:** GRPO update implementation with hand-computed gradient fixtures. |
| B24 | DPO pipelines | Can pairwise preferences yield calibrated improvement? | **Built, narrow:** [synthetic preference-record validation](../projects/post-training-data/); **planned:** DPO training comparison. |
| B25 | RLVR pipelines | Is a verifiable reward robust to reward hacking? | **Planned:** verifier-backed reward and adversarial solver tests. |
| B26 | Synthetic data generation | Are generated examples useful, diverse, and leak-free? | **Planned:** synthetic data quality and contamination audit. |
| B27 | Healthcare, code, and legal tasks differ | Can evals adapt to domain risk and error cost? | **Planned:** three-domain evaluation specification with distinct failure severity. |
| B28 | Multi-turn tool use and sandbox execution | Do agents handle state, tools, and unsafe actions? | **Built, narrow:** [trajectory checks](../projects/agent-trajectory-eval/) and [prompt-injection screening](../projects/prompt-injection-screen/); **planned:** sandboxed multi-turn task environment. |
| B29 | Production data should become training signal | Are usage events consented, labeled, and attributable? | **Planned:** privacy-aware production-feedback schema and replay. |
| B30 | Distribution shift affects the reward loop | Does quality survive a shifted month or domain? | **Built, adjacent:** [month-shift classifier evaluation](../projects/shopper-behavior-classifier/); **planned:** post-training shift study. |
| B31 | Diagnose reward hacking | Can a policy exploit the reward without achieving the task? | **Planned:** exploit discovery and reward repair case study. |
| B32 | Diagnose importance-sampling drift | Do off-policy ratios or effective sample size signal failure? | **Planned:** off-policy correction and ESS failure benchmark. |
| B33 | Diagnose advantage-estimation instability | Do baselines, clipping, and variance controls behave as expected? | **Planned:** advantage-variance ablation with learning curves. |
| B34 | Publish and contribute to open-source libraries | Can findings survive public review and be reused? | **Planned:** reproducible write-up and upstream contribution; actual publications remain candidate verification. |
| B35 | GRPO/PPO knowledge beyond recipes | Can group advantage, clipped objective, and KL penalty be derived and tested? | **Planned:** math-to-code GRPO/PPO notebook with finite-difference gradient tests. |
| B36 | Know rewards that train versus rewards that exploit | Are metric and task success separated? | **Planned:** reward-proxy stress suite with withheld human judgment. |
| B37 | Experience with multi-turn agents, beyond single-turn QA | Is stateful tool use evaluated through failure recovery? | **Planned:** multi-turn environment with stateful scoring and replay. |
| B38 | Own data-to-training-to-evaluation-to-deployment | Is each release step reproducible and gated? | **Planned:** complete post-training release manifest and local service. |
| B39 | Production ML experience and a closed training–inference loop | Did real traffic lead to safe model improvement? | **Candidate verification:** actual shipped system and feedback-loop history; demos cannot prove this. |
| B40 | RL frameworks are preferred | Can a framework run be profiled and debugged? | **Planned:** RL trainer integration with reproducible checkpoints. |
| B41 | Top-venue publications are preferred | Does the candidate have peer-reviewed original work? | **Candidate verification:** publication list or preprints with contribution details; project prototypes are not equivalent. |
| B42 | Collaborative, inclusive team | Are disagreements and affected users represented in review? | **Planned:** cross-functional review record and inclusive eval protocol. |

Benefits, equity, insurance, PTO, and 401(k) need applicant review. They are not technical tests. The upper base-band margin is narrow enough that the user should confirm salary expectations early if they pursue this conditional role.
