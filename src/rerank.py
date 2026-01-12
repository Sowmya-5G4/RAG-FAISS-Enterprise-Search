from sentence_transformers import CrossEncoder

# Lightweight, fast, very common reranker
model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query, results, top_k=3):
    """
    Rerank retrieved results using a cross-encoder
    """
    pairs = [(query, r["text"]) for r in results]
    scores = model.predict(pairs)

    # Attach rerank scores
    for r, score in zip(results, scores):
        r["rerank_score"] = float(score)

    # Sort by rerank score
    reranked = sorted(results, key=lambda x: x["rerank_score"], reverse=True)

    return reranked[:top_k]
