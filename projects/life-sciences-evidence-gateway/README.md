# Life-sciences evidence gateway

**Posting test:** [Anthropic's Applied AI Engineer, Beneficial Deployments (Life Sciences) role](https://job-boards.greenhouse.io/anthropic/jobs/5437172008) asks for reusable scientific-data tools, benchmarks, auditability, and partner documentation. This project demonstrates a narrow literature lookup with visible citations and abstention. It does **not** establish deep biomedical research, molecular design, clinical validity, an MCP server, or production deployment.

From the repository root, with Python 3.10+:

```sh
python3 -m unittest discover -s projects/life-sciences-evidence-gateway -p 'test_*.py' -v
python3 projects/life-sciences-evidence-gateway/gateway.py
```

The [record cards](records.json) paraphrase metadata and selected findings from three primary research sources indexed by PubMed: [AlphaFold method validation, PMID 34265844](https://pubmed.ncbi.nlm.nih.gov/34265844/), [human proteome application, PMID 34293799](https://pubmed.ncbi.nlm.nih.gov/34293799/), and [AlphaFold Protein Structure Database, PMID 34791371](https://pubmed.ncbi.nlm.nih.gov/34791371/). The source URL must match each PMID. The code does not fetch fresh literature or reproduce the studies.

[gateway.py](gateway.py) ranks a query against the local title and indexed terms. It returns a source-linked card only when at least two terms match and the best record has a unique lead; otherwise it abstains. It never synthesizes a biomedical recommendation. The [five-case benchmark](cases.json) has three known-source questions, one ambiguous question, and one unsupported treatment question. The checked-in [result](results.json) gets five of five on **these hand-written cases only**; this is not an accuracy estimate for scientific questions in general. Tests cover source attribution, malformed citations, duplicate PMIDs, and abstention.

To make this useful to a research partner, the next steps would be to ingest a versioned corpus from a documented source API, retain source snapshots, have domain experts verify claim cards and question labels, add contradiction and retraction handling, evaluate across institutions and scientific tasks, and expose a permissioned tool interface. A scientist would still need to review conclusions drawn from the papers.
