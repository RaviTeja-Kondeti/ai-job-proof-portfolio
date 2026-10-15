# Cartesia — Research Engineer, Data Infrastructure (Language Modeling)

[Employer posting](https://jobs.ashbyhq.com/cartesia/6ca9b352-6a7b-42a3-a7c4-8f071712db90) · Ashby last published: 2026-09-24 · San Francisco annual base: **$200k–$350k** plus equity. This is a foundation-model **pretraining data-systems** role. The candidate's stated GenAI/LLM background does not by itself prove massive-scale ingestion, data loading, vendor management, or model-training ablations.

Each candidate-facing line is treated as a test. Every row gives one small proof project. **Built** links demonstrate only a narrow method; **planned** rows have no completed proof. Employment-scale claims require the candidate's real history.

| Posting signal | Test | One small project / state |
|---|---|---|
| Build AI that learns from and interacts with the world | Can a data choice be tied to a measurable downstream model behavior? | **Planned:** input-source ablation with held-out interaction tasks. |
| Invent efficient foundation-model architectures, including SSMs | Does data formatting/loading meet a new architecture's constraints? | **Planned:** SSM-versus-transformer batch-shape/data-loader comparison. |
| Combine model innovation, systems engineering, and product design | Can a research data recipe become a usable product-facing capability? | **Planned:** research-to-product data contract and evaluation report. |
| Ship cutting-edge models and experiences | Does a new data recipe survive release checks and user-task evaluation? | **Planned:** versioned model-data release exercise. |
| Data is the lifeblood of models | Is data quality measured as a model-input quality gate? | **Built, narrow:** [record validation and provenance](../projects/post-training-data/); pretraining quality remains planned. |
| Build datasets and systems that power pretraining | Can a corpus be reproduced from a manifest and processing code? | **Planned:** public-text pretraining corpus builder with content hash. |
| Acquire massive datasets | Can sources be inventoried, licensed, and acquired reproducibly? | **Planned:** source catalog with rights and availability checks. |
| Process and curate massive datasets | Can throughput, rejection rates, and quality be tracked by stage? | **Planned:** streaming text-curation pipeline benchmark. |
| Partner with research on data characteristics/composition | Does changing mixture weights alter held-out quality? | **Planned:** frozen data-mixture ablation and researcher decision memo. |
| Infrastructure directly shapes model capability and quality | Is a data improvement linked to a model outcome? | **Planned:** data-to-eval impact trace. |
| Ingest and combine massive text datasets | Are formats normalized with provenance and bounded memory? | **Planned:** multi-source ingestion with streaming parser. |
| High-throughput, reproducible pipeline | Can a rerun produce identical content hashes and performance numbers? | **Built, tiny method:** [deterministic manifest](../projects/post-training-data/); large-scale replay planned. |
| Preprocessing | Are normalization choices evaluated for language and formatting damage? | **Planned:** preprocessing regression set. |
| Filtering | Does quality filtering remove bad text without losing useful long-tail content? | **Planned:** quality-filter precision/recall audit. |
| Deduplication | Does near-duplicate removal preserve genuinely distinct examples? | **Planned:** document dedup benchmark with asymmetric error costs. |
| Augmentation | Does augmentation improve held-out tasks without contamination? | **Planned:** augmentation ablation with source lineage. |
| Ablate data sources | Does removing one source change model behavior? | **Planned:** source-removal experiment on a small language model. |
| Ablate processing choices | Which transformation actually helps? | **Planned:** preprocessing/filtering factorial experiment. |
| Ablate mixture weights | Can quality versus cost be optimized across sources? | **Planned:** mixture-weight sweep with confidence intervals. |
| Co-design data loading with research/infrastructure | Can a loader avoid bottlenecks and malformed batches? | **Planned:** loader profile and batch-contract tests. |
| Version datasets and experiments | Can an exact model run be linked to an immutable data snapshot? | **Built, partial:** [schema/content hash](../projects/post-training-data/); complete experiment lineage planned. |
| Quality feedback loop between data and model behavior | Can eval failures be traced to source records and corrected? | **Planned:** failure-to-data provenance debugger. |
| Find novel datasets | Can candidate sources be assessed for usefulness, rights, and contamination? | **Planned:** source acquisition scorecard. |
| Manage external data vendors and budgets | Can cost, quality, and licensing terms be compared? | **Planned:** vendor benchmark and cost decision; actual relationship ownership needs candidate evidence. |
| Hands-on ML data infrastructure | Has the candidate operated training pipelines, versioning, loading, and inference integration? | **Candidate verification:** real systems, scale, role, and metrics. Tiny schema code is insufficient. |
| Clean, tested modern engineering; choose the right tool | Can implementation tradeoffs be justified and failure-tested? | **Built, small:** [dataset validation tests](../projects/post-training-data/); **planned:** tool-choice benchmark. |
| Build/evaluate generative-model datasets | Does a data-quality change survive a real model evaluation? | **Planned:** small generative-model training/eval comparison. |
| Understand training and inference | Can training-data changes be connected to inference behavior and cost? | **Planned:** data-to-model-to-serving trace. |
| Parallel processing with Ray/Spark/Kubernetes is a plus | Can a pipeline scale across workers without changing output? | **Planned:** distributed deterministic dedup experiment. |
| Pretraining language models is a plus | Has any model actually been pretrained and evaluated? | **Candidate verification:** actual pretraining work; **planned:** small public-corpus baseline. |
| Ship fast without losing quality or design | Does a short iteration preserve reproducibility and review? | **Planned:** timed pipeline iteration with tests and change log. |
| Open, inclusive collaboration | Can competing research/infrastructure concerns be recorded and resolved? | **Planned:** multi-reviewer design record. |
| In-person SF, eligibility, visa, benefits, and EEO terms | Are location and employment terms acceptable? | **Candidate decision:** user accepts onsite US work; visa/work authorization and offer details remain private application facts. |

The investors, advisors, and benefits provide company context, not evidence of candidate skill. Only the posted upper salary band exceeds $250k. No public prototype here should be described as operation of Cartesia-scale pretraining infrastructure.
