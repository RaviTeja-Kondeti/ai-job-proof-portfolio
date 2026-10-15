"""Count inspectable artifact links in current line-by-line job maps.

This is a link inventory, not a judgment that a project satisfies a job test.
"""

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAP_DIR = ROOT / "job-maps"
ARTIFACT = re.compile(r"\]\((?:\.\./projects/|https://github\.com/RaviTeja-Kondeti/)")
MAP_LINK = re.compile(r"\]\(([a-z0-9-]+\.md)\)")


def table_rows(path: Path) -> list[str]:
    lines = path.read_text().splitlines()
    for index in range(len(lines) - 1):
        if lines[index].startswith("|") and re.fullmatch(r"[\s|:\-]+", lines[index + 1]):
            rows = []
            for line in lines[index + 2:]:
                if not line.startswith("|"):
                    break
                rows.append(line)
            return rows
    raise ValueError(f"No Markdown table found in {path}")


def first_signal(row: str) -> str:
    cells = [cell.strip() for cell in row.strip("|").split("|")]
    # Five-column maps use an ID followed by the substantive signal.
    signal = cells[1] if len(cells) >= 5 and re.fullmatch(r"[A-Z]\d{2}", cells[0]) else cells[0]
    return re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", signal)


def current_maps() -> list[Path]:
    index = (MAP_DIR / "index.md").read_text()
    names = set(MAP_LINK.findall(index))
    ignored = {"index.md", "screening-notes.md", "previous-shortlist.md"}
    return [MAP_DIR / name for name in sorted(names - ignored)
            if (MAP_DIR / name).is_file()]


def indexed_roles() -> list[str]:
    return [line for line in (MAP_DIR / "index.md").read_text().splitlines()
            if re.match(r"^\| (?:Sep|Oct) \d+ \|", line)]


def audit() -> tuple[list[dict], list[tuple[str, str]]]:
    summary = []
    gaps = []
    for path in current_maps():
        rows = table_rows(path)
        linked = sum(bool(ARTIFACT.search(row)) for row in rows)
        external = sum("Candidate verification" in row or "Pending user" in row
                       for row in rows)
        summary.append({"map": path.name, "tests": len(rows),
                        "linked": linked, "unlinked": len(rows) - linked,
                        "external": external})
        for row in rows:
            if not ARTIFACT.search(row):
                gaps.append((path.name, first_signal(row)))
    return summary, gaps


def markdown(summary: list[dict]) -> str:
    total_tests = sum(row["tests"] for row in summary)
    total_linked = sum(row["linked"] for row in summary)
    total_external = sum(row["external"] for row in summary)
    roles = indexed_roles()
    mapped_roles = sum(bool(MAP_LINK.search(line)) for line in roles)
    lines = [
        "# Proof-link coverage for current role maps",
        "",
        "This inventory checks **only whether a mapped test row links to an inspectable project or the candidate's existing public GitHub work**. One artifact may support several rows; this audit does not prove that every line has its own distinct project. A link can be partial, synthetic, inconclusive, or irrelevant to a production qualification; it does not establish that the test has been passed. The tool also cannot verify that every sentence of the live posting was mapped. [The role queue](job-maps/index.md) defines which maps are current for this audit.",
        "",
        f"Salary/date-screened role rows: **{len(roles)}**. Roles with a line map: **{mapped_roles}**. Roles without a line map: **{len(roles)-mapped_roles}**. Current mapped roles audited here: **{len(summary)}**.",
        "",
        f"Mapped test rows: **{total_tests}**. Rows with an artifact link: **{total_linked}**. Rows without one: **{total_tests-total_linked}**. Rows explicitly requiring candidate-supplied history or credentials: **{total_external}** (may overlap either link category).",
        "",
        "| Current role map | Test rows | With artifact link | Without artifact link | Candidate verification rows |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in summary:
        lines.append(f"| [{row['map'].removesuffix('.md')}](job-maps/{row['map']}) | "
                     f"{row['tests']} | {row['linked']} | {row['unlinked']} | {row['external']} |")
    lines += [
        "",
        "Run `python3 tools/audit_proof_links.py --gaps` for every current row without a linked artifact; use `--unmapped-roles` for salary/date-screened roles without a map. Run `python3 tools/audit_proof_links.py --markdown` to regenerate this table. Update maps only after inspecting and testing the linked work; an existing artifact is not automatically proof of the exact posting line.",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    summary, gaps = audit()
    if "--gaps" in sys.argv:
        for filename, signal in gaps:
            print(f"{filename}: {signal}")
    elif "--unmapped-roles" in sys.argv:
        for row in indexed_roles():
            if not MAP_LINK.search(row):
                print(row.split("|")[2].strip())
    else:
        print(markdown(summary))
