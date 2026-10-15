# Exa — Research Engineer, Index Intelligence

[Employer posting](https://jobs.ashbyhq.com/exa/67310301-d019-4290-9c79-e8d6e70d5d50) · Ashby last published: 2026-10-01 · San Francisco annual base: **$180k–$350k**. The role centers on ML signals that change crawling/indexing choices and improve search. The candidate's large-scale search ownership and production impact are not established by five years of broadly described ML/AI work.

Every substantive statement is read as a test, including the mission, example projects, and collaboration style. Each row names one small proof project. **Built** links are narrow methods, not evidence of web-scale production work; **planned** rows remain open.

| Posting signal | Test | One small project / state |
|---|---|---|
| Applied AI lab building a new search engine | Can an ML idea be judged by search usefulness, not model score alone? | **Built, synthetic:** [index decision and downstream coverage](../projects/index-selection-eval/); real search remains planned. |
| Crawl the entire web | Can data ingestion and quality checks operate at scale? | **Planned:** bounded crawl pipeline with throughput and error report. |
| Train embedding models | Do representations improve retrieval on held-out queries? | **Planned:** embedding-model evaluation with labeled query/document pairs. |
| High-performance vector databases | Can retrieval meet p95 latency and recall targets? | **Planned:** vector-index recall/latency benchmark. |
| Search serves developers and AI products | Can API behavior and evidence be explained to downstream teams? | **Planned:** documented retrieval contract and integration test. |
| Goal of high-quality search over broad information | Are coverage, trust, and usefulness measured together? | **Planned:** search quality scorecard with human judgments. |
| Cannot keep or refresh every crawled page | Does a finite index budget force a better selection rule? | **Built, synthetic:** [budgeted page selector](../projects/index-selection-eval/). |
| Cannot spend a GPU on every page | Can quality per unit compute be measured? | **Planned:** staged cheap/expensive model cascade and compute-cost report. |
| Decide pages worth indexing | Does a threshold preserve useful pages? | **Built, synthetic:** [index versus non-index decision](../projects/index-selection-eval/). |
| Decide links worth following | Does a frontier policy find valuable unseen information? | **Planned:** crawl-frontier prioritization replay. |
| Detect pages saying the same thing | Can near duplicates be removed without collapsing useful variants? | **Planned:** semantic-duplicate error benchmark. |
| Detect stale pages | Does freshness change a decision and retrieval outcome? | **Built, toy:** [freshness-aware selector](../projects/index-selection-eval/); real timestamps and update policy planned. |
| Identify pages that should never be indexed | Can unsafe, spam, or useless pages be rejected with false-positive accounting? | **Planned:** page-exclusion classifier and review queue. |
| Improve search by removing useless and adding missing pages | Does the selected set increase weighted query coverage? | **Built, synthetic:** [query-coverage comparison](../projects/index-selection-eval/); real outcomes planned. |
| Current decisions mix learned signals and hand-set thresholds | Can calibrated scores beat a threshold under an explicit budget? | **Built, partial method:** [classifier calibration exercise](../projects/classifier-evaluation/); integrated calibrated selector planned. |
| Own both signals and decisions | Is the whole data→score→action→outcome chain auditable? | **Built, small:** [selection/evaluation separation](../projects/index-selection-eval/); production audit trail planned. |
| No ground truth is given | Can a defensible label rubric and disagreement process be created? | **Planned:** page-value annotation guide and adjudication pilot. |
| Classifiers, rankers, calibration | Are probabilities and ordering evaluated separately? | **Built, supporting:** [classifier evaluation](../projects/classifier-evaluation/) and [search ranking evaluation](../projects/search-ranking-eval/); web-scale calibration planned. |
| Strong data instincts at web scale | Can sampling bias and long-tail failures be diagnosed? | **Planned:** crawl sample audit by language, source, and page type. |
| A signal only counts if a decision changes and search improves | Does the evaluator inspect downstream impact rather than signal AUC alone? | **Built, synthetic:** [two indexing policies and hidden outcomes](../projects/index-selection-eval/). |
| Crawling, indexing, retrieval teams consume the work | Are feature and decision contracts stable across stages? | **Planned:** cross-stage schema and failure-mode test. |
| Finding high-quality knowledge matters | Can credibility and retrieval quality be kept distinct? | **Planned:** provenance-aware source-quality rubric. |
| Make parsing work on broken pages and prove it | Does parsing recall improve on difficult HTML? | **Planned:** page extraction failure set and before/after benchmark. |
| Agree on what page quality means | Can ambiguous labels be made consistent enough to train? | **Planned:** rater guide, agreement statistic, and label revision log. |
| Credibility and misinformation | Can source claims be checked without conflating disagreement with falsehood? | **Planned:** claim/source evidence rubric and error audit. |
| Distinguish semantic duplicates from valuable differences | Can dedup preserve user-visible distinct information? | **Planned:** duplicate-pair dataset with asymmetric error costs. |
| Equal-opportunity statement and San Francisco location | Are application terms acceptable and qualifications accurate? | **Candidate decision:** user accepts US onsite work; employment and accommodation facts are not technical proof. |

The $250k target is within the listed range, not its floor. The published indexing fixture intentionally makes one policy better and is not evidence of live search lift. It also cannot prove the candidate has trained embeddings, operated web-scale systems, or owned an employer's search decisions.
