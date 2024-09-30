from fastapi import FastAPI
from graphs.graph import process_graph
from processing.result_parser import parse_results

app = FastAPI()

@app.post("/llm_process/")
async def process_cv_and_profile(data: dict):
    # Extract the CV and requirement profile from the request
    cv_content = data['messages'][0][1]
    profile_content = data['messages'][1][1]

    # State for processing
    state = {
        "messages": [
            ("user", cv_content),
            ("user", profile_content),
        ]
    }

    # Process the CV and profile
    result = process_graph(state)

    # Parse the results
    parsed_result = parse_results(result)


    return parsed_result
