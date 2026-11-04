# Chunk schema (final)

Every law is split into **chunks**: one chunk per top-level subsection (a), (b), (c).
All chunks live in `data/chunks.json`. `ingestion/chunk_laws.py` writes them from `data/sources.csv` and `data/raw/`.
Run `python rules/check_chunks.py` to check every chunk against this page.

## Fields

| Field | Required | Format | Example | Notes |
| --- | --- | --- | --- | --- |
| `chunk_id` | yes | `<law_id>-<subsection>` | `CIV-1950.5-g` | Must be unique |
| `law_id` | yes | see Law ID format | `CIV-1950.5` | Must match the Law ID column in `data/sources.csv` |
| `law_name` | yes | text | Security deposits | Plain-language name |
| `citation` | yes | text | Cal. Civ. Code § 1950.5 | Shown to users |
| `subsection` | yes | lowercase letters, no brackets | `g` | `full` if the law has no lettered subsections |
| `text` | yes | text | (a) This section applies... | Official wording of that subsection only. No edits or summaries |
| `domain` | yes | `tenant` / `employment` / `immigration` | tenant | Lowercase |
| `jurisdiction` | yes | `CA` / `federal` | CA | |
| `source_url` | yes | `https://` URL | https://leginfo... | Official government page only (leginfo, eCFR, uscis.gov, dir.ca.gov). No Justia or FindLaw |
| `tier` | yes | `1` / `2` / `3` | 1 | 1 = law, 2 = official guidance, 3 = legal aid |
| `effective_date` | recommended | `YYYY-MM-DD` | 2026-01-01 | When this version took effect. Leave empty only if truly unknown |
| `last_verified` | yes | `YYYY-MM-DD` | 2026-11-03 | Date a person last checked the text against the official site |

## Law ID format
Code abbreviation + section, no spaces:
- CA codes: `CIV-1950.5`, `LAB-510`, `CCP-1161`, `GOV-12940`
- Federal regs: `8CFR-214.2-f`, `29CFR-541.100`
- Federal statutes: `29USC-207`

## Example chunk

```json
{
  "chunk_id": "CIV-1950.5-a",
  "law_id": "CIV-1950.5",
  "law_name": "Security deposits",
  "citation": "Cal. Civ. Code § 1950.5",
  "subsection": "a",
  "text": "(a) This section applies to security for a rental agreement for residential property that is used as the dwelling of the tenant.",
  "domain": "tenant",
  "jurisdiction": "CA",
  "source_url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1950.5",
  "tier": 1,
  "effective_date": "",
  "last_verified": "2026-11-03"
}
```

## Before a chunk is accepted
- `python rules/check_chunks.py` prints "All good"
- `text` matches the official page word for word
- `last_verified` is the date a person actually checked it

## Not in the chunk
Topic tags (deposit, repairs, eviction...) live in `rules/topic_map.yaml`. The rules pick law IDs; search only looks inside those laws.
