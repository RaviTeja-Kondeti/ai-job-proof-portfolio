# Proof-link coverage for current role maps

This inventory checks **only whether a mapped test row links to an inspectable project or the candidate's existing public GitHub work**. One artifact may support several rows; this audit does not prove that every line has its own distinct project. A link can be partial, synthetic, inconclusive, or irrelevant to a production qualification; it does not establish that the test has been passed. The tool also cannot verify that every sentence of the live posting was mapped. [The role queue](job-maps/index.md) defines which maps are current for this audit.

Salary/date-screened role rows: **36**. Roles with a line map: **17**. Roles without a line map: **19**. Current mapped roles audited here: **17**.

Mapped test rows: **546**. Rows with an artifact link: **133**. Rows without one: **413**. Rows explicitly requiring candidate-supplied history or credentials: **38** (may overlap either link category).

| Current role map | Test rows | With artifact link | Without artifact link | Candidate verification rows |
|---|---:|---:|---:|---:|
| [cartesia-data-infrastructure](job-maps/cartesia-data-infrastructure.md) | 33 | 4 | 29 | 2 |
| [cohere-post-training-data](job-maps/cohere-post-training-data.md) | 23 | 7 | 16 | 2 |
| [exa-content-understanding](job-maps/exa-content-understanding.md) | 35 | 2 | 33 | 1 |
| [exa-index-intelligence](job-maps/exa-index-intelligence.md) | 27 | 9 | 18 | 0 |
| [firecrawl-agent-experience](job-maps/firecrawl-agent-experience.md) | 33 | 4 | 29 | 2 |
| [firecrawl-benchmarks](job-maps/firecrawl-benchmarks.md) | 43 | 9 | 34 | 1 |
| [glean-applied-scientist](job-maps/glean-applied-scientist.md) | 29 | 12 | 17 | 2 |
| [glean-search-quality](job-maps/glean-search-quality.md) | 28 | 7 | 21 | 4 |
| [luma-inference](job-maps/luma-inference.md) | 25 | 2 | 23 | 3 |
| [openai-b2b-data-scientist](job-maps/openai-b2b-data-scientist.md) | 33 | 4 | 29 | 4 |
| [openai-growth](job-maps/openai-growth.md) | 36 | 19 | 17 | 1 |
| [openai-implicit-signals](job-maps/openai-implicit-signals.md) | 38 | 7 | 31 | 0 |
| [openrouter-trust-safety](job-maps/openrouter-trust-safety.md) | 44 | 15 | 29 | 2 |
| [replit-growth-data-scientist](job-maps/replit-growth-data-scientist.md) | 37 | 9 | 28 | 6 |
| [spacexsi-eval-infrastructure](job-maps/spacexsi-eval-infrastructure.md) | 19 | 3 | 16 | 2 |
| [suno-content-discovery](job-maps/suno-content-discovery.md) | 39 | 12 | 27 | 5 |
| [writer-ai-engineer](job-maps/writer-ai-engineer.md) | 24 | 8 | 16 | 1 |

Run `python3 tools/audit_proof_links.py --gaps` for every current row without a linked artifact; use `--unmapped-roles` for salary/date-screened roles without a map. Run `python3 tools/audit_proof_links.py --markdown` to regenerate this table. Update maps only after inspecting and testing the linked work; an existing artifact is not automatically proof of the exact posting line.

