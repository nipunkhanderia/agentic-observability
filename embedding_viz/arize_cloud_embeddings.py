import os
import time
import numpy as np
from phoenix.otel import register

API_KEY = os.environ.get("ARIZE_API_KEY")
SPACE_ID = os.environ.get("ARIZE_SPACE_ID")

if not API_KEY or not SPACE_ID:
    raise ValueError("Set ARIZE_API_KEY and ARIZE_SPACE_ID environment variables")

tracer_provider = register(
    project_name="embedding-demo",
    endpoint="https://otlp.arize.com",
    headers={
        "space_id": SPACE_ID,
        "api_key": API_KEY,
    },
    batch=True,
)
tracer = tracer_provider.get_tracer(__name__)

# Documents in different categories
documents = [
    "What is the baggage allowance for economy class?",
    "Can I carry extra luggage on international flights?",
    "How much does checked baggage cost?",
    "What are the dimensions allowed for carry-on bags?",
    "Is there a weight limit for hand luggage?",
    "How do I book a round trip ticket?",
    "Can I change my flight date after booking?",
    "What is the cancellation policy for tickets?",
    "How to get a refund on cancelled flights?",
    "Can I upgrade my seat after purchase?",
    "What meals are served on long haul flights?",
    "Can I request a vegetarian meal?",
    "Is food included in economy tickets?",
    "Do you serve halal food options?",
    "Can I bring my own food on the plane?",
]

categories = ["baggage"] * 5 + ["booking"] * 5 + ["food"] * 5

# Generate clustered embeddings (10-dim to keep it small)
np.random.seed(42)
cluster_centers = {
    "baggage": np.array([1.0, 0.0, 0.0, 0.5, 0.2, 0.1, 0.8, 0.3, 0.0, 0.4]),
    "booking": np.array([0.0, 1.0, 0.0, 0.3, 0.8, 0.6, 0.1, 0.7, 0.2, 0.0]),
    "food": np.array([0.0, 0.0, 1.0, 0.7, 0.1, 0.4, 0.3, 0.0, 0.9, 0.5]),
}

print("Sending embedding spans to Arize Cloud...")

for i, (doc, cat) in enumerate(zip(documents, categories)):
    embedding = (cluster_centers[cat] + np.random.normal(0, 0.1, size=10)).tolist()

    with tracer.start_as_current_span("embedding_query") as span:
        span.set_attribute("openinference.span.kind", "EMBEDDING")
        span.set_attribute("input.value", doc)
        span.set_attribute("output.value", f"Response for: {doc}")
        span.set_attribute("metadata.category", cat)
        span.set_attribute("embedding.model_name", "fake-model-v1")
        span.set_attribute("embedding.embeddings.0.embedding.text", doc)
        # Use individual float attributes for the vector
        for j, val in enumerate(embedding):
            span.set_attribute(f"embedding.embeddings.0.embedding.vector.{j}", val)

    print(f"✓ [{cat}] {doc[:50]}...")

time.sleep(2)
tracer_provider.force_flush()
print("\nDone! Go to https://app.arize.com → embedding-demo project")
