# AI job proof portfolio

This repository turns job-post statements into small, inspectable projects. It uses synthetic data so the code and results can be shared publicly. It does **not** claim that these simulations represent work performed for an employer.

## Current source and status

- [OpenAI — Machine Learning Engineer, Growth](https://openai.com/careers/machine-learning-engineer-growth-san-francisco/): [line-by-line evidence map](job-maps/openai-growth.md).
- [OpenAI — Machine Learning Engineer, Implicit Signals](https://jobs.ashbyhq.com/openai/a01fc9ed-de08-4326-9206-4ee3f08000dc): [line-by-line evidence map](job-maps/openai-implicit-signals.md).
- [Abridge — Software Engineer, Generative AI](https://jobs.ashbyhq.com/abridge/897709b2-e03d-4574-8611-5cfd669adde9): [line-by-line evidence map](job-maps/abridge-genai.md).
- [Anthropic — ML/Research Engineer, Safeguards](https://job-boards.greenhouse.io/anthropic/jobs/4949336008): [line-by-line evidence map](job-maps/anthropic-safeguards.md).
- [Firecrawl — Research Engineer, Benchmarks](https://jobs.ashbyhq.com/firecrawl/90f88e13-7d5f-43e2-a3fc-9e16d836b71c): [line-by-line evidence map](job-maps/firecrawl-benchmarks.md).
- [30-day, salary-filtered AI-first posting queue](job-maps/index.md).
- Built proof: [budget allocation](projects/budget-allocation/), [spend pacing](projects/spend-pacing/), [incrementality](projects/incrementality/), [LLM output evaluation](projects/llm-evaluation/), [prompt-injection screening](projects/prompt-injection-screen/), [provider benchmarks](projects/provider-benchmarks/), and [classifier evaluation](projects/classifier-evaluation/).
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
python3 projects/budget-allocation/allocate.py
python3 projects/spend-pacing/pacing.py
python3 projects/incrementality/experiment.py
python3 projects/llm-evaluation/evaluate.py
python3 projects/prompt-injection-screen/screen.py
python3 projects/provider-benchmarks/benchmark.py
python3 projects/classifier-evaluation/evaluate.py
```

Each project has its own assumptions, failure cases, and output. The job map links to the relevant proof. The repository is a portfolio demonstration, not a claim of production impact or employment history.
