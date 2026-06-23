


# from langsmith import traceable
# import time


# @traceable(name="user_pipeline", metadata={"version":"1.0", "team":"Avon"}, tags=["production", "baggage"])
# def response_llm(query):
#     return "baggage policy is 23 kgs"


# if __name__ == "__main__":
#     response_llm("What is baggage policy?")
#     time.sleep(2)



from langsmith import traceable
import time


@traceable(name = "Nipun's test", tags = ["ai", "prod", "llm" ,"agentic"], metadata={"env":"prod","contract":"AsycnAPI","version":"v1"})
def response_llm(query):
    result = "Baggage is 23 kgs"
    return result

if __name__ == "__main__":
    response_llm("What is the baggage policy?")
    time.sleep(2)