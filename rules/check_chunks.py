"""
LegalBee - chunk checker (Asthra)

Checks data/chunks.json against docs/schema.md and lists any problems.
Also checks that every law ID in rules/topic_map.yaml has chunks.

Run it from the top of the repo:
    python rules/check_chunks.py
"""

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHUNKS_FILE = ROOT / "data" / "chunks.json"
SOURCES_CSV = ROOT / "data" / "sources.csv"
sys.path.insert(0, str(ROOT))

REQUIRED = ["chunk_id", "law_id", "law_name", "citation", "subsection", "text",
            "domain", "jurisdiction", "source_url", "tier", "last_verified"]
DOMAINS = {"tenant", "employment", "immigration"}
JURISDICTIONS = {"CA", "federal"}
TIERS = {1, 2, 3}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SUBSECTION = re.compile(r"^([a-z]{1,2}|full)$")


def source_law_ids():
    with open(SOURCES_CSV, newline="", encoding="utf-8") as f:
        return {row["Law ID"].strip() for row in csv.DictReader(f) if row.get("Law ID", "").strip()}


def check(chunks, known_law_ids):
    problems, warnings = [], []
    seen = set()
    for i, c in enumerate(chunks):
        name = c.get("chunk_id") or f"chunk #{i}"

        for field in REQUIRED:
            if c.get(field) in (None, ""):
                problems.append(f"{name}: missing {field}")

        if c.get("chunk_id") in seen:
            problems.append(f"{name}: duplicate chunk_id")
        seen.add(c.get("chunk_id"))

        law_id, sub = c.get("law_id"), c.get("subsection")
        if law_id and sub and c.get("chunk_id") != f"{law_id}-{sub}":
            problems.append(f"{name}: chunk_id should be {law_id}-{sub}")
        if law_id and law_id not in known_law_ids:
            problems.append(f"{name}: law_id {law_id} is not in data/sources.csv")
        if sub and not SUBSECTION.match(str(sub)):
            problems.append(f"{name}: subsection '{sub}' should be a lowercase letter or 'full'")

        if c.get("domain") and c["domain"] not in DOMAINS:
            problems.append(f"{name}: domain '{c['domain']}' must be one of {sorted(DOMAINS)}")
        if c.get("jurisdiction") and c["jurisdiction"] not in JURISDICTIONS:
            problems.append(f"{name}: jurisdiction '{c['jurisdiction']}' must be CA or federal")
        if c.get("tier") not in (None, "") and c["tier"] not in TIERS:
            problems.append(f"{name}: tier must be 1, 2 or 3")

        url = c.get("source_url") or ""
        if url and not url.startswith("https://"):
            problems.append(f"{name}: source_url must start with https://")

        for field in ("effective_date", "last_verified"):
            value = c.get(field)
            if value and not DATE.match(str(value)):
                problems.append(f"{name}: {field} '{value}' must be YYYY-MM-DD")

    # Warnings: allowed by the schema, but worth fixing
    no_date = sorted({c["law_id"] for c in chunks if not c.get("effective_date")})
    if no_date:
        warnings.append(f"No effective_date for: {', '.join(no_date)}")
    return problems, warnings


def check_topic_map(chunk_law_ids):
    try:
        from rules.match import all_topics
    except ImportError:
        return []
    missing = []
    for topic, law_ids in all_topics().items():
        for law_id in law_ids:
            if law_id not in chunk_law_ids:
                missing.append(f"topic '{topic}' uses {law_id}, which has no chunks yet")
    return missing


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else CHUNKS_FILE
    chunks = json.loads(path.read_text(encoding="utf-8"))
    problems, warnings = check(chunks, source_law_ids())
    warnings += check_topic_map({c.get("law_id") for c in chunks})

    laws = sorted({c.get("law_id") for c in chunks})
    print(f"Checked {len(chunks)} chunks from {len(laws)} laws: {', '.join(laws)}")
    for w in warnings:
        print("Warning:", w)
    if problems:
        print(f"{len(problems)} problem(s):")
        for p in problems:
            print(" -", p)
        sys.exit(1)
    print("All good: no missing URLs, law IDs or dates.")
