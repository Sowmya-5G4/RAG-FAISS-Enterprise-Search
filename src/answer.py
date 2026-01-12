import google.genai as genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

context = """
Retrieval Augmented Generation (RAG) combines search with large language models.
"""

question = "What is RAG?"

prompt = f"""
Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}
"""

response = client.models.generate_content(
    model="models/gemini-2.0-flash-lite",   # ✅ model exists
    contents=[prompt]               # ✅ MUST be a list
)

print(response.text)
