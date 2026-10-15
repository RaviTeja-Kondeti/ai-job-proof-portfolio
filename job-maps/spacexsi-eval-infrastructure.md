# SpaceXSI — Member of Technical Staff, Evaluation Infrastructure

[Employer posting](https://job-boards.greenhouse.io/xai/jobs/5252714007) · Greenhouse first published: 2026-09-30 · Palo Alto base: $180k–$440k. The job board path says xAI while the current posting names **SpaceXSI**. It asks for large-scale distributed systems experience; the candidate's production infrastructure history is unknown.

Each distinct candidate-evaluating statement is treated as a test and small project. **Built** links show narrow synthetic work; **planned** rows remain gaps. Five years in ML does not by itself prove the required distributed-systems experience.

| Posting signal | Test | One project / state |
|---|---|---|
| Super Intelligence stack joins compute, Grok models, and applications | Can one quality signal move between training and product? | **Planned:** model-to-product evaluation trace. |
| Product feedback shapes future models | Can usage-derived signals be de-biased and turned into evals? | **Planned:** production-signal-to-held-out-eval pipeline. |
| RL infrastructure owns evaluation capability | Does an eval system support repeated large training runs? | **Planned:** asynchronous RL-eval orchestration prototype. |
| Infrastructure must be reliable | Do failures retry safely without duplicate scores? | **Planned:** idempotent eval job queue with fault injection. |
| Infrastructure must be efficient | Are throughput and resource costs measured? | **Planned:** evaluation scheduler load study. |
| Infrastructure must be easy to use | Can researchers launch and inspect evals without custom glue? | **Planned:** researcher-facing CLI/API with usability test. |
| Evals run at scale | Can work be partitioned, queued, and recovered? | **Planned:** distributed evaluation worker simulation. |
| Collaborate with modeling/evaluation teams on new evals | Can requirements become a versioned task definition? | **Planned:** eval-spec review and registry. |
| Maintain evaluation signal quality | Do calibration, slices, and contamination checks catch false confidence? | **Built, partial:** [classifier evaluation gate](../projects/classifier-evaluation/); **planned:** drift/contamination monitor. |
| Internal tooling supports next-generation model training | Does feedback arrive with useful latency and provenance? | **Planned:** training-run eval dashboard with lineage. |
| Diagnose inference bottlenecks | Can profiling identify model-serving limits? | **Planned:** inference microbenchmark and bottleneck report. |
| Diagnose capacity-fleet bottlenecks | Can scheduling keep expensive workers utilized? | **Planned:** fleet-capacity simulation with queue metrics. |
| Diagnose async orchestration bottlenecks | Can stuck jobs and backpressure be observed? | **Planned:** async-eval trace and fault study. |
| Build/debug/optimize large distributed systems | What actual scale and operational ownership exist? | **Candidate verification:** production system metrics and responsibility; toy work is insufficient. |
| Dive deep across all layers | Can an observed regression be traced to root cause? | **Planned:** end-to-end eval incident reconstruction. |
| LLM inference experience preferred | Can quality, latency, and cost be measured together? | **Planned:** batched inference tradeoff study. |
| GPU management, scheduling, dynamic optimization preferred | Are scarce accelerators allocated to highest-value evals? | **Planned:** GPU scheduling simulation with capacity constraints. |
| Interfaces for comparing models/evals preferred | Can a reviewer reproduce a comparison and see uncertainty? | **Built, toy comparison:** [provider benchmark structure](../projects/provider-benchmarks/); **planned:** model/eval comparison UI. |
| Application asks for exceptional work in ≤100 words | Can one real owned result be described precisely? | **Candidate verification:** concise account of actual work; synthetic code alone cannot establish impact. |

The posting's salary, benefits, privacy, work authorization, and application-form requests are facts to verify rather than technical portfolio tests. The posted base range is broad and does not predict an individual offer.
