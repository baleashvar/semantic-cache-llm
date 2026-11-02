import os
import sys
import time
from groq import Groq
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(__file__))
import cache

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def ask(query: str) -> str:
    # 1. Check cache first
    cached = cache.get(query)
    if cached:
        return cached

    # 2. Cache miss — call LLM
    print("  [LLM CALL] querying Groq...")
    start = time.time()
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": query}],
        max_tokens=200,
    )
    elapsed = time.time() - start
    answer = response.choices[0].message.content.strip()
    print(f"  [LLM DONE] took {elapsed:.2f}s")

    # 3. Store in cache for next time
    cache.set(query, answer)
    return answer


if __name__ == "__main__":
    test_queries = [
        "What is Python?",                          # 1st call  → LLM
        "Can you explain Python to me?",            # similar   → cache hit
        "Tell me about the Python language",        # similar   → cache hit
        "What is machine learning?",                # different → LLM
        "Explain machine learning in simple terms", # similar   → cache hit
    ]

    for q in test_queries:
        print(f"\nQ: {q}")
        answer = ask(q)
        print(f"A: {answer[:100]}...")
