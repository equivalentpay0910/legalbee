# LegalBee Chunk Schema

Every law is split into **chunks**, one chunk per lettered subsection: (a), (b), (c)...
Never split by character count, because that breaks citations.

All chunks live in `data/chunks.json` as a list of objects.

## Fields

| Field | Type | Required | Rule | Example |
| --- | --- | --- | --- | --- |
| chunk_id | string | yes | `law_id` + `-` + subsection. Must be unique. | `CIV-1950.5-b` |
| law_id | string | yes | Must match the Law ID in the Sources tab. | `CIV-1950.5` |
| citation | string | yes | Official citation, written the way a person would cite it. | `Cal. Civ. Code § 1950.5(b)` |
| subsection | string | yes | Letter or number only, no parentheses. Use `full` if the law has no subsections. | `b` |
| text | string | yes | Exact official wording. No summaries, no edits. | `(text copied from leginfo)` |
| domain | string | yes | One of: `tenant`, `employment`, `immigration` | `tenant` |
| jurisdiction | string | yes | One of: `federal`, `california`, `city` | `california` |
| source_url | string | yes | Official government URL only. No blogs, Justia, or FindLaw. | `https://leginfo.legislature.ca.gov/...` |
| tier | integer | yes | `1` = law text (statute or regulation). `2` = official guidance (CA Courts Self-Help, Study in the States, DIR FAQs). | `1` |
| effective_date | string | no | `YYYY-MM-DD`. Leave empty if unknown. | `2024-07-01` |
| last_verified | string | yes | `YYYY-MM-DD`. Date someone last checked the text against the official source. | `2026-11-01` |

## Law ID format

| Domain | Format | Example |
| --- | --- | --- |
| CA Civil Code | `CIV-<section>` | `CIV-1950.5` |
| CA Code of Civil Procedure | `CCP-<section>` | `CCP-1161` |
| CA Labor Code | `LAB-<section>` | `LAB-510` |
| Federal regulations | `<title>CFR-<section>-<subsection>` | `8CFR-214.2-f-10` |

## Example chunk

```json
{
  "chunk_id": "CIV-1950.5-b",
  "law_id": "CIV-1950.5",
  "citation": "Cal. Civ. Code § 1950.5(b)",
  "subsection": "b",
  "text": "(exact text of subsection (b) copied from leginfo)",
  "domain": "tenant",
  "jurisdiction": "california",
  "source_url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1950.5",
  "tier": 1,
  "effective_date": "",
  "last_verified": "2026-11-01"
}
```

## Checklist before a chunk is accepted

- [ ] Every required field is filled in
- [ ] `chunk_id` is unique across the whole file
- [ ] `law_id` exists in the Sources tab
- [ ] `source_url` opens an official government page
- [ ] `text` matches the official page word for word

## Not in the chunk

Matching tags (deposit, repairs, eviction, F-1 work, and so on) live in `rules/topic_map.yaml`, not in each chunk. The rules pick law IDs, and search only looks inside those laws.

## Open questions

- Does `tier` mean what this doc says? Please confirm.
- Who updates `last_verified`, and how often?
