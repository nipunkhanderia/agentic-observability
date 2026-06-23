


from langsmith import traceable
import time


@traceable(name="user_pipeline", metadata={"version":"1.0", "team":"Avon"}, tags=["production", "baggage"])
def response_llm(query):
    return "baggage policy is 23 kgs"


if __name__ == "__main__":
    response_llm("What is baggage policy?")
    time.sleep(2)