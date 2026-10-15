"""Run a small, grain-safe B2B metrics model against synthetic data."""

import json
from pathlib import Path
import sqlite3

ROOT = Path(__file__).parent


def database() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript((ROOT / "schema_and_data.sql").read_text())
    return conn


def account_metrics(conn: sqlite3.Connection) -> list[dict]:
    rows = [dict(row) for row in conn.execute((ROOT / "account_metrics.sql").read_text())]
    if len(rows) != conn.execute("SELECT COUNT(*) FROM accounts").fetchone()[0]:
        raise ValueError("Account grain violated")
    return rows


if __name__ == "__main__":
    with database() as conn:
        print(json.dumps(account_metrics(conn), indent=2))
