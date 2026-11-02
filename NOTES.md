# NOTES — Semantic Cache for LLM Calls

## Concept
- Normal cache: exact string match
- Semantic cache: meaning match using embeddings + cosine similarity
- Saves LLM calls when two questions mean the same thing

## Stack
- Groq: LLM calls
- sentence-transformers (all-MiniLM-L6-v2): local embedding model
- numpy: cosine similarity
- json file: cache storage

## Files
- src/cache.py  → SemanticCache class (embed, search, store)
- src/main.py   → demo runner

## Key concepts learned
- Embeddings: text → vector of floats representing meaning
- Cosine similarity: measures angle between vectors (1.0 = identical, 0.0 = unrelated)
- Threshold: 0.85 means "85% similar = treat as same question"
