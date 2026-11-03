# Chunk schema (draft: Asthra to finalize)

Every chunk in `data/chunks.json` has these fields. `ingestion/chunk_laws.py` already writes them.

| Field | Example | Notes |
| --- | --- | --- |
| `chunk_id` | `CIV-1950.5-g` | Law ID + subsection letter. Unique |
| `law_id` | `CIV-1950.5` | Same as the Law ID column in the Sources tab |
| `law_name` | Security deposits | Plain-language name |
| `citation` | Cal. Civ. Code § 1950.5 | Shown to users |
| `subsection` | `g` | `full` if the law has no lettered subsections |
| `text` | (a) ... | Official text of that subsection only |
| `domain` | tenant | tenant / employment / immigration |
| `jurisdiction` | CA | CA or federal |
| `source_url` | https://leginfo... | Official page; shown as the source link |
| `tier` | 1 | 1 = law, 2 = official guidance, 3 = legal aid |
| `effective_date` | 2026-01-01 | When this version took effect, if known |
| `last_verified` | 2026-11-03 | Date someone last checked it against the official site |

## Law ID format
Code abbreviation + section, no spaces:
- CA codes: `CIV-1950.5`, `LAB-510`, `CCP-1161`, `GOV-12940`
- Federal regs: `8CFR-214.2-f`, `29CFR-541.100`
- Federal statutes: `29USC-207`
