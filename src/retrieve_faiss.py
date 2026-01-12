import numpy as np
import faiss
import google.genai as genai
import os
import re

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

index = faiss.read_index("vector.index")
chunks = np.load("chunks.npy", allow_pickle=True)
sources = np.load("sources.npy", allow_pickle=True)

def split_query(query):
    parts = re.split(r'\band\b|\?|,', query.lower())
    cleaned = [p.strip() for p in parts if p.strip()]

    # Fallback for very short queries like "ml", "ai", "db"
    if not cleaned:
        return [query.lower().strip()]

    return cleaned


def retrieve(query, top_k=3, threshold=0.55):
    sub_queries = split_query(query)
    collected = {}

    for sub_q in sub_queries:
        q_emb = client.models.embed_content(
            model="models/text-embedding-004",
            contents=sub_q
        ).embeddings[0].values

        q_vec = np.array(q_emb, dtype="float32").reshape(1, -1)
        scores, indices = index.search(q_vec, top_k)

        for score, idx in zip(scores[0], indices[0]):
            src = sources[idx]

            # Always keep the best result per source
            if src not in collected or collected[src]["score"] < score:
                collected[src] = {
                    "source": src,
                    "text": chunks[idx],
                    "score": round(float(score), 3)
                }

    if not collected:
        return []

    results = list(collected.values())

    # Prefer strong matches, but never return empty
    strong = [r for r in results if r["score"] >= threshold]
    return strong if strong else [max(results, key=lambda x: x["score"])]
