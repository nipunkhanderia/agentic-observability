"""Minimal test to verify Arize Cloud connection."""
import os
import time
from phoenix.otel import register

API_KEY = os.environ.get("ARIZE_API_KEY")
SPACE_ID = os.environ.get("ARIZE_SPACE_ID")

if not API_KEY or not SPACE_ID:
    raise ValueError("Set ARIZE_API_KEY and ARIZE_SPACE_ID environment variables")

# Try the endpoint without /traces suffix — phoenix register adds it automatically
tracer_provider = register(
    project_name="connection-test",
    endpoint="https://otlp.arize.com",
    headers={
        "space_id": SPACE_ID,
        "api_key": API_KEY,
    },
    batch=True,
)
tracer = tracer_provider.get_tracer(__name__)

# Simplest possible span — no embeddings
with tracer.start_as_current_span("hello_arize") as span:
    span.set_attribute("input.value", "test input")
    span.set_attribute("output.value", "test output")
    span.set_attribute("openinference.span.kind", "CHAIN")

print("Sent a simple span. Waiting for flush...")
time.sleep(2)
tracer_provider.force_flush()
print("Done. Check https://app.arize.com for 'connection-test' project.")
