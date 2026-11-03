"""
LegalBee - retrieval step (Esha)

Given a question and the law IDs the rules step picked, return the most
relevant chunks. Never searches outside the matched laws.

    from retrieval.search import search
    results = search("Can my landlord keep my deposit?", ["CIV-1950.5"])

Ranking:
  - sentence-transformers (meaning) when installed and the model can load
  - BM25 keywords (rank_bm25) as a fallback, and later as the hybrid partner
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHUNKS_FILE = ROOT / "data" / "chunks.json"
MODEL_NAME = "all-MiniLM-L6-v2"

_model = None


def load_chunks():
    return json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))


def _tokens(text):
    return re.findall(r"[a-z0-9.]+", text.lower())


def _get_model():
    """Load the embedding model once; return None if it isn't available."""
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _model = SentenceTransformer(MODEL_NAME)
        except Exception as err:  # not installed, or no internet for first download
            print(f"[search] embeddings unavailable ({err.__class__.__name__}); using keyword ranking")
            _model = False
    return _model or None


def _rank_by_meaning(question, candidates, model):
    from sentence_transformers import util
    q_vec = model.encode(question, convert_to_tensor=True)
    c_vecs = model.encode([c["text"] for c in candidates], convert_to_tensor=True)
    return util.cos_sim(q_vec, c_vecs)[0].tolist()


def _rank_by_keywords(question, candidates):
    from rank_bm25 import BM25Okapi
    bm25 = BM25Okapi([_tokens(c["text"]) for c in candidates])
    return list(bm25.get_scores(_tokens(question)))


def search(question, law_ids, top_k=4):
    """Return up to top_k chunks from the given laws, best match first."""
    candidates = [c for c in load_chunks() if c["law_id"] in set(law_ids)]
    if not candidates:
        return []

    model = _get_model()
    scores = (_rank_by_meaning(question, candidates, model) if model
              else _rank_by_keywords(question, candidates))

    ranked = sorted(zip(scores, candidates), key=lambda pair: pair[0], reverse=True)
    return [dict(chunk, score=round(float(score), 3)) for score, chunk in ranked[:top_k]]


if __name__ == "__main__":
    import sys
    q = sys.argv[1] if len(sys.argv) > 1 else "How long does my landlord have to return my deposit?"
    laws = sys.argv[2].split(",") if len(sys.argv) > 2 else ["CIV-1950.5"]
    for hit in search(q, laws):
        print(f"{hit['score']:>7}  {hit['chunk_id']:<16} {hit['text'][:90]}...")
