# Exa — Research Engineer, Content Understanding

[Employer posting](https://jobs.ashbyhq.com/exa/508f3b2e-980b-41e9-ae02-26c72ce6b775) · Ashby last published: 2026-10-01 · San Francisco annual base: **$180k–$350k**. The work asks for document understanding and supervision at web scale. The posting specifically asks for transformer implementation and efficient trained models; neither is proven by the candidate's stated general ML/LLM strengths.

Every substantive statement in the company description, role, desired experience, and example projects is read as a test. Each row specifies one small proof project. **Built** means a narrow existing method, **planned** means no proof link yet, and actual production experience needs candidate evidence.

| Posting signal | Test | One small project / state |
|---|---|---|
| Applied AI lab building broad search | Can a page-level model improve search results? | **Built, synthetic downstream method:** [index decision to query coverage](../projects/index-selection-eval/); live retrieval impact planned. |
| Crawl the web | Can extraction handle varied real-world HTML reliably? | **Planned:** page extraction corpus and error benchmark. |
| Train state-of-the-art embeddings | Do representations improve retrieval across page types? | **Planned:** query-document embedding evaluation. |
| Use high-performance vector retrieval | Can quality be maintained at bounded latency? | **Planned:** vector recall/p95 benchmark. |
| Search supports developers and AI products | Are API evidence and failures useful to downstream consumers? | **Planned:** retrieval quality contract and client test. |
| Goal is high-quality knowledge access | Can quality, credibility, and relevance be measured separately? | **Planned:** multi-axis search judgment rubric. |
| Search quality depends on understanding each page | Can page predictions be traced to retrieval failure? | **Planned:** page-to-search error attribution. |
| Separate content from page furniture | Is extracted main text accurate on difficult layouts? | **Planned:** content extraction benchmark with annotated regions. |
| Classify page kind | Does a page-type classifier work on long-tail formats? | **Built, supporting method:** [classifier evaluation and slices](../projects/classifier-evaluation/); page model planned. |
| Classify page topic | Are multi-label topics calibrated and useful downstream? | **Planned:** page-topic label set and evaluation. |
| Determine whether a page is usable | Can broken/empty/blocked pages be rejected with false-positive costs? | **Planned:** usability classifier and review set. |
| Extract publication time | Can date extraction distinguish publish, update, and crawl times? | **Planned:** publication-date extraction benchmark. |
| Judge page quality | Can raters agree on a supervision target? | **Planned:** quality rubric and agreement pilot. |
| Judge source trust | Can claim, source, and evidence be evaluated without overclaiming certainty? | **Planned:** source/claim evidence audit. |
| Detect genuinely new information versus duplicates | Can semantic dedup retain useful differences? | **Planned:** near-duplicate pair benchmark. |
| Work in every language and page shape | Does quality degrade on multilingual or unusual layouts? | **Planned:** language/layout stress set with slice metrics. |
| Credibility and misinformation remain open | Can uncertainty and rater disagreement be surfaced? | **Planned:** uncertainty-aware credibility labels. |
| AI-generated or machine-spun content | Can manipulation be detected without penalizing legitimate AI-assisted writing? | **Planned:** synthetic-text detection failure audit. |
| Pages optimized for crawlers rather than readers | Can search spam be recognized with counterexamples? | **Planned:** SEO-spam evaluation set. |
| Search trust depends on page judgments | Does improving a page model change user-visible trust? | **Planned:** page-model-to-result audit with blinded judgments. |
| Graduate-level ML or exceptional undergraduate record | Is education and relevant work verifiable? | **Candidate verification:** degree and dated projects; no credential inferred. |
| Build a transformer from scratch in PyTorch | Can architecture, training, and correctness be demonstrated? | **Planned:** minimal Transformer implementation and unit/learning tests; actual experience unverified. |
| Train models cheap enough for web-scale use | Do accuracy, throughput, and cost meet an explicit budget? | **Planned:** small/large model cascade with p95 and dollar-cost estimate. |
| Build large-scale datasets and live in the data | Is supervision quality and sampling bias examined before architecture changes? | **Planned:** web-page data profile and label-error study. |
| Supervision may matter more than architecture | Does label improvement beat model complexity in an ablation? | **Planned:** annotation-versus-model ablation. |
| Define ground truth where none exists | Can ambiguous quality be made learnable? | **Planned:** label-guide pilot with disagreement and revision. |
| Care about high-quality knowledge | Can design choices reduce false confidence in bad sources? | **Planned:** trustworthy-search failure taxonomy. |
| Fix parsing and prove the improvement | Is the before/after test frozen and representative? | **Planned:** difficult-HTML parser regression. |
| Teach a model page quality | Do labels and a held-out model agree with a human rubric? | **Planned:** quality model and rater agreement report. |
| Model credibility and misinformation | Are claims linked to evidence rather than source popularity alone? | **Planned:** claim/evidence pair classifier. |
| Distinguish semantic sameness from valuable differences | Are false merges and missed duplicates reported separately? | **Planned:** asymmetric duplicate-cost benchmark. |
| Classify/extract accurately and cheaply at web scale | What is quality per million pages and p95 inference time? | **Planned:** batch inference cost/quality benchmark. |
| Design supervision with no existing labels | Does a small label pilot show learnability before large spend? | **Planned:** active-labeling learning curve. |
| Trace bad results to page predictions and fix the source | Can an incident be reconstructed end to end? | **Planned:** retrieval failure reconstruction and correction log. |
| EEO statement and SF location | Are terms acceptable and application claims accurate? | **Candidate decision:** user accepts US onsite work; EEO terms are application facts. |

The employer's investors and current customers establish context and scale, not a personal qualification. The upper portion of the salary range passes $250k; reaching it is uncertain. Current linked work is only partial method evidence and does not prove transformer training or large-scale search deployment.
