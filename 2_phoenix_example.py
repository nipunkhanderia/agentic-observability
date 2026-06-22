"""
ARIZE PHOENIX EXAMPLE - Simplest possible tracing
----------------------------------------------------
What this does: starts a local Phoenix server (a dashboard that runs
on YOUR computer, no account needed) and traces a function to it.

SETUP: nothing needed in advance! Phoenix runs locally.
Just run this file directly: python 2_phoenix_example.py
"""

import phoenix as px
from openinference.instrumentation import using_attributes
from opentelemetry import trace
from phoenix.otel import register

# Step 1: launch the Phoenix dashboard (opens a local web server)
px.launch_app()

# Step 2: register Phoenix as the place traces get sent
tracer_provider = register(project_name="fake-rag-demo")
tracer = tracer_provider.get_tracer(__name__)


# This fake function pretends to do RAG (retrieve + answer).
# @tracer.start_as_current_span(...) is Phoenix's way of saying
# "log this function call as one traced step"
def answer_question(question: str) -> str:
    with tracer.start_as_current_span("fake_rag_pipeline") as span:
        # Step 1: pretend to "retrieve" some context
        fake_context = "London is the capital of the United Kingdom."

        # Step 2: pretend to "ask the LLM" using that context
        fake_answer = f"Based on the context, the answer is: {fake_context}"

        # Attach extra info to the trace so you can see it in the dashboard
        span.set_attribute("input.value", question)
        span.set_attribute("output.value", fake_answer)

        return fake_answer


if __name__ == "__main__":
    question = "What is the capital of the UK?"
    result = answer_question(question)
    print("Answer:", result)
    print("\nPhoenix dashboard should have opened in your browser.")
    print("If not, go to: http://localhost:6006")
    print("Keep this script running for a bit so you can see the trace!")

    # Keep the script alive so the dashboard stays up to look at
    input("\nPress Enter to exit...")
