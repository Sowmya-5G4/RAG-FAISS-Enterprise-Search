import json
from src.retrieve_faiss import retrieve
from src.rerank import rerank


def precision_at_k(results, relevant_sources, k):
    retrieved_sources = [r["source"] for r in results[:k]]
    relevant_retrieved = [
        s for s in retrieved_sources if s in relevant_sources
    ]
    return len(relevant_retrieved) / k


def recall_at_k(results, relevant_sources, k):
    retrieved_sources = [r["source"] for r in results[:k]]
    for src in relevant_sources:
        if src in retrieved_sources:
            return 1.0
    return 0.0


def run_evaluation(k=3):
    with open("data/eval_queries.json") as f:
        eval_data = json.load(f)

    precision_scores = []
    recall_scores = []

    for item in eval_data:
        query = item["query"]
        relevant_sources = item["relevant_sources"]

        results = retrieve(query, top_k=10)
        results = rerank(query, results, top_k=k)

        p = precision_at_k(results, relevant_sources, k)
        r = recall_at_k(results, relevant_sources, k)

        precision_scores.append(p)
        recall_scores.append(r)

        print(f"\nQuery: {query}")
        print(f"Precision@{k}: {p:.2f}")
        print(f"Recall@{k}: {r:.2f}")

    print("\n=== Overall Metrics ===")
    print(f"Avg Precision@{k}: {sum(precision_scores)/len(precision_scores):.2f}")
    print(f"Avg Recall@{k}: {sum(recall_scores)/len(recall_scores):.2f}")


if __name__ == "__main__":
    run_evaluation(k=3)
