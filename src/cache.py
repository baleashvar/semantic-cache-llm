import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer

CACHE_FILE = "cache_store.json"
THRESHOLD = 0.85  # similarity score needed to count as a cache hit

# Loaded once at startup — runs locally, no API needed
model = SentenceTransformer("all-MiniLM-L6-v2")


def _load() -> list:
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return []


def _save(store: list):
    with open(CACHE_FILE, "w") as f:
        json.dump(store, f, indent=2)


def _cosine_similarity(a: list, b: list) -> float:
    # Measures how similar two vectors are (1.0 = identical meaning, 0.0 = unrelated)
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def get(query: str) -> str | None:
    """Search cache for a semantically similar query. Returns answer or None."""
    store = _load()
    if not store:
        return None

    query_embedding = model.encode(query).tolist()

    best_score, best_answer = 0.0, None
    for entry in store:
        score = _cosine_similarity(query_embedding, entry["embedding"])
        if score > best_score:
            best_score, best_answer = score, entry["answer"]

    if best_score >= THRESHOLD:
        print(f"  [CACHE HIT] similarity={best_score:.3f}")
        return best_answer

    print(f"  [CACHE MISS] best similarity={best_score:.3f}")
    return None


def set(query: str, answer: str):
    """Store a query+answer pair with its embedding."""
    store = _load()
    store.append({
        "query": query,
        "embedding": model.encode(query).tolist(),
        "answer": answer,
    })
    _save(store)
    print(f"  [CACHED] query stored ({len(store)} total entries)")
