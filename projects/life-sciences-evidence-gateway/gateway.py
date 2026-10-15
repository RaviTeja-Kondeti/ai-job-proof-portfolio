"""A small cited literature lookup that abstains on ambiguous or unsupported questions."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
STOP = {"a", "an", "and", "for", "in", "is", "of", "on", "paper", "reported",
        "study", "the", "to", "what", "which", "with"}


def tokens(text):
    return {part for part in re.findall(r"[a-z0-9]+(?:\.[0-9]+)?", text.lower())
            if part not in STOP}


def load_records(path=ROOT / "records.json"):
    records = json.loads(Path(path).read_text())
    seen = set()
    for record in records:
        if set(record) != {"pmid", "title", "year", "url", "terms", "evidence_note"}:
            raise ValueError("Invalid record schema")
        pmid = record["pmid"]
        if not re.fullmatch(r"\d{7,9}", pmid) or pmid in seen:
            raise ValueError("Invalid or duplicate PMID")
        if record["url"] != f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/":
            raise ValueError("Source URL does not match PMID")
        if not isinstance(record["year"], int) or not 1900 <= record["year"] <= 2100:
            raise ValueError("Invalid publication year")
        if not record["title"] or not record["evidence_note"] or not record["terms"]:
            raise ValueError("Missing evidence metadata")
        seen.add(pmid)
    return records


def lookup(question, records):
    if not isinstance(question, str):
        raise ValueError("Question must be text")
    query = tokens(question)
    if len(query) < 2:
        return {"status": "abstain", "reason": "too little context"}
    scored = []
    for record in records:
        indexed = tokens(record["title"] + " " + " ".join(record["terms"]))
        matched = sorted(query & indexed)
        scored.append((len(matched), record["pmid"], matched, record))
    scored.sort(key=lambda row: (-row[0], row[1]))
    best, runner_up = scored[0], scored[1] if len(scored) > 1 else (0, None, [], None)
    if best[0] < 2 or best[0] - runner_up[0] < 1:
        return {"status": "abstain", "reason": "unsupported or ambiguous"}
    record = best[3]
    return {"status": "cited_record", "pmid": record["pmid"],
            "title": record["title"], "year": record["year"],
            "source_url": record["url"], "evidence_note": record["evidence_note"],
            "matched_terms": best[2]}


def evaluate(records=None, cases=None):
    records = records if records is not None else load_records()
    cases = cases if cases is not None else json.loads((ROOT / "cases.json").read_text())
    outputs = []
    for case in cases:
        result = lookup(case["question"], records)
        actual = result.get("pmid")
        outputs.append({"question": case["question"], "expected_pmid": case["expected_pmid"],
                        "actual_pmid": actual, "correct": actual == case["expected_pmid"],
                        "result": result})
    return {"cases": outputs, "accuracy": sum(row["correct"] for row in outputs) / len(outputs),
            "record_count": len(records), "case_count": len(outputs)}


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
