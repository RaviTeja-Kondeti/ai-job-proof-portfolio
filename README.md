# AI job proof portfolio

This repository turns job-post statements into small, inspectable projects. It uses synthetic data so the code and results can be shared publicly. It does **not** claim that these simulations represent work performed for an employer.

## Current source and status

- [OpenAI — Machine Learning Engineer, Growth](https://openai.com/careers/machine-learning-engineer-growth-san-francisco/): [line-by-line evidence map](job-maps/openai-growth.md).
- [OpenAI — Machine Learning Engineer, Implicit Signals](https://jobs.ashbyhq.com/openai/a01fc9ed-de08-4326-9206-4ee3f08000dc): [line-by-line evidence map](job-maps/openai-implicit-signals.md).
- [OpenAI — Data Scientist, B2B Strategy & Intelligence](https://jobs.ashbyhq.com/openai/756d8c20-649a-47f2-8012-553b5f6cb0c5): [line-by-line evidence map](job-maps/openai-b2b-data-scientist.md).
- [Abridge — Software Engineer, Generative AI](https://jobs.ashbyhq.com/abridge/897709b2-e03d-4574-8611-5cfd669adde9): [line-by-line evidence map](job-maps/abridge-genai.md).
- [Anthropic — ML/Research Engineer, Safeguards](https://job-boards.greenhouse.io/anthropic/jobs/4949336008): [line-by-line evidence map](job-maps/anthropic-safeguards.md).
- [Firecrawl — Research Engineer, Benchmarks](https://jobs.ashbyhq.com/firecrawl/90f88e13-7d5f-43e2-a3fc-9e16d836b71c): [line-by-line evidence map](job-maps/firecrawl-benchmarks.md).
- [Firecrawl — Agent Experience Engineer](https://jobs.ashbyhq.com/firecrawl/a81209e5-5e75-4ac8-905a-0df49891d61b): [line-by-line evidence map](job-maps/firecrawl-agent-experience.md).
- [Glean — Senior/Staff Applied Scientist](https://job-boards.greenhouse.io/gleanwork/jobs/4740092005): [line-by-line evidence map](job-maps/glean-applied-scientist.md).
- [WRITER — AI Engineer](https://jobs.ashbyhq.com/writer/40f9e2b4-3284-4a20-b45d-0f5e5dd9108d): [line-by-line evidence map](job-maps/writer-ai-engineer.md).
- [Cohere — MTS, Post-Training Data Infrastructure](https://jobs.ashbyhq.com/cohere/eef82766-7e31-430f-a102-bc33a5022597): [line-by-line evidence map](job-maps/cohere-post-training-data.md).
- [SpaceXSI — MTS, Evaluation Infrastructure](https://job-boards.greenhouse.io/xai/jobs/5252714007): [line-by-line evidence map](job-maps/spacexsi-eval-infrastructure.md).
- [Replit — Data Scientist, Growth](https://jobs.ashbyhq.com/replit/1066b974-3cd8-42cf-a11c-a4217c06f70f): [line-by-line evidence map](job-maps/replit-growth-data-scientist.md).
- [30-day, salary-filtered AI-first posting queue](job-maps/index.md).
- [Eight-week proof plan](ROADMAP.md) for turning the highest-value gaps into linked evidence.
- [Audit of existing public GitHub work](EXISTING_WORK_AUDIT.md), with fixed-commit links and evidence limits.
- Built proof: [budget allocation](projects/budget-allocation/), [spend pacing](projects/spend-pacing/), [incrementality](projects/incrementality/), [experiment audit](projects/experiment-audit/), [growth backtesting](projects/growth-backtest/), [B2B metrics](projects/b2b-metrics-layer/), [LLM output evaluation](projects/llm-evaluation/), [agent trajectory evaluation](projects/agent-trajectory-eval/), [prompt-injection screening](projects/prompt-injection-screen/), [provider benchmarks](projects/provider-benchmarks/), [classifier evaluation](projects/classifier-evaluation/), and [post-training data checks](projects/post-training-data/).
- The map labels unbuilt projects as **planned**. A plan is never presented as a completed proof link.

## Reproduce the proof

Python 3.10+ and its standard library are sufficient:

```sh
python3 -m unittest discover -s projects/budget-allocation -p 'test_*.py'
python3 -m unittest discover -s projects/spend-pacing -p 'test_*.py'
python3 -m unittest discover -s projects/incrementality -p 'test_*.py'
python3 -m unittest discover -s projects/llm-evaluation -p 'test_*.py'
python3 -m unittest discover -s projects/prompt-injection-screen -p 'test_*.py'
python3 -m unittest discover -s projects/provider-benchmarks -p 'test_*.py'
python3 -m unittest discover -s projects/classifier-evaluation -p 'test_*.py'
python3 -m unittest discover -s projects/post-training-data -p 'test_*.py'
python3 -m unittest discover -s projects/growth-backtest -p 'test_*.py'
python3 -m unittest discover -s projects/experiment-audit -p 'test_*.py'
python3 -m unittest discover -s projects/b2b-metrics-layer -p 'test_*.py'
python3 -m unittest discover -s projects/agent-trajectory-eval -p 'test_*.py'
python3 projects/budget-allocation/allocate.py
python3 projects/spend-pacing/pacing.py
python3 projects/incrementality/experiment.py
python3 projects/llm-evaluation/evaluate.py
python3 projects/prompt-injection-screen/screen.py
python3 projects/provider-benchmarks/benchmark.py
python3 projects/classifier-evaluation/evaluate.py
python3 projects/post-training-data/build_dataset.py
python3 projects/growth-backtest/backtest.py
python3 projects/experiment-audit/audit.py
python3 projects/b2b-metrics-layer/metrics.py
python3 projects/agent-trajectory-eval/evaluate.py
```

Each project has its own assumptions, failure cases, and output. The job map links to the relevant proof. The repository is a portfolio demonstration, not a claim of production impact or employment history.
