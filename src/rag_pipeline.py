from retrieve_faiss import retrieve
from router import classify_query
from generate import generate_answer
from generate_ollama import generate_answer
from rerank import rerank


def normalize_query(query):
    q = query.lower().strip()

    alias_map = {
        "ml": "What is machine learning?",
        "why ml": "Why is machine learning important?",
        "ai": "What is artificial intelligence?",
        "cloud": "What is cloud computing?",
        "security": "Why is security important?",
        "cloud security": "How does security apply to cloud systems?",
    }

    return alias_map.get(q, query)

query = input("Ask a question: ")
normalized_query = normalize_query(query)


route = classify_query(query)
print(f"\nQuery type: {route}")

if route == "semantic":
    results = retrieve(normalized_query, top_k=10)
    results = rerank(normalized_query, results, top_k=3)


    if not results:
        print("\nNo relevant context found. Try rephrasing the question.\n")
    else:
        print("\nRetrieved context:\n")
        for r in results:
            print(f"[{r['source']}] score={r['score']}")
            print(r["text"])
            print("-" * 40)

        print("\nGenerated answer:\n")
        answer = generate_answer(normalized_query, results)

# 🔹 Add citations
sources = sorted(set(r["source"] for r in results))
citations = "\n".join(f"- {s}" for s in sources)

# 🔹 Confidence score (based on retrieval similarity)
confidence_score = max(r["score"] for r in results)

if confidence_score >= 0.75:
    confidence_label = "High"
elif confidence_score >= 0.5:
    confidence_label = "Medium"
else:
    confidence_label = "Low"

final_answer = f"""{answer}

Confidence: {confidence_label} ({confidence_score:.2f})

Sources:
{citations}
"""


print(final_answer)

