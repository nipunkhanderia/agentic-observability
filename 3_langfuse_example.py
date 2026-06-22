"""
LANGFUSE EXAMPLE - Simplest possible tracing
-----------------------------------------------
This is the SAME fake function, traced with Langfuse instead,
so you can compare all 3 side by side.

SETUP (you likely already have these from your rag-eval project):
    set LANGFUSE_PUBLIC_KEY=pk-lf-...
    set LANGFUSE_SECRET_KEY=sk-lf-...
    set LANGFUSE_HOST=https://cloud.langfuse.com
"""

from langfuse import observe

# @observe() is Langfuse's version of @traceable -- same idea,
# one decorator, automatic logging.
@observe(name="fake_rag_pipeline")
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
    print("\nNow go check https://cloud.langfuse.com -> Tracing")
    print("You should see a trace named 'fake_rag_pipeline'")
