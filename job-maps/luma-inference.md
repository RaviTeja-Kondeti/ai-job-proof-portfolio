# Luma — Software Engineer, Inference

[Employer posting](https://jobs.ashbyhq.com/lumaai/c4b9ff5f-40b2-40d4-9f6f-8b7aad9b8860) · Ashby last published: 2026-10-08 · Redwood City base: $195k–$345k. This is a **large-scale inference systems** role. The candidate's five years in ML/AI and public C++ work do not establish Kubernetes, GPU-fleet, or thousand-machine serving experience.

Each distinct candidate-facing statement, including Luma's mission and first-90-day expectations, becomes a test and small project. **Built** means a narrow inspectable artifact exists; **planned** is still a gap.

| Posting signal | Test | One project / state |
|---|---|---|
| Unified general intelligence operates in the physical world | Can model serving support multimodal, real-world tasks? | **Planned:** multimodal inference task and latency benchmark. |
| Vision is central beyond language | Can image/video inputs be served and evaluated? | **Planned:** vision-language request pipeline. |
| Own model serving | Can an architecture be integrated without service regression? | **Planned:** versioned model adapter and rollout. |
| Deploy across thousands of machines | Can jobs be scheduled and observed across a fleet? | **Planned:** distributed fleet simulation and runbook. |
| Keep expensive GPUs busy while meeting SLOs | Can utilization and tail latency be balanced? | **Planned:** constrained inference scheduler benchmark. |
| This is systems work, not pure modeling | Is hands-on serving/operations experience verifiable? | **Candidate verification:** real production systems, not ML-only tenure. |
| Integrate new model architectures into the engine | Can interfaces handle changing model shapes and requirements? | **Planned:** model architecture compatibility contract. |
| Collaborate across research, engineering, infrastructure | Can one change be validated end to end? | **Planned:** cross-team performance review and rollout record. |
| Measure/profile inference job lifetimes | Are queue, run, retry, and completion times visible? | **Planned:** inference trace collector and lifecycle dashboard. |
| Automate and test services for uptime | Do faults recover without losing requests? | **Planned:** service failure-injection and SLO test. |
| Manage workloads across hardware providers | Can placement honor capacity and cost constraints? | **Planned:** multi-provider placement simulator. |
| Scale deployments across thousands of machines | Does rollout remain safe as fleet size grows? | **Planned:** progressive rollout simulator. |
| Scheduling meets SLOs | Can priority, batching, and preemption be evaluated? | **Planned:** SLO-aware scheduling experiment. |
| CI/CD for checkpoints and SDKs | Are artifacts versioned and rollback-ready? | **Planned:** checkpoint/SDK release manifest and rollback exercise. |
| Days 1–30 diagnose reliability/utilization | Can the top bottleneck be found from traces? | **Planned:** simulated fleet profiling report. |
| Days 30–60 ship a measurable improvement | Does a change improve uptime or utilization versus baseline? | **Planned:** scheduler A/B benchmark and decision memo. |
| Days 60–90 harden deployments | Do regression and failure tests become routine? | **Planned:** deployment runbook and automated regression gate. |
| Strong Python and system architecture | Can a service be designed with explicit constraints? | **Built, small:** [local decision service](../projects/growth-decision-service/); **planned:** real inference service. |
| Model deployment with PyTorch/HF/vLLM/SGLang/TensorRT-LLM | Has a model been served with one of these? | **Candidate verification:** actual deployments; **planned:** local vLLM-style service benchmark. |
| Queues, traffic control, fleet management | Can backpressure and admission control be tested? | **Planned:** bounded queue and load-shedding simulation. |
| Linux, Docker, Kubernetes, orchestration | Are deployments reproducible and observable? | **Planned:** container/Kubernetes deployment with probes and SLOs. |
| Redis and S3-compatible storage | Can cache/checkpoint consistency be handled? | **Planned:** cache and object-store failure study. |
| RDMA/NVLink networking is a plus | Can network limits be quantified? | **Planned:** communication-cost model; real hardware access unverified. |
| 100+ GPU scale is a plus | What actual fleet-scale ownership exists? | **Candidate verification:** hardware/run metrics; a toy simulation is insufficient. |
| CUDA or multimedia processing is a plus | Is low-level acceleration or media handling demonstrated? | **Existing partial systems code:** [Vortex C++ engine and benchmark](https://github.com/RaviTeja-Kondeti/vortex/tree/da5cdc85f7db59c21871b737ee9d7ad841c97dff); **CUDA/multimedia remain unverified**. See [audit](../EXISTING_WORK_AUDIT.md). |

Equal-opportunity and location details are application facts, not proof. The posted band includes values below $250k. Even at the upper end, the central gap is large-scale GPU inference operations.
