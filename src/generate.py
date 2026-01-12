import google.genai as genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_answer(question, contexts):
    """
    question: str
    contexts: list of retrieved chunks (dicts with 'text')
    """

    # Combine retrieved text into one context block
    context_text = "\n\n".join([c["text"] for c in contexts])

    prompt = f"""
Answer the question using ONLY the context below.
If the answer is not present in the context, say "I don't know".

Context:
{context_text}

Question:
{question}
"""

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-pro",
            contents=[prompt]
        )
        return response.text

    except Exception as e:
        return f"[Generation skipped: {str(e)}]"
