📘 Retrieval-Augmented Generation (RAG) System with FAISS, Hybrid Routing & FastAPI
Overview

This project implements a production-style Retrieval-Augmented Generation (RAG) system from scratch, focusing on correct retrieval, explainability, and real-world system design rather than prompt-only demos.

The system supports:

Semantic document retrieval using embeddings and FAISS

Hybrid query routing for structured (CSV) and unstructured (text) data

Cross-encoder reranking for improved retrieval precision

Confidence scoring and source citations

Optional local LLM-based answer generation using Ollama

FastAPI deployment for real API-based usage

The primary goal is to demonstrate how enterprise-grade knowledge search and analytics systems are designed, evaluated, and deployed.

🧠 High-Level Architecture
User Query
   ↓
Query Normalization
   ↓
Query Router
   ├── Structured Queries → Pandas (CSV analytics)
   └── Semantic Queries
         ↓
     FAISS Vector Search
         ↓
     Cross-Encoder Reranking
         ↓
     Context Selection
         ↓
(Optional) Local LLM Generation (Ollama)
         ↓
Answer + Confidence + Sources

📁 Project Structure
RAG Project/
├── data/
│   ├── docs/                 # Unstructured knowledge base (text files)
│   ├── tables/               # Structured CSV data
│   └── eval_queries.json     # Evaluation dataset
│
├── src/
│   ├── api.py                # FastAPI service
│   ├── ingest.py             # Document loading
│   ├── chunk.py              # Document chunking
│   ├── embed_faiss.py        # Embeddings + FAISS index creation
│   ├── retrieve_faiss.py     # FAISS-based retriever
│   ├── rerank.py             # Cross-encoder reranking
│   ├── router.py             # Query classification
│   ├── structured_qa.py      # CSV-based analytics
│   ├── generate_ollama.py    # Local LLM generation (Ollama)
│   ├── evaluate.py           # Precision@K / Recall@K evaluation
│   └── rag_pipeline.py       # CLI pipeline (isolated from API)
│
├── requirements.txt
└── README.md

🔍 Key Design Decisions
1️⃣ Why FAISS?

FAISS (Facebook AI Similarity Search) is used as the vector database because:

Extremely fast similarity search

Scales from small demos to millions of vectors

Fully local and free (no external services required)

Widely used in research and production systems

FAISS cleanly separates vector search from metadata storage, mirroring real-world architectures.

2️⃣ Why Hybrid RAG (Text + CSV)?

Real enterprise systems must answer both:

Semantic questions (policies, documentation, knowledge bases)

Analytical questions (metrics, KPIs, incidents)

This project routes queries intelligently to:

FAISS-based semantic retrieval for unstructured text

Pandas-based computation for structured CSV data

3️⃣ Why Reranking?

FAISS optimizes for speed, not perfect accuracy.

A cross-encoder reranker is applied after retrieval to:

Improve precision

Reduce irrelevant context

Reflect enterprise RAG best practices

4️⃣ Why Ollama for Generation?

LLM generation is intentionally optional and modular.

Ollama is used because:

Fully local (no API keys or quotas)

Supports multiple open models

Easy to swap or disable

If generation fails, the system still returns retrieved context, confidence, and sources.

📊 Retrieval Evaluation

The project includes offline evaluation using:

Precision@K

Recall@K

This enables:

Measuring retrieval quality

Validating reranking improvements

Data-driven iteration

🚀 FastAPI Service

The RAG system is deployed as a FastAPI service.

Start the API
uvicorn src.api:app --reload

Swagger UI
http://127.0.0.1:8000/docs

Example Request
{
  "question": "How does security apply to machine learning systems?"
}

Example Response
{
  "answer": "Security applies to machine learning systems by enforcing access control...",
  "confidence": "High (0.82)",
  "sources": ["security_ml.txt", "ml_platform.txt"],
  "route": "semantic"
}

🧪 Running Locally (CLI)
python -m src.rag_pipeline

🛠️ Installation
pip install -r requirements.txt


If generation is enabled, ensure Ollama is running:

ollama serve

⚠️ Notes on Generation

Local LLM generation may time out depending on model size and hardware

Retrieval, confidence scoring, and citations work independently of generation

This behavior is intentional and production-safe

✅ What This Project Demonstrates

End-to-end RAG system design

FAISS vector database usage

Hybrid structured + unstructured querying

Cross-encoder reranking

Retrieval evaluation metrics

Production-safe error handling

FastAPI deployment

Modular, extensible architecture

🔮 Future Enhancements

Streaming responses

Dockerized deployment

Authentication & rate limiting

UI frontend

Multiple vector backends

👤 Author

Built as a learning and portfolio project to demonstrate real-world Retrieval-Augmented Generation system design and backend deployment practices.