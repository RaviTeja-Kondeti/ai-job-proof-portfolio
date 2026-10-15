# Glean — Machine Learning Engineer, Search Quality

[Employer posting](https://job-boards.greenhouse.io/gleanwork/jobs/4738120005) · Greenhouse first published: 2026-09-25 · SF base: $140k–$265k. The role requires 2+ years and search, recommendation, NLP, or another large ML system. The upper **$15k** of its listed band exceeds the user's $250k base target.

Each distinct candidate-evaluating line, including the company description, working style, and AI interview exercise, is turned into a test and one proof project. **Built** links show narrow synthetic evidence; **planned** rows remain gaps. Production model deployment must be verified from real history.

| Posting signal | Test | One project / state |
|---|---|---|
| Work AI spans enterprise search, assistant, and agents | Can a relevance signal help multiple product surfaces? | **Planned:** shared retrieval evaluation across search and assistant. |
| Connectors, model choice, APIs, secure open platform | Can results remain correct across data sources and models? | **Planned:** connector/model portability test. |
| Enterprise and personal graphs tailor context | Can personalization improve ranking without exposing private items? | **Built, method only:** [permission-gated ranking comparison](../projects/search-ranking-eval/); graph features remain planned. |
| Use structured/unstructured, historical/current data | Is retrieval freshness and source provenance visible? | **Planned:** time-aware multi-source ranking test. |
| Faster onboarding, productivity, safer decisions | Are search improvements tied to user outcomes and trust? | **Planned:** task-time and safety metric tree. |
| Enterprise integrations used every day | Does quality survive realistic workflows? | **Planned:** cross-application search journey test. |
| Query understanding | Can ambiguous intent be classified and evaluated? | **Built, supporting method:** [classifier evaluation gate](../projects/classifier-evaluation/); query model remains planned. |
| Document understanding | Can content be represented with citations and permissions? | **Planned:** document relevance and access-control dataset. |
| Domain-adapted language models | Does adapting to customer corpus improve held-out tasks? | **Planned:** domain adaptation experiment. |
| Natural-language QA | Are answers grounded in retrieved evidence? | **Built, toy:** [grounding evaluation](../projects/llm-evaluation/); search integration remains planned. |
| Evaluation and experimentation across stack | Do offline ranking wins survive online testing? | **Built, partial methods:** [ranking evaluation](../projects/search-ranking-eval/) and [experiment audit](../projects/experiment-audit/); online lift remains planned. |
| Work directly with customers and pain points | Can a real customer issue shape the metric? | **Candidate verification:** actual customer examples; **planned:** interview-to-eval case. |
| Use simple or complex tools as needed | Is complexity justified by measured gain? | **Planned:** simple-ranker versus learned-ranker comparison. |
| Invent signals for personalization | Can a new user/document feature improve permitted relevance? | **Planned:** feature ablation on held-out queries. |
| Train signal-interaction ranking model | Does a learned ranker beat an explainable baseline? | **Planned:** learning-to-rank model with ablations. |
| Smarter customer-corpus adaptation | Can a model transfer without memorizing sensitive content? | **Planned:** retrieval/domain-adaptation contamination study. |
| Combine LLMs with search for complex questions | Do retrieval and generation succeed jointly? | **Planned:** RAG answer benchmark with attribution. |
| Robust readable maintainable tested code | Can a reviewer run meaningful failure tests? | **Built, small:** [ranking evaluator and tests](../projects/search-ranking-eval/); production code remains unverified. |
| Mentor or learn from experienced peers | Can design feedback change an implementation? | **Planned:** design review and revision record; real mentoring history requires candidate evidence. |
| Two-plus years of relevant experience | Are dates and responsibilities verifiable? | **Candidate verification:** actual resume; candidate reported about five years overall. |
| BA/BS in relevant field or related degree | Is education documented? | **Candidate verification:** degree not supplied. |
| Search, recommendations, NLP, or large ML systems | Which actual systems have been built? | **Existing supporting work:** [sentiment/NLP notebook](https://github.com/RaviTeja-Kondeti/LLM-Sentiment-Analysis/tree/8367c5514182515479908f641c5b1d3907684b29) and [ranking method](../projects/search-ranking-eval/); see [reproducibility limits](../EXISTING_WORK_AUDIT.md). |
| Analytical data skills | Can ranking errors be examined by slice? | **Built, synthetic:** [slice-level ranking report](../projects/search-ranking-eval/). |
| Ship production-ready models | Is serving, monitoring, and rollback actually evidenced? | **Candidate verification:** real deployed model; synthetic ranking code is insufficient. |
| ML framework proficiency and strong coding | Can training and inference run reproducibly? | **Planned:** trained ranker and serving reference; framework experience unverified. |
| Customer-focused cross-functional work | Can quality tradeoffs be explained to product and engineering? | **Planned:** search release decision memo. |
| Proactive ownership and troubleshooting | Can a regression be found and corrected end to end? | **Planned:** search-quality incident reconstruction. |
| AI fluency interview exercise/discussion | Can AI use be demonstrated with validation? | **Planned:** AI-assisted development walkthrough using commits and tests. |

The posting says four days in the SF office, while an application-form sentence references Palo Alto on Monday/Wednesday/Friday; clarify the requisition's actual schedule. Benefits, privacy/arbitration terms, and voluntary demographics are application decisions, not technical accomplishments. The salary target is possible only at the very top of the listed range.
