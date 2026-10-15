# Project 13: growth decision service reference

**Job-post test:** Can an allocation policy become a callable, auditable service that respects consent and caps, handles stale feedback safely, and records policy version and idempotent decisions?

`python3 -m unittest test_engine.py` exercises the pure decision engine and HTTP handler without opening a socket. `python3 engine.py` starts a local HTTP service with `GET /health`, `GET /metrics`, and `POST /decide` in an environment that permits local listening. The deterministic policy allocates a toy integer budget between search and social, leaves unallocatable spend unspent, and falls back to equal priority when feedback is more than 24 hours old.

This is an **in-memory reference implementation**, not a deployed or production-ready ad-spend service. It lacks authentication, persistent idempotency, real marginal-return models, telemetry pipelines, consent provenance, concurrency control for budget commitments, audit retention, and a rollout/rollback system. No real marketing budget or user data is involved.
