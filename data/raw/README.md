# data/raw

One text file per law, named by its Law ID, e.g. `CIV-1950.5.txt`.

How to fill one in:
1. Open the law's Official URL from the Sources tab (leginfo for CA codes, eCFR for federal rules)
2. Select the law text only, from `(a)` to the end. Skip menus and the section title
3. Paste into a new file here named `<Law ID>.txt` and save
4. Keep each `(a)`, `(b)`, `(c)` at the **start of its own line** so the chunker can split it

Then run `python ingestion/chunk_laws.py` from the top of the repo.
