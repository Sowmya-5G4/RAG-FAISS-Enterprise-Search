# Retrieval-Augmented Generation (RAG) System with FAISS and Gemini

## Overview

This project implements a **production-style Retrieval-Augmented Generation (RAG) system** from scratch. The system retrieves relevant information from a document corpus using **semantic search with embeddings and a vector database (FAISS)** and optionally generates a natural-language answer using **Google Gemini**.

The focus of this project is **correct, explainable retrieval**, which is the most critical and challenging part of real-world RAG systems.

---

## Architecture (High Level)

```
User Query
   ↓
Query Classification (semantic)
   ↓
Query Decomposition (multi-intent handling)
   ↓
Embedding Generation (Gemini embeddings)
   ↓
FAISS Vector Search
   ↓
Relevant Context Chunks
   ↓
(Optional) LLM Generation (Gemini)
```

---

## Project Structure

```
RAG Project/
├── data/
│   └── docs/                 # Knowledge base documents
│
├── src/
│   ├── ingest.py             # Load documents
│   ├── chunk.py              # Chunk large documents
│   ├── embed_faiss.py        # Create embeddings + FAISS index
│   ├── retrieve_faiss.py     # FAISS-based retriever
│   ├── router.py             # Query classification
│   ├── generate.py           # LLM generation (guarded)
│   └── rag_pipeline.py       # End-to-end pipeline
│
├── vector.index              # FAISS index (generated)
├── chunks.npy                # Chunk text metadata
├── sources.npy               # Source metadata
├── requirements.txt
└── README.md
```

---

## Key Design Decisions

### 1. Why FAISS?

FAISS (Facebook AI Similarity Search) is used as the vector database because:

* It is **fast and scalable** for similarity search
* It is **free and local** (no external services required)
* It is widely used in research and production systems
* It cleanly separates **vector search** from **metadata storage**

FAISS allows the system to scale from small demos to **millions of document chunks** without changing architecture.

---

### 2. Why Gemini for Embeddings?

Gemini embedding models provide:

* High-quality semantic representations
* Strong performance on technical and enterprise text
* Easy integration with Google’s GenAI SDK

Embeddings are used for **semantic retrieval**, not keyword matching.

---

### 3. Why Only One Gemini Generation Model?

The project uses **one Gemini generation model** (e.g., `gemini-2.5-pro` or `gemini-flash-latest`) for the following reasons:

* Generation is **modular** and easily replaceable
* Retrieval quality matters more than generation model choice
* Free-tier API quotas are limited
* The system is designed so generation can be swapped with:

  * OpenAI GPT models
  * Local LLMs (Ollama / llama.cpp)
  * Any future model

The model choice does **not affect retrieval correctness**, which is the core of RAG.

---

## Retrieval Strategy

* Semantic embeddings are generated for document chunks
* FAISS performs similarity search
* A **similarity threshold** filters weak matches
* **Fallback logic** ensures at least one relevant chunk is returned
* **Multi-intent queries** are decomposed and retrieved independently

This avoids empty results and reduces noise.

---

## Generation Step

The generation step:

* Receives retrieved context
* Is restricted to answer **only using retrieved text**
* Is wrapped in error handling to gracefully handle API quota limits

If generation fails, the system still returns grounded context.

---

## Example Queries

```
What is machine learning?
How does security apply to machine learning systems?
How does cloud infrastructure support ML workloads?
What happens during a security incident?
```

---

## How to Run

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Set API key

```
export GEMINI_API_KEY=your_key_here
```

(Windows PowerShell)

```
setx GEMINI_API_KEY "your_key_here"
```

### 3. Build embeddings and FAISS index

```
python src/embed_faiss.py
```

### 4. Run the pipeline

```
python src/rag_pipeline.py
```

---

## Notes on API Quotas

* Gemini free-tier API limits may block generation
* Retrieval works independently of generation
* This is expected behavior and documented intentionally

---

## What This Project Demonstrates

* End-to-end RAG architecture
* Vector database usage (FAISS)
* Semantic retrieval with embeddings
* Multi-intent query handling
* Threshold-based filtering
* Robust fallback logic
* Production-style error handling

---

## Future Enhancements

* Add reranking model
* Add structured data (CSV / SQL) retrieval
* Add local LLM for generation
* Deploy as a web service

---

## Author

Built as a learning and portfolio project to demonstrate real-world RAG system design.
