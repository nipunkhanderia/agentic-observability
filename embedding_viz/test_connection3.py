"""Test using Arize's standard env-variable based setup."""
import os

# Set these before importing anything else
os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "https://otlp.arize.com"
os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"space_id={os.environ.get('ARIZE_SPACE_ID')},api_key={os.environ.get('ARIZE_API_KEY')}"

import time
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

resource = Resource.create({"project.name": "embedding-demo"})

provider = TracerProvider(resource=resource)
exporter = OTLPSpanExporter()
provider.add_span_processor(BatchSpanProcessor(exporter))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("test_span") as span:
    span.set_attribute("openinference.span.kind", "CHAIN")
    span.set_attribute("input.value", "hello from python")
    span.set_attribute("output.value", "test response")

print("Span sent. Flushing...")
provider.force_flush()
time.sleep(3)
print("Done. Check Arize dashboard.")
