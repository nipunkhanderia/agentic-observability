"""Test with Arize's documented OTLP format."""
import os
import time
from phoenix.otel import register

API_KEY = os.environ.get("ARIZE_API_KEY")
SPACE_ID = os.environ.get("ARIZE_SPACE_ID")

if not API_KEY or not SPACE_ID:
    raise ValueError("Set ARIZE_API_KEY and ARIZE_SPACE_ID environment variables")

# Try different endpoint formats Arize might expect
tracer_provider = register(
    project_name="embedding-demo",
    endpoint="https://otlp.arize.com/v1",
    headers={
        "space_id": SPACE_ID,
        "api_key": API_KEY,
    },
    protocol="http/protobuf",
    batch=True,
)
tracer = tracer_provider.get_tracer(__name__)

# Simple test span
with tracer.start_as_current_span("test_span") as span:
    span.set_attribute("openinference.span.kind", "CHAIN")
    span.set_attribute("input.value", "hello arize")
    span.set_attribute("output.value", "world")

print("Span sent. Flushing...")
time.sleep(2)
tracer_provider.force_flush()
time.sleep(3)
print("Done. Check Arize dashboard.")
