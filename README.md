# 🧠 Semantic Cache for LLM Calls

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Groq](https://img.shields.io/badge/Groq-LLaMA3-orange)
![Embeddings](https://img.shields.io/badge/Embeddings-MiniLM-purple)
![License](https://img.shields.io/badge/License-MIT-green)

Stop paying for the same LLM call twice. Semantic cache returns cached answers for questions that **mean the same thing** — even if the wording is different.

---

## 🤔 The Problem

Normal caching is useless for LLMs:

```
"What is Python?"           → cache MISS (first time)
"Can you explain Python?"   → cache MISS (different string!)
"Tell me about Python"      → cache MISS (again!)
```

3 LLM calls. Same answer. Wasted money and time.

---

## ✅ The Solution

```
"What is Python?"           → LLM call → cached ✅
"Can you explain Python?"   → cache HIT 🎯 (similarity: 0.94)
"Tell me about Python"      → cache HIT 🎯 (similarity: 0.91)
```

1 LLM call. 3 answers served. 

---

## 🔧 How It Works

```
User Query
    │
    ▼
Convert to embedding vector (local, free)
    │
    ▼
Compare against cached embeddings (cosine similarity)
    │
    ├── score ≥ 0.85 → return cached answer instantly
    │
    └── score < 0.85 → call LLM → cache result → return answer
```

---

## 🚀 Quickstart

### 1. Clone & install
```bash
git clone https://github.com/<your-username>/semantic-cache-llm.git
cd semantic-cache-llm
pip install -r requirements.txt
```

### 2. Add your API key
```bash
# create a .env file
echo GROQ_API_KEY=your_key_here > .env
```
Get a free key at [console.groq.com](https://console.groq.com)

### 3. Run
```bash
python src/main.py
```

---

## 📁 Project Structure

```
semantic-cache-llm/
├── src/
│   ├── cache.py       # core: embed → search → store
│   └── main.py        # demo runner + Groq integration
├── .env               # your API key (never committed)
├── requirements.txt
├── NOTES.md
└── README.md
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| [Groq](https://groq.com) | Fast LLM inference |
| LLaMA 3.1 8B | Answer generation |
| `sentence-transformers` | Local embeddings (all-MiniLM-L6-v2) |
| `numpy` | Cosine similarity calculation |
| JSON file | Lightweight cache storage |

---

## 📊 Key Concept: Cosine Similarity

Embeddings are vectors. Cosine similarity measures the angle between them:

| Score | Meaning |
|-------|---------|
| 1.0 | Identical meaning |
| 0.85+ | Same question, different words → **cache hit** |
| < 0.85 | Different enough → call LLM |

---

## 📌 Roadmap

- [ ] Redis backend for production cache storage
- [ ] Cache TTL (expiry time)
- [ ] Cache stats dashboard (hit rate, savings)
- [ ] FastAPI wrapper to use as a drop-in proxy

---

## License

MIT
