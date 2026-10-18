# LegalBee

A legal information copilot for young Californians, built by SJSU Responsible Computing Club.

## Structure
```
legalbee/
├── ingestion/   # scraping and loading legal sources
├── retrieval/   # vector DB and search
├── rules/       # questionnaire → topic matching
├── llm/         # prompts and explanation layer
├── app/         # frontend
├── eval/        # test questions and accuracy checks
└── docs/        # architecture diagram and decisions
```
# 2 parts of LegalBee
- Ahead of time # we build our library
  collect official legal sources, clean that text, break into small chunks, store each in a vector DB, tag where it comes from + what domain it is in + when we last checked it. only thing bot is allowed to use
- Live part # 5 steps
  questionnaire (user answers simple questions eg. where they live + is this about housing or work or immigration + what is going on)
  rules (fixed logic, no AI, takes those answers and decides which area of law applies. they are referred out if this is out of scope)
  retrieval (search the vector DB for legal text that best matches their situation)
  LLM (takes only those retrieved chunks and explains in plain language. no hallucination)
  Answer (user sees the explanation, the exact sources with links, like a legal aid office nearby)

  eval tests each step with real questions we've written, to catch wrong answers or missing citations.
