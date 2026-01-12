import subprocess

def generate_answer(question, contexts):
    context_text = "\n\n".join([c["text"] for c in contexts])

    prompt = f"""
You are a helpful assistant.

Use the context below to answer the question.
Do NOT use outside knowledge.
If the context does not contain the answer, say "I don't know".

Context:
{context_text}

Question:
{question}
"""

    try:
        result = subprocess.run(
            ["ollama", "run", "llama3"],
            input=prompt.encode("utf-8"),   # ✅ FIX IS HERE
            capture_output=True,
            timeout=90
        )

        return result.stdout.decode("utf-8", errors="ignore").strip()

    except Exception as e:
        return f"[Ollama generation failed: {e}]"
