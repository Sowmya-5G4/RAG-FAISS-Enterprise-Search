from src.router import classify_query
from src.retrieve_faiss import retrieve
from src.rerank import rerank
from src.generate_ollama import generate_answer
from src.structured_qa import answer_structured_query


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


def run_cli():
    query = input("Ask a question: ")
    normalized_query = normalize_query(query)

    route = classify_query(normalized_query)
    print(f"\nQuery type: {route}")

    # ---------------- STRUCTURED PATH ----------------
    if route == "structured":
        answer = answer_structured_query(normalized_query)
        print("\nAnswer:\n")
        print(answer)

    # ---------------- SEMANTIC (RAG) PATH ----------------
    else:
        results = retrieve(normalized_query, top_k=10)
        results = rerank(normalized_query, results, top_k=3)

        if not results:
            print("\nNo relevant context found. Try rephrasing the question.\n")
            return

        print("\nRetrieved context:\n")
        for r in results:
            print(f"[{r['source']}] score={r['score']}")
            print(r["text"])
            print("-" * 40)

        answer = generate_answer(normalized_query, results)

        # 🔹 Citations
        sources = sorted(set(r["source"] for r in results))
        citations = "\n".join(f"- {s}" for s in sources)

        # 🔹 Confidence score
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

        print("\nGenerated answer:\n")
        print(final_answer)


# 🔐 IMPORTANT: Prevent FastAPI from executing CLI input
if __name__ == "__main__":
    run_cli()
