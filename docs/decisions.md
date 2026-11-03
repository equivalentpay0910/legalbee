# LegalBee decisions log

Every choice the team locks in goes here, newest first, with the reason.

| Date | Decision | Why |
| --- | --- | --- |
| 2026-10-25 | **LLM:** Groq (Llama 3.3 70B). Backup: GitHub Models | Free, no card, doesn't train on our prompts |
| 2026-10-25 | **Embeddings:** sentence-transformers `all-MiniLM-L6-v2`, run locally | Free, no API key |
| 2026-10-25 | **No vector DB for the MVP.** Filter chunks by law ID, rank in memory. Add Chroma if the corpus passes ~60 laws | 30-60 laws is small; rules already narrow each question |
| 2026-10-25 | **Keyword search:** rank_bm25 (fallback now, hybrid in Week 4) | Catches exact section numbers like "1950.5" |
| 2026-10-25 | **Rules + questionnaire:** YAML files in `rules/` | Non-coders can edit them on github.com |
| 2026-10-25 | **Website:** Streamlit; hosted on Streamlit Community Cloud | Free, pure Python |
| 2026-10-25 | **Chunking:** one chunk per top-level subsection (a), (b), (c) | Keeps citations exact (from Khushi's source plan) |
| 2026-10-25 | **Immigration scope:** F-1 students (CPT, OPT, STEM OPT) | Fits SJSU users (from Khushi's source plan) |
| 2026-10-11 | Scope: CA + overlapping federal law; tenant, employment, immigration | Target users are CA students, young renters, immigrants |
| 2026-10-11 | Rule-based matching before RAG | Predictable routing, fewer hallucinations |

## Open
- Frontend owner
- RCC final deadline (plan assumes Sun Nov 29)
- San José rent ordinance: stretch goal
