from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
import time

# Set up tracer with basic service name
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({"service.name": "otel-curl-test"})
    )
)
tracer = trace.get_tracer(__name__)

# Configure the OTLP HTTP exporter
otlp_exporter = OTLPSpanExporter(endpoint="http://otel-opentelemetry-collector:4318/v1/traces")

# Add the exporter to the span processor
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

# Generate a test trace
with tracer.start_as_current_span("curl-test-span") as span:
    span.set_attribute("test.attribute", "value")
    span.add_event("test event")
    print("Trace sent!")
    time.sleep(2)  # Give time for batch processor to export
