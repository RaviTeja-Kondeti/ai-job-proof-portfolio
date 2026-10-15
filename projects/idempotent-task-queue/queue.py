"""A deterministic SQLite task queue with retry, lease fencing, and cost attribution."""

import json
import sqlite3


class TaskQueue:
    def __init__(self, max_inflight=2, max_attempts=3, lease_seconds=10):
        if min(max_inflight, max_attempts, lease_seconds) < 1:
            raise ValueError("Queue limits must be positive")
        self.db = sqlite3.connect(":memory:")
        self.db.row_factory = sqlite3.Row
        self.max_inflight = max_inflight
        self.max_attempts = max_attempts
        self.lease_seconds = lease_seconds
        self.db.executescript("""
            CREATE TABLE tasks (
                task_id TEXT PRIMARY KEY, payload TEXT NOT NULL,
                status TEXT NOT NULL, attempts INTEGER NOT NULL,
                created_at INTEGER NOT NULL, next_at INTEGER NOT NULL,
                lease_until INTEGER, result TEXT, last_error TEXT,
                tokens INTEGER NOT NULL DEFAULT 0,
                cost_microusd INTEGER NOT NULL DEFAULT 0
            );
            CREATE INDEX ready_tasks ON tasks(status, next_at, created_at);
        """)

    def enqueue(self, task_id, payload, now):
        if not task_id or not isinstance(task_id, str) or not isinstance(now, int):
            raise ValueError("Invalid task ID or time")
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        prior = self.db.execute("SELECT payload FROM tasks WHERE task_id=?", (task_id,)).fetchone()
        if prior:
            if prior["payload"] != encoded:
                raise ValueError("Idempotency key reused for different payload")
            return False
        self.db.execute("""INSERT INTO tasks
            (task_id,payload,status,attempts,created_at,next_at)
            VALUES (?,?,'queued',0,?,?)""", (task_id, encoded, now, now))
        self.db.commit()
        return True

    def claim(self, now):
        if not isinstance(now, int):
            raise ValueError("Time must be integer seconds")
        with self.db:
            self.db.execute("""UPDATE tasks SET status='dead', last_error='lease expired'
                WHERE status='running' AND lease_until<=? AND attempts>=?""",
                (now, self.max_attempts))
            running = self.db.execute("""SELECT COUNT(*) FROM tasks
                WHERE status='running' AND lease_until>?""", (now,)).fetchone()[0]
            if running >= self.max_inflight:
                return None
            row = self.db.execute("""SELECT task_id,payload,attempts FROM tasks
                WHERE ((status IN ('queued','retry') AND next_at<=?)
                   OR (status='running' AND lease_until<=?)) AND attempts<?
                ORDER BY created_at,task_id LIMIT 1""",
                (now, now, self.max_attempts)).fetchone()
            if not row:
                return None
            attempt = row["attempts"] + 1
            self.db.execute("""UPDATE tasks SET status='running',attempts=?,lease_until=?
                WHERE task_id=?""", (attempt, now+self.lease_seconds, row["task_id"]))
            return {"task_id": row["task_id"], "payload": json.loads(row["payload"]),
                    "attempt": attempt, "lease_until": now+self.lease_seconds}

    def _check_lease(self, task_id, attempt, now):
        row = self.db.execute("SELECT * FROM tasks WHERE task_id=?", (task_id,)).fetchone()
        if (not row or row["status"] != "running" or row["attempts"] != attempt
                or row["lease_until"] <= now):
            raise ValueError("Stale or invalid lease")
        return row

    def complete(self, task_id, attempt, result, tokens, price_microusd_per_token, now):
        if not all(isinstance(x, int) for x in (tokens, price_microusd_per_token, now)):
            raise ValueError("Tokens, price, and time must be integers")
        if min(tokens, price_microusd_per_token) < 0:
            raise ValueError("Tokens and price must be nonnegative")
        self._check_lease(task_id, attempt, now)
        with self.db:
            self.db.execute("""UPDATE tasks SET status='done', result=?,tokens=?,
                cost_microusd=?,lease_until=NULL WHERE task_id=?""",
                (json.dumps(result, sort_keys=True), tokens,
                 tokens*price_microusd_per_token, task_id))

    def fail(self, task_id, attempt, error, now):
        row = self._check_lease(task_id, attempt, now)
        if not error or not isinstance(error, str):
            raise ValueError("Failure reason is required")
        status = "dead" if row["attempts"] >= self.max_attempts else "retry"
        retry_at = now + min(2 ** (attempt-1), 32) if status == "retry" else now
        with self.db:
            self.db.execute("""UPDATE tasks SET status=?,next_at=?,lease_until=NULL,
                last_error=? WHERE task_id=?""", (status, retry_at, error, task_id))
        return {"status": status, "retry_at": retry_at if status == "retry" else None}

    def snapshot(self):
        counts = {row["status"]: row["n"] for row in self.db.execute(
            "SELECT status,COUNT(*) AS n FROM tasks GROUP BY status")}
        costs = self.db.execute("""SELECT COALESCE(SUM(tokens),0) AS tokens,
            COALESCE(SUM(cost_microusd),0) AS cost_microusd FROM tasks""").fetchone()
        return {"status_counts": counts, "tokens": costs["tokens"],
                "cost_microusd": costs["cost_microusd"]}


def demo():
    q = TaskQueue(max_inflight=1)
    log = []
    q.enqueue("extract-1", {"document": "synthetic-a"}, 0)
    q.enqueue("extract-1", {"document": "synthetic-a"}, 0)
    q.enqueue("extract-2", {"document": "synthetic-b"}, 0)
    first = q.claim(0)
    log.append({"claim": first})
    log.append({"backpressure": q.claim(0) is None})
    log.append({"failure": q.fail("extract-1", first["attempt"], "temporary dependency error", 1)})
    second = q.claim(1)
    q.complete("extract-2", second["attempt"], {"ok": True}, 12, 20, 2)
    retry = q.claim(2)
    q.complete("extract-1", retry["attempt"], {"ok": True}, 10, 20, 3)
    return {"events": log, "final": q.snapshot()}


if __name__ == "__main__":
    print(json.dumps(demo(), indent=2, sort_keys=True))
