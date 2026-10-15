"""Run a consent-scoped, maturity-aware synthetic growth funnel in SQLite."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

SQL = Path(__file__).with_name("funnel.sql").read_text()
USER_FIELDS = frozenset({"user_id", "segment", "market"})
EVENT_FIELDS = frozenset({"event_id", "user_id", "event_name", "event_at",
                          "received_at", "consent"})
EVENT_NAMES = frozenset({"signup", "core_action", "upgrade"})


def utc_time(value: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError("Timestamp must be a string")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("Timestamp must have a timezone")
    return parsed.astimezone(timezone.utc)


def utc_text(value: str) -> str:
    return utc_time(value).isoformat(timespec="microseconds").replace("+00:00", "Z")


def validate(users: list[dict], events: list[dict]) -> None:
    if not users or not events:
        raise ValueError("Users and events are required")
    ids = set()
    for user in users:
        if set(user) != USER_FIELDS or not isinstance(user["user_id"], str):
            raise ValueError("Invalid user schema")
        if not user["user_id"] or user["user_id"] in ids:
            raise ValueError("Invalid or duplicate user ID")
        ids.add(user["user_id"])
        if user["segment"] not in {"consumer", "business"} or not user["market"]:
            raise ValueError("Invalid segment or market")
    versions = {}
    for event in events:
        if set(event) != EVENT_FIELDS or event["user_id"] not in ids:
            raise ValueError("Invalid event schema or orphan")
        if (not isinstance(event["event_id"], str) or not event["event_id"]
                or event["event_name"] not in EVENT_NAMES
                or not isinstance(event["consent"], bool)):
            raise ValueError("Invalid event fields")
        identity = (event["user_id"], event["event_name"])
        receipt = utc_text(event["received_at"])
        if event["event_id"] in versions:
            previous_identity, receipts = versions[event["event_id"]]
            if identity != previous_identity or receipt in receipts:
                raise ValueError("Conflicting event versions or receipt-time tie")
            receipts.add(receipt)
        else:
            versions[event["event_id"]] = (identity, {receipt})
        if utc_time(event["received_at"]) < utc_time(event["event_at"]):
            raise ValueError("Receipt cannot precede event time")


def run(users: list[dict], events: list[dict], as_of: str) -> dict:
    validate(users, events)
    cutoff = utc_text(as_of)
    normalized_events = [
        {**event, "event_at": utc_text(event["event_at"]),
         "received_at": utc_text(event["received_at"])}
        for event in events
    ]
    with sqlite3.connect(":memory:") as db:
        db.row_factory = sqlite3.Row
        db.executescript("""
            CREATE TABLE users (user_id TEXT PRIMARY KEY, segment TEXT, market TEXT);
            CREATE TABLE events (
                event_id TEXT, user_id TEXT, event_name TEXT,
                event_at TEXT, received_at TEXT, consent INTEGER
            );
        """)
        db.executemany("INSERT INTO users VALUES (:user_id, :segment, :market)", users)
        db.executemany("""INSERT INTO events VALUES
            (:event_id, :user_id, :event_name, :event_at, :received_at, :consent)""", normalized_events)
        rows = [dict(row) for row in db.execute(SQL, {"as_of": cutoff})]
    return {
        "as_of": as_of,
        "definitions": {
            "acquired": "first consented signup per user",
            "activated": "consented core action within days 0-7 after signup",
            "retention_eligible": "activated user whose signup is at least 60 days old",
            "retained": "eligible user with consented core action in days 30-59",
            "expanded": "activated user with consented upgrade after activation, within 90 days",
            "deduplication": "latest received version of each event ID; exclude it if that version lacks consent",
            "as_of_rule": "both event time and receipt time must be no later than as_of",
        },
        "input_audit": {"users": len(users), "events": len(events),
                        "events_without_analytics_consent": sum(not e["consent"] for e in events)},
        "cohorts": rows,
    }


def fixture() -> tuple[list[dict], list[dict]]:
    users = [
        {"user_id": "u1", "segment": "consumer", "market": "US"},
        {"user_id": "u2", "segment": "consumer", "market": "US"},
        {"user_id": "u3", "segment": "business", "market": "US"},
        {"user_id": "u4", "segment": "consumer", "market": "UK"},
        {"user_id": "u5", "segment": "business", "market": "UK"},
        {"user_id": "u6", "segment": "consumer", "market": "US"},
        {"user_id": "u7", "segment": "business", "market": "US"},
    ]
    events = []

    def add(event_id: str, user_id: str, name: str, day: str,
            received: str | None = None, consent: bool = True) -> None:
        events.append({"event_id": event_id, "user_id": user_id,
                       "event_name": name, "event_at": day + "T00:00:00Z",
                       "received_at": (received or day) + "T12:00:00Z",
                       "consent": consent})

    add("s1", "u1", "signup", "2026-01-01")
    add("a1", "u1", "core_action", "2026-01-02")
    add("r1", "u1", "core_action", "2026-02-05")
    add("x1", "u1", "upgrade", "2026-01-20")
    add("s2", "u2", "signup", "2026-01-05")
    add("a2", "u2", "core_action", "2026-01-06", "2026-01-06")  # corrected below
    add("a2", "u2", "core_action", "2026-01-15", "2026-01-16")
    add("r2", "u2", "core_action", "2026-02-10")
    add("s3", "u3", "signup", "2026-01-03")
    add("a3", "u3", "core_action", "2026-01-04")
    add("r3", "u3", "core_action", "2026-02-08")
    add("x3", "u3", "upgrade", "2026-02-09")
    add("s4", "u4", "signup", "2026-01-07")
    add("a4", "u4", "core_action", "2026-01-08")
    add("r4", "u4", "core_action", "2026-02-11", consent=False)
    add("s5", "u5", "signup", "2026-02-01")
    add("a5", "u5", "core_action", "2026-02-02")
    add("r5", "u5", "core_action", "2026-03-08")
    add("x5", "u5", "upgrade", "2026-03-01")
    add("s6", "u6", "signup", "2026-03-01")
    add("a6", "u6", "core_action", "2026-03-02")
    add("s7", "u7", "signup", "2026-01-10", consent=False)
    add("a7", "u7", "core_action", "2026-01-11", consent=False)
    return users, events


if __name__ == "__main__":
    print(json.dumps(run(*fixture(), as_of="2026-04-15T00:00:00Z"), indent=2,
                     sort_keys=True))
