# Idempotent Applied AI task queue

**Posting test:** [Mercor's Software Engineer, Systems & Platform Applied AI role](https://jobs.ashbyhq.com/mercor/374cd009-516f-4a1f-abbf-bcca5287daae) asks for queued data and job pipelines, idempotency, retries, backpressure, recovery, and token/cost attribution. This is a small local demonstration of those ideas, not production service or evidence of backend employment.

From the repository root, with Python 3.10+:

```sh
python3 -m unittest discover -s projects/idempotent-task-queue -p 'test_*.py' -v
python3 projects/idempotent-task-queue/queue.py
```

[queue.py](queue.py) stores synthetic tasks in SQLite. A repeated task ID with the same payload does not duplicate work; a changed payload under that ID fails. `claim()` limits active leases, provides retry eligibility after bounded exponential delays, reclaims expired leases, and dead-letters exhausted tasks. Completion uses the attempt number as a fencing token, so an old worker cannot commit after a new claim. Tokens and per-token micro-USD cost are charged only on successful completion. [tests](test_queue.py) cover those boundaries, including double-charge prevention. The deterministic [result](results.json) ends with two completed tasks, 22 tokens, and 440 micro-USD at a synthetic price of 20 micro-USD per token.

**Limits:** The database is in memory and uses one connection. It does not prove multi-process concurrency, real durability, throughput at scale, container orchestration, tracing, alerting, production on-call work, or user-visible reliability. The sample prices and jobs are invented. A deployed version would need persistent storage, transactional claiming across workers, lease heartbeats, dead-letter review, metrics and alert thresholds, load tests, and failure-injection against real dependencies.
