"""
LANGSMITH EXAMPLE - Simplest possible tracing
-----------------------------------------------
What this does: wraps a function with @traceable so every call
gets logged to LangSmith's dashboard automatically.

SETUP (do this in your terminal/PowerShell BEFORE running this file):
    set LANGSMITH_API_KEY=lsv2_your_key_here
    set LANGSMITH_TRACING=true

(On Windows PowerShell use: $env:LANGSMITH_API_KEY="lsv2_..."  )
"""

from langsmith import traceable

# This fake function pretends to do RAG (retrieve + answer).
# In your real project, this would call FAISS + Groq.
@traceable(name="fake_rag_pipeline")  # <-- this one line is all LangSmith needs
def answer_question(question: str) -> str:
    # Step 1: pretend to "retrieve" some context
    fake_context = "London is the capital of the United Kingdom."

    # Step 2: pretend to "ask the LLM" using that context
    fake_answer = f"Based on the context, the answer is: {fake_context}"

    return fake_answer


if __name__ == "__main__":
    question = "What is the capital of the UK?"
    result = answer_question(question)
    print("Answer:", result)
    print("\nNow go check https://smith.langchain.com -> Projects -> default")
    print("You should see a trace named 'fake_rag_pipeline'")
