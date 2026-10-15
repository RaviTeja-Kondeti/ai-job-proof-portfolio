# Firecrawl — Research Engineer, Benchmarks

[Live posting](https://jobs.ashbyhq.com/firecrawl/90f88e13-7d5f-43e2-a3fc-9e16d836b71c) · Ashby last published: 2026-09-29 · SF base: $250k–$290k · 4+ years relevant experience and benchmark/evaluation work already shipped.

Each distinct candidate-facing statement is paraphrased below as a test and a small project. **Built** means a runnable link exists. **Planned** is a gap. A synthetic demo does not prove real vendor performance, employment history, or a shipped public benchmark.

| Posting signal | Test | One proof project |
|---|---|---|
| Independent comparison of company-data providers | Are outcomes independent of vendors' claims? | **Built, toy:** [company-domain comparison](../projects/provider-benchmarks/). |
| Independent comparison of person-data providers | Can you identify a person's current employer and title? | **Planned:** dated person-identity benchmark with ambiguity labels. |
| Independent comparison of fresh job providers | Can you measure relevance, recency, and duplicates? | **Planned:** job-feed benchmark with freshness and duplicate scoring. |
| Cover Alexandria's providers and the wider market | Are inclusion rules fair and public? | **Planned:** provider inclusion protocol and coverage registry. |
| Automated public weekly publication | Can a stranger reproduce one release? | **Planned:** weekly pipeline with frozen inputs, commit, manifest, and downloadable results. |
| Benchmarks inform Alexandria's provider choice | Does evaluation change a decision safely? | **Built, toy:** [domain selection rule](../projects/provider-benchmarks/benchmark.py); **planned:** shadow router with rollback. |
| Results must withstand vendor challenges | Can errors be disputed and corrected? | **Planned:** challenge log, adjudication policy, correction protocol. |
| Own methodology without a prescribed design | Can you defend metrics chosen before seeing results? | **Planned:** preregistered benchmark design and adversarial review. |
| Own datasets and ground truth | Are examples sampled, labeled, dated, and traceable? | **Built, toy only:** [nine synthetic tasks](../projects/provider-benchmarks/synthetic_tasks.json); **planned:** versioned labeled sample. |
| Own scoring and harness | Does one system apply identical rules to all providers? | **Built, toy scorer:** [code and tests](../projects/provider-benchmarks/); **planned:** API adapter contract. |
| Web pages become clean structured data for AI agents | Is extraction correct, not just parseable? | **Planned:** web-to-structured-data fidelity evaluation. |
| Build a large knowledge repository | Can entities be refreshed, deduplicated, and traced to sources? | **Planned:** incrementally updated entity graph with provenance. |
| Small team, end-to-end ownership | Can one person ship and operate a product slice? | **Planned:** hosted benchmark page, runbook, monitoring, and incident review. |
| Rapid, deep work on agent data infrastructure | Can scope be cut without weakening validity? | **Planned:** one-week release log with decisions and failure analysis. |
| Company details: named-vendor comparison | Is entity matching and attribute accuracy measured? | **Planned:** company-record benchmark with attribute-level scoring. |
| Current person, employer, and title: named-vendor comparison | Is temporal truth and identity ambiguity addressed? | **Planned:** current-title benchmark with dated references. |
| Fresh, relevant, nonduplicate jobs: named-vendor comparison | Are duplicate and stale results penalized? | **Planned:** job-search precision, freshness, and duplicate study. |
| Keep test sets and truth from staling or leaking | Can you detect expired labels and contamination? | **Planned:** label expiry, held-out canaries, and access audit. |
| Reproducible, versioned, defensible runs | Can an external reviewer replay one score? | **Planned:** pinned-input replay command and signed release manifest. |
| Accuracy | Is correctness measured for each field and task? | **Built, toy exact match:** [scorer](../projects/provider-benchmarks/benchmark.py); **planned:** error taxonomy. |
| Coverage | Are missing results counted? | **Built, toy:** [coverage metric](../projects/provider-benchmarks/benchmark.py); **planned:** error/abstention taxonomy. |
| Freshness | Is data correct when used? | **Planned:** timestamp and recheck study across time windows. |
| Speed | Are latency distributions and timeouts measured? | **Built, toy p95:** [scorer](../projects/provider-benchmarks/benchmark.py); **planned:** live API timing. |
| Cost | Is cost per verified answer clear? | **Built, toy mean cost:** [scorer](../projects/provider-benchmarks/benchmark.py); **planned:** real pricing analysis. |
| Public leaderboard with marketing | Can nontechnical readers inspect methods and caveats? | **Planned:** accessible leaderboard with sample sizes and downloadable rows. |
| Expand benchmark categories | Are adapters reusable without changing fairness rules? | **Planned:** plugin specification plus an additional domain. |
| Already shipped credible evals or benchmarks | Is a prior public release and validity argument available? | **Gap requiring real history:** toy prototype cannot satisfy this; candidate must supply actual work or publish a genuine release. |
| Relevant lab, data-company, benchmark, or OSS experience | Is the work context independently verifiable? | **Candidate verification:** link actual employment or accepted OSS contributions; do not invent affiliation. |
| Python strength | Is code readable, runnable, and tested? | **Built, basic:** [Python benchmark](../projects/provider-benchmarks/). |
| APIs, rate limits, and inconsistent schemas | Does the harness survive messy vendors? | **Planned:** mock adapters with 429, timeout, malformed schema, and retry tests. |
| Sampling, labeling, inter-rater agreement | Is annotation quality quantified? | **Planned:** stratified sampler, label guide, double-label agreement report. |
| Appropriate use of LLM judges | Are disputed/high-stakes labels human-adjudicated? | **Planned:** blinded judge-versus-human agreement study. |
| Heavy practical AI tool use | Can workflow gains be shown with error checks? | **Planned:** AI-assisted build log with accepted/rejected suggestions and results. |
| Ships without detailed instructions | Can ambiguity become a scoped release? | **Planned:** independent one-week benchmark from question to release. |
| Clear writing for engineers, marketers, and losing vendors | Can one dataset support three honest explanations? | **Planned:** methods report, buyer summary, and dispute response. |
| No convenient metric selection | Were metrics and exclusions fixed before outcomes? | **Planned:** preregistration, sensitivity analysis, all-runs disclosure. |
| Research judgment plus working engineering | Does a defensible method actually run on schedule? | **Planned:** complete release with executable harness and review memo. |
| Urgent pace and ownership | Is there dated evidence of reliable iteration? | **Planned:** weekly release history including defects and corrections. |
| Application asks for work and why it was right | Is there one inspectable artifact and validity case? | **Planned:** application dossier linking a genuine release and failure analysis. |
| Technical chat: current-title benchmark | Can ground truth be defended to a losing vendor? | **Planned:** worked design memo and challenge drill. |
| Workflow chat: AI tools and faster shipping | Can a real workflow improvement be shown? | **Planned:** walkthrough based on this repository's commit history. |
| Founder chat: culture, pace, ownership | Can the candidate explain actual fit? | **Candidate reflection:** honest personal decision memo. |
| Paid work trial: real provider category | Can a real benchmark ship in about 40 hours? | **Planned:** trial-sized playbook; a real trial requires employer invitation. |

## Posting facts to verify

- The posting conflicts on SF schedule: one section says hybrid with at least three onsite days; another says five onsite days. Confirm with Firecrawl.
- Work authorization and any sponsorship need factual answers. The posting lists supported visas/transfers and limits new H-1B sponsorship for candidates outside the US.
- Salary, equity, benefits, and interview stages are application terms, not candidate proof.
- Funding, growth, popularity, and product scale are employer claims that explain the environment; this repository has not audited them.

## Highest-value next release

Publish a dated benchmark for one real provider category with independently verifiable ground truth, a frozen sample, deterministic scoring, uncertainty intervals, documented API failures, and a vendor challenge process. That would address the role's central test much better than more synthetic tasks.
