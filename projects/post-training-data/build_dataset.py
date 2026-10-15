"""Validate and manifest a tiny synthetic SFT/preference/RL dataset."""

import hashlib
import json
from pathlib import Path


REQUIRED = {
    "sft": {"prompt", "response"},
    "preference": {"prompt", "chosen", "rejected"},
    "rl": {"prompt", "response", "reward"},
}


def build_manifest(rows: list[dict]) -> dict:
    if not rows:
        raise ValueError("Dataset is empty")
    seen = set()
    counts = {kind: 0 for kind in REQUIRED}
    normalized = []
    for row in rows:
        kind = row.get("type")
        if kind not in REQUIRED:
            raise ValueError(f"Unknown record type: {kind}")
        if not {"id", "source", "created_at", *REQUIRED[kind]} <= row.keys():
            raise ValueError(f"Missing required fields: {row.get('id')}")
        if not all(row.get(field) for field in ("id", "source", "created_at")):
            raise ValueError("Every record needs identity, provenance and date")
        if row["id"] in seen:
            raise ValueError(f"Duplicate ID: {row['id']}")
        if kind == "preference" and row["chosen"] == row["rejected"]:
            raise ValueError("Preference pair must contain distinct responses")
        if kind == "rl" and not isinstance(row["reward"], (int, float)):
            raise ValueError("Reward must be numeric")
        if any(not isinstance(row[field], str) or not row[field].strip()
               for field in REQUIRED[kind] - {"reward"}):
            raise ValueError("Text fields cannot be empty")
        seen.add(row["id"])
        counts[kind] += 1
        normalized.append(row)
    payload = json.dumps(sorted(normalized, key=lambda row: row["id"]),
                         sort_keys=True, separators=(",", ":")).encode()
    return {
        "schema_version": 1,
        "record_count": len(rows),
        "type_counts": counts,
        "sha256": hashlib.sha256(payload).hexdigest(),
        "warning": "Synthetic records; manifest only, not production lineage or scale",
    }


if __name__ == "__main__":
    rows = json.loads(Path(__file__).with_name("synthetic_records.json").read_text())
    print(json.dumps(build_manifest(rows), indent=2))
