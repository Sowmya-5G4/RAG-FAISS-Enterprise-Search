import google.genai as genai
import os
import numpy as np
import faiss
from ingest import load_documents
from chunk import chunk_text

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

documents = load_documents()

embeddings = []
chunks = []
sources = []

for doc in documents:
    doc_chunks = chunk_text(doc["text"])
    for chunk in doc_chunks:
        response = client.models.embed_content(
            model="models/text-embedding-004",
            contents=chunk
        )
        vector = np.array(response.embeddings[0].values, dtype="float32")
        embeddings.append(vector)
        chunks.append(chunk)
        sources.append(doc["source"])

# Convert to numpy array
embedding_matrix = np.vstack(embeddings)

# Create FAISS index
dim = embedding_matrix.shape[1]
index = faiss.IndexFlatIP(dim)   # Inner Product ≈ cosine similarity
index.add(embedding_matrix)

# Save everything
faiss.write_index(index, "vector.index")
np.save("chunks.npy", chunks)
np.save("sources.npy", sources)

print("✅ FAISS index created")
