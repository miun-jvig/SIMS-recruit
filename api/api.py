# Temporary function just to describe for Måns what kind of data he should work with, i.e. a dict with two inputs

from fastapi import FastAPI

app = FastAPI()

@app.post("/llm_process/")
async def process_cv_and_profile(data: dict):
    # Simulate processsing the input using LLM
    cv_content = data['messages'][0][1]
    profile_content = data['messages'][1][1]


    # Simulate LLM logic ex. scoring and reasoning
    numerical_score = 2
    reasoning = "temp reasoning"

    return {"numerical_score": numerical_score, "reasoning": reasoning}


# To run this service
# uvicorn api:app --host 0.0.0.0 --port 8001

    #def temp_api():
    #dict_temp = {
     #   "numerical_score": 2,
      #  "reasoning": "temporary reasoning"
    #}
