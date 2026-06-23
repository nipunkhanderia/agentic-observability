
import phoenix as px
from phoenix.otel import register

# phoenix.launch_app()
px.launch_app()
tracer_name = register(project_name="Nipun's demo")
tracer = tracer_name.get_tracer(__name__)






def response_llm(qury):
    with tracer.start_as_current_span("nipun span") as span:
            
        result = "Baggage is 23 kgs"
        span.set_attribute("input.value", qury)
        span.set_attribute("output.value",result)
        span.set_attribute("metadata.category", "baggage")
        span.set_attribute("metadata.category", "baggage")
        span.set_attribute("metadata.priority", "high")
        span.set_attribute("metadata.feedback_score", 0.9)
        return result
    

if __name__ == "__main__":
    response_llm("What is the baggage policy?")
    print("Arize phoenix triggered")


