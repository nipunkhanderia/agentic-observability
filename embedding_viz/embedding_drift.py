import numpy as np
import pandas as pd
import phoenix as px
from openai import OpenAI

client = OpenAI()  # Needs OPENAI_API_KEY env var


def get_embeddings(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(
        input=texts,
        model="text-embedding-3-small",
    )
    return [item.embedding for item in response.data]


# Two sets of documents to compare drift
production_docs = [
    "What is the baggage allowance?",
    "How to book a flight?",
    "Can I get a refund?",
    "What meals are available?",
    "How to upgrade my seat?",
    "Is Wi-Fi available on flights?",
    "What is the check-in time?",
    "Can I select my seat?",
    "How to add extra baggage?",
    "What documents do I need to travel?",
]

new_docs = [
    "What is the pet travel policy?",
    "Can I bring my dog on the plane?",
    "How much does pet cargo cost?",
    "Are emotional support animals allowed?",
    "What vaccines does my pet need to fly?",
    "Can I fly with a cat in cabin?",
    "What size pet carrier is allowed?",
    "Do you have pet-friendly destinations?",
    "Is there a quarantine for pets?",
    "How to book pet travel?",
]

print("Generating embeddings for production docs...")
prod_embeddings = get_embeddings(production_docs)

print("Generating embeddings for new docs...")
new_embeddings = get_embeddings(new_docs)

# Production dataset
prod_df = pd.DataFrame({
    "text": production_docs,
    "category": ["general"] * len(production_docs),
})
prod_df["embedding"] = prod_embeddings

# New/drifted dataset
new_df = pd.DataFrame({
    "text": new_docs,
    "category": ["pet_travel"] * len(new_docs),
})
new_df["embedding"] = new_embeddings

schema = px.Schema(
    prompt_column_names=px.EmbeddingColumnNames(
        vector_column_name="embedding",
        raw_data_column_name="text",
    ),
)

# Launch with primary (production) and reference (new) to see drift
session = px.launch_app(
    primary=px.Inferences(prod_df, schema, name="production"),
    reference=px.Inferences(new_df, schema, name="new_queries"),
)

print(f"\nPhoenix is running at: {session.url}")
print("You can now see embedding drift between production and new queries.")
print("Press Ctrl+C to stop.\n")

import time
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down Phoenix.")
