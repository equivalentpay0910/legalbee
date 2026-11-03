"""
LegalBee - chunking prototype (Esha, Week 1-2)

What it does
  1. Reads data/sources.csv (exported from the "Sources" tab of the team sheet)
  2. For each law, reads its official text from data/raw/<law_id>.txt
     (paste the text straight from leginfo / eCFR into that file)
  3. Splits the text into one chunk per top-level subsection: (a), (b), (c), ...
  4. Tags every chunk with the schema fields and writes data/chunks.json

Run it from the top of the repo:
    python ingestion/chunk_laws.py
"""

import csv
import json
import re
import string
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES_CSV = ROOT / "data" / "sources.csv"
RAW_DIR = ROOT / "data" / "raw"
OUT_FILE = ROOT / "data" / "chunks.json"

# A line that starts a top-level subsection looks like "(a) The landlord ..."
SUBSECTION_START = re.compile(r"^\(([a-z]{1,2})\)\s*(.*)")


def expected_labels():
    """a, b, ..., z, then aa, bb, ... (the order California codes use)."""
    letters = list(string.ascii_lowercase)
    return letters + [c * 2 for c in letters]


ROMAN_LOOKALIKES = {"i", "v", "x"}  # also used as nested roman numerals


def _step_to(label, labels, next_i):
    """
    How many letters ahead of the expected one this label is (0 = exactly next),
    or None if it isn't a new top-level subsection.
    Allows up to 2 skipped letters (in case a paste dropped one), except for
    i / v / x, which must be exactly next because they are also roman numerals.
    """
    for step in range(3):
        idx = next_i + step
        if idx < len(labels) and labels[idx] == label:
            if step > 0 and label in ROMAN_LOOKALIKES:
                return None
            return step
    return None


def split_subsections(text):
    """
    Split statute text into top-level subsections.

    Only splits on the NEXT expected letter, so nested items like (i) inside
    (h)(1)(A) are not mistaken for a new top-level subsection.
    Text before "(a)" (or a law with no lettered subsections) becomes one chunk
    labelled "full".
    """
    labels = expected_labels()
    next_i = 0
    chunks = []
    current_label, current_lines = "full", []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        m = SUBSECTION_START.match(line)
        step = _step_to(m.group(1), labels, next_i) if m else None
        if step is not None:
            if current_lines:
                chunks.append((current_label, " ".join(current_lines)))
            current_label, current_lines = m.group(1), [line]
            next_i += step + 1
        else:
            current_lines.append(line)

    if current_lines:
        chunks.append((current_label, " ".join(current_lines)))

    # Drop a tiny preamble (e.g. just the section number) if real subsections exist
    if len(chunks) > 1 and chunks[0][0] == "full" and len(chunks[0][1]) < 40:
        chunks = chunks[1:]
    return chunks


def load_sources():
    with open(SOURCES_CSV, newline="", encoding="utf-8") as f:
        return [row for row in csv.DictReader(f) if row.get("Law ID", "").strip()]


def build_chunks():
    sources = load_sources()
    all_chunks, missing = [], []

    for row in sources:
        law_id = row["Law ID"].strip()
        raw_file = RAW_DIR / f"{law_id}.txt"
        if not raw_file.exists():
            missing.append(law_id)
            continue

        text = raw_file.read_text(encoding="utf-8")
        for label, chunk_text in split_subsections(text):
            all_chunks.append({
                "chunk_id": f"{law_id}-{label}",
                "law_id": law_id,
                "law_name": row.get("Law name", "").strip(),
                "citation": row.get("Citation", "").strip(),
                "subsection": label,
                "text": chunk_text,
                "domain": row.get("Domain", "").strip().lower(),
                "jurisdiction": row.get("Jurisdiction", "").strip(),
                "source_url": row.get("Official URL", "").strip(),
                "tier": 1,
                "effective_date": row.get("Effective date", "").strip(),
                "last_verified": row.get("Last verified", "").strip()
                or date.today().isoformat(),
            })

    OUT_FILE.write_text(json.dumps(all_chunks, indent=2, ensure_ascii=False), encoding="utf-8")

    laws_done = len({c["law_id"] for c in all_chunks})
    print(f"Wrote {len(all_chunks)} chunks from {laws_done} laws to {OUT_FILE.relative_to(ROOT)}")
    if missing:
        print("No text file yet for:", ", ".join(missing))
        print(f"  -> paste each law's text into {RAW_DIR.relative_to(ROOT)}/<Law ID>.txt")


if __name__ == "__main__":
    build_chunks()
