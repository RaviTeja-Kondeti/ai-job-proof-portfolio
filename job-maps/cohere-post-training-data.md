# Cohere — Member of Technical Staff, Post-Training Data Infrastructure

[Employer posting](https://jobs.ashbyhq.com/cohere/eef82766-7e31-430f-a102-bc33a5022597) · Ashby last published: 2026-10-14. The ATS compensation tiers list US base ranges of $205k–$380k in CA/NY/WA and $175k–$325k elsewhere. The candidate's large-scale pipeline and distributed inference history has not been provided.

The map treats each substantive candidate-facing statement, including company context and values, as a separate test. **Built** links are runnable but limited synthetic proof; **planned** rows have no completed proof.

| Posting signal | Test | One project / state |
|---|---|---|
| Security-first enterprise AI | Can sensitive data enter a pipeline with access controls and deletion? | **Planned:** permissioned training-data pipeline and retention audit. |
| Frontier foundation models solve business problems | Can model-data choices be tied to downstream utility? | **Planned:** post-training data ablation with user-task evaluation. |
| Models are trained and deployed for enterprise use | Can training artifacts be reproduced and safely released? | **Planned:** versioned model/data release workflow. |
| Each contributor raises model capability and customer value | Can an engineering change show model and customer impact? | **Planned:** data-recipe impact study with cost and quality metrics. |
| Researchers, engineers, designers collaborate globally | Can requirements and tradeoffs be communicated across roles? | **Planned:** cross-functional data contract and decision record. |
| Own pipelines for SFT, RL, synthetic, human data | Can each source be ingested with provenance and validation? | **Built, tiny:** [three-type dataset builder](../projects/post-training-data/); **planned:** real ingestion pipeline. |
| Researchers and annotation teams iterate rapidly | Does a new recipe reach evaluation quickly without breaking history? | **Planned:** recipe-to-dataset continuous integration workflow. |
| Build SFT pipelines | Are instruction/completion examples clean and versioned? | **Built, toy:** [SFT schema checks](../projects/post-training-data/); **planned:** production ingestion. |
| Build preference pipelines | Are pairwise preferences validated for ties and annotator disagreement? | **Built, partial:** [invalid-pair rejection](../projects/post-training-data/); **planned:** annotator agreement report. |
| Build RL post-training pipelines | Can rollout and reward records be joined correctly? | **Built, toy:** [RL record validation](../projects/post-training-data/); **planned:** trajectory joins. |
| Dataset quality | Are duplicates, contamination, toxicity, and malformed records visible? | **Built, partial:** [duplicate/malformed rejection](../projects/post-training-data/); **planned:** contamination and toxicity checks. |
| Dataset versioning and reproducibility | Can one run be rebuilt from exact inputs? | **Built, partial:** [deterministic content manifest](../projects/post-training-data/); **planned:** full replay command. |
| Research recipes become production components | Can experimental logic survive scale and varied inputs? | **Planned:** recipe package with adapter and failure tests. |
| Scale inference for synthetic data generation | Are throughput, tail latency, and cost measured? | **Planned:** batched generation throughput benchmark. |
| Scale model-based grading | Is grader drift and calibration monitored? | **Planned:** grader-vs-human agreement and load test. |
| Efficient, consistent training schemas | Are SFT, preference, and RL records structurally compatible? | **Planned:** schema registry and migration tests. |
| Pipelines keep pace with model research | Can backlog and bottlenecks be measured? | **Planned:** pipeline lead-time and failure dashboard. |
| Strong software engineering | Are code, APIs, tests, and operational docs maintainable? | **Built, small:** [Python tests](../projects/classifier-evaluation/); **planned:** production-scale pipeline package. |
| Large-scale ML data pipelines | Has the candidate operated a relevant system? | **Candidate verification:** actual employment/project scale; toy work is insufficient. |
| Distributed processing and inference track record | Is production scale and ownership verifiable? | **Candidate verification:** system metrics and responsibility; **planned:** distributed demo. |
| SFT, RLHF, DPO understanding | Can data structure and objective differences be explained? | **Planned:** comparative data recipe and training experiment. |
| Clear communication | Can a failure and decision be explained to researchers and operators? | **Planned:** data-release incident and correction memo. |
| Diverse backgrounds are welcome | Can collaboration include alternative perspectives? | **Planned:** documented multi-reviewer dataset design critique. |

Remote-friendly location, benefits, accommodations, applicant screening notice, and scam warning are application facts, not candidate accomplishments. The US pay tiers come from the posting's ATS compensation data; location and level will determine the actual offer. The critical fit question is real large-scale data/inference ownership.
