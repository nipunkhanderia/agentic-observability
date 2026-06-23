import time
import numpy as np
import phoenix as px
from phoenix.otel import register
from opentelemetry import trace

# Launch Phoenix
session = px.launch_app()
print(f"Phoenix running at: {session.url}")

# Register tracer
tracer_provider = register(project_name="embedding_demo")
tracer = tracer_provider.get_tracer(__name__)

# Sample documents in different categories
documents = [
    # Baggage related
    "What is the baggage allowance for economy class?",
    "Can I carry extra luggage on international flights?",
    "How much does checked baggage cost?",
    "What are the dimensions allowed for carry-on bags?",
    "Is there a weight limit for hand luggage?",
    # Flight booking related
    "How do I book a round trip ticket?",
    "Can I change my flight date after booking?",
    "What is the cancellation policy for tickets?",
    "How to get a refund on cancelled flights?",
    "Can I upgrade my seat after purchase?",
    # Food and meals
    "What meals are served on long haul flights?",
    "Can I request a vegetarian meal?",
    "Is food included in economy tickets?",
    "Do you serve halal food options?",
    "Can I bring my own food on the plane?",
]

categories = ["baggage"] * 5 + ["booking"] * 5 + ["food"] * 5

# Generate fake clustered embeddings
np.random.seed(42)
cluster_centers = {
    "baggage": np.random.normal(loc=[1, 0, 0, 0.5, 0.2], scale=0.01, size=5),
    "booking": np.random.normal(loc=[0, 1, 0, 0.3, 0.8], scale=0.01, size=5),
    "food": np.random.normal(loc=[0, 0, 1, 0.7, 0.1], scale=0.01, size=5),
}


def fake_embed(text: str, category: str) -> list[float]:
    emb = cluster_centers[category] + np.random.normal(0, 0.15, size=5)
    return emb.tolist()


# Log each document as a retriever span with embeddings
for doc, cat in zip(documents, categories):
    with tracer.start_as_current_span("embedding_lookup") as span:
        embedding = fake_embed(doc, cat)
        span.set_attribute("input.value", doc)
        span.set_attribute("metadata.category", cat)
        span.set_attribute("embedding.model_name", "fake-model-v1")
        span.set_attribute("embedding.embeddings.0.embedding.text", doc)
        span.set_attribute("embedding.embeddings.0.embedding.vector", embedding)
        span.set_attribute("openinference.span.kind", "EMBEDDING")

print(f"\nLogged {len(documents)} embedding spans to Phoenix.")
print(f"Open {session.url} to visualize.")
print("Press Ctrl+C to stop.\n")

time.sleep(3)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down.")
