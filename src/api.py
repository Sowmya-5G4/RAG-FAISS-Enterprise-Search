from fastapi import FastAPI
from pydantic import BaseModel

from src.router import classify_query
from src.retrieve_faiss import retrieve
from src.rerank import rerank
from src.generate_ollama import generate_answer
from src.structured_qa import answer_structured_query
from src.rag_pipeline import normalize_query


app = FastAPI(title="RAG-FAISS-Enterprise-Search")

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    confidence: str | None = None
    sources: list[str] | None = None
    route: str

@app.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    query = request.question
    normalized_query = normalize_query(query)
    route = classify_query(normalized_query)

    # Structured path
    if route == "structured":
        answer = answer_structured_query(normalized_query)
        return QueryResponse(
            answer=answer,
            route="structured"
        )

    # Semantic path
    results = retrieve(normalized_query, top_k=10)
    results = rerank(normalized_query, results, top_k=3)

    answer = generate_answer(normalized_query, results)

    confidence_score = max(r["score"] for r in results)
    if confidence_score >= 0.75:
        confidence = "High"
    elif confidence_score >= 0.5:
        confidence = "Medium"
    else:
        confidence = "Low"

    sources = sorted(set(r["source"] for r in results))

    return QueryResponse(
        answer=answer,
        confidence=f"{confidence} ({confidence_score:.2f})",
        sources=sources,
        route="semantic"
    )

@app.get("/")
def health():
    return {"status": "RAG API is running"}
