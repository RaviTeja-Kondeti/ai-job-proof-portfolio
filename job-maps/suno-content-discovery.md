# Suno — Senior/Staff Machine Learning Engineer, Content Discovery

[Employer posting](https://jobs.ashbyhq.com/suno/e94b6a03-6315-45c2-a439-51630af15f05) · Ashby last published: 2026-10-02 · San Francisco base: **$241,200–$382,935 per year** plus equity. The role overlaps ML, data science, ranking, and experimentation, but its core is **production recommendations**. The candidate's actual recommendation work, shipped 0→1 models, degree or equivalent experience, and eligibility to work in the US remain unverified.

Each candidate-facing signal below is read as a test. A **built** link is a narrow, synthetic method demonstration; a **planned** project is a gap. None of these projects proves past employment or production ownership.

| Posting line or signal | The test hidden in it | One small project / state |
|---|---|---|
| Music creation is for everyone | Does discovery work for new, sparse-history, and niche users? | **Built, synthetic:** [cold-start and niche-user slices](../projects/music-discovery-eval/); real-user fairness remains planned. |
| Casual creators and professional musicians both use the platform | Can quality be evaluated by creator/listener segment? | **Planned:** segment-specific discovery benchmark with agreed relevance criteria. |
| Fast growth and millions of users | Can recommendation serving scale without losing quality? | **Planned:** throughput/latency benchmark with an SLO and capacity model. |
| Small team, ambition, quality, ownership, intensity | Can one owner turn an unclear goal into a shipped, reviewed outcome? | **Planned:** end-to-end recommendation RFC, implementation, test, and retrospective. |
| Creative expression and love of music | Can discovery surface novelty without burying user taste? | **Built, narrow:** [genre diversity and relevance comparison](../projects/music-discovery-eval/); domain understanding and music-taste evidence need candidate examples. |
| Early member of recommendations team | Can the initial system be scoped and prioritized? | **Planned:** 0→1 recommendation architecture and 90-day rollout plan. |
| Work closely with founding team | Can model tradeoffs be explained to decision makers? | **Planned:** one-page ranking tradeoff decision memo. |
| Own technical decisions for models and deployment | Can the choice of baseline, model, feature, and release gate be defended? | **Planned:** model selection record with costs, failure modes, and rollback. |
| Formulate user preference mathematically | Does a user representation predict held-out interest? | **Built, toy:** [smoothed genre affinity](../projects/music-discovery-eval/); **planned:** trained preference model. |
| Model item similarity | Does a track embedding find related music and avoid trivial duplicates? | **Planned:** content/collaborative similarity benchmark. |
| Model engagement | Do click, listen, completion, and return signals align with satisfaction? | **Planned:** engagement-label and delayed-outcome study. |
| Sparse interaction data | Does the approach behave sensibly with little user history? | **Built, toy:** [sparse-history and cold-start cases](../projects/music-discovery-eval/). |
| Noisy interaction data | Can accidental listens and bots be handled? | **Planned:** feedback-noise stress test and robust estimator. |
| Evolving user taste | Can preference updates track drift without unstable recommendations? | **Planned:** time-decayed preference replay. |
| Build recommendation models | Can a learned model beat popularity on a frozen holdout? | **Planned:** trained collaborative/content ranker; [current heuristic](../projects/music-discovery-eval/) is not a learned model. |
| Deploy recommendation models | Is serving versioned, observable, and rollback-ready? | **Planned:** model-serving API with canary and rollback exercise; past production ownership requires candidate evidence. |
| Real-time latency constraints | Is p95 latency met under realistic traffic? | **Planned:** load test of candidate generation and ranking. |
| Throughput constraints | Does the system meet requests per second under load and backpressure? | **Planned:** throughput/cost benchmark. |
| Relevance as an objective | Does the ranker improve a defined held-out ranking measure? | **Built, synthetic:** [NDCG@3 comparison](../projects/music-discovery-eval/); not real lift. |
| Novelty as an objective | Does it expose unfamiliar but fitting tracks? | **Planned:** novelty metric and controlled tradeoff study. |
| Diversity as an objective | Can ranking avoid monotony without damaging relevance? | **Built, synthetic:** [genre-diversity metric](../projects/music-discovery-eval/). |
| Long-term satisfaction as an objective | Do users return and remain satisfied beyond one session? | **Planned:** delayed-outcome metric and retention experiment. |
| Translate objectives to optimized systems | Can competing metrics become an explicit release rule? | **Built, toy:** [offline gate](../projects/music-discovery-eval/); **planned:** constrained multi-objective optimization. |
| Large-scale experiments | Are randomization, sample-ratio, and guardrails sound? | **Built, synthetic method:** [experiment audit](../projects/experiment-audit/); real scale unverified. |
| Causal analyses | Is an effect attributable to the recommendation change? | **Built, small method:** [incrementality exercise](../projects/incrementality/); production experiment unverified. |
| Evaluate model behavior and product impact | Can offline wins be checked against online outcomes? | **Planned:** offline-to-online validation and launch memo. |
| Collaborate with product and research leaders | Can ambiguous personalization goals become an agreed technical direction? | **Planned:** stakeholder problem statement, metric contract, and design review. |
| Master's/PhD or equivalent practical experience | Is education or equivalent work documented? | **Candidate verification:** resume, degree, and actual work history. |
| Python proficiency | Can a reviewer run readable implementation and tests? | **Built, small:** [stdlib Python evaluator and tests](../projects/music-discovery-eval/). |
| Modern ML framework such as PyTorch | Can a model be trained and reproduced? | **Planned:** PyTorch ranker with frozen data and model card; framework history unverified. |
| Implement and iterate on research ideas | Does a hypothesis survive ablations and failure inspection? | **Planned:** research reproduction with ablation log. |
| Data pipelines and cloud such as Spark/AWS | Can events be processed without leakage or duplicates? | **Planned:** batch/stream feature pipeline with data-quality checks; cloud history unverified. |
| Build 0→1 production ML/DS systems | Is the candidate's real ownership and operation documented? | **Candidate verification:** shipped system, deployment, metrics, incident, and references. Synthetic proofs do not satisfy this line. |
| Cross-functional communication with Product, Data, and Infra | Can a tradeoff be explained and agreed across groups? | **Planned:** cross-functional review packet and decision log; real collaboration requires candidate examples. |
| Love of music is a plus | Can a domain insight change a measurable product decision? | **Planned:** music-discovery user journey and evaluation rubric. |
| Preferred 3+ years in recommendations/search/ads/optimization/RL | What directly relevant work was actually done and when? | **Candidate verification:** dated projects and responsibilities; [search method](../projects/search-ranking-eval/) and [optimization method](../projects/budget-allocation/) are supplementary only. |
| Publications at KDD/ICML/NeurIPS/RecSys/ACL or similar | Is original research publicly documented? | **Candidate verification:** publication links if any; no publication inferred. |
| Eligible to work in the US | Does candidate meet the employer's condition? | **Candidate verification:** private application fact; no portfolio project. |
| San Francisco location, benefits, equity, and equal-opportunity terms | Are the location and offer terms acceptable? | **Candidate decision:** user accepts onsite work; exact office schedule and offer details require recruiter confirmation. These are application facts, not technical proof. |

The Suno music rendition and investor list add company context, not a technical qualification. The range can exceed $250k, but it starts below that target. The synthetic evaluator was made for the posting and must not be described as professional recommendation experience.
