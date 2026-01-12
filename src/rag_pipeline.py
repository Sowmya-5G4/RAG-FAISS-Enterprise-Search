from retrieve_faiss import retrieve
from router import classify_query
from generate import generate_answer
from generate_ollama import generate_answer


query = input("Ask a question: ")

route = classify_query(query)
print(f"\nQuery type: {route}")

if route == "semantic":
    results = retrieve(query, top_k=3)

    if not results:
        print("\nNo relevant context found. Try rephrasing the question.\n")
    else:
        print("\nRetrieved context:\n")
        for r in results:
            print(f"[{r['source']}] score={r['score']}")
            print(r["text"])
            print("-" * 40)

        print("\nGenerated answer:\n")
        answer = generate_answer(query, results)

# 🔹 Add citations
sources = sorted(set(r["source"] for r in results))
citations = "\n".join(f"- {s}" for s in sources)

final_answer = f"""{answer}

Sources:
{citations}
"""

print(final_answer)

