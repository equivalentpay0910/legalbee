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
## How LegalBee Works

LegalBee has two parts:

### 1. Ahead of time: building our library
- Collect official legal sources
- Clean the text and break it into small chunks
- Store each chunk in a vector DB, tagged with:
  - where it comes from
  - what domain it is in
  - when we last checked it

> This library is the **only** thing the bot is allowed to use.

### 2. Live part: 5 steps

1. **Questionnaire**: the user answers simple questions (e.g., where they live, whether this is about housing, work or immigration, and what is going on)
2. **Rules**: fixed logic, no AI. Takes those answers and decides which area of law applies. Users are referred out if their question is out of scope.
3. **Retrieval**: searches the vector DB for the legal text that best matches their situation
4. **LLM**: takes only those retrieved chunks and explains them in plain language. No hallucination.
5. **Answer**: the user sees the explanation, the exact sources with links, and next steps (like a nearby legal aid office)

### Evaluation
Eval tests each step with real questions we've written, to catch wrong answers or missing citations.
