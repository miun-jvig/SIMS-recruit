from fastapi import FastAPI, UploadFile, File
from starlette.middleware.cors import CORSMiddleware
from graphs.graph import process_graph
from processing.result_parser import parse_results
import streamlit as st
import logging
import requests

app = FastAPI()

# LOG settings (fastapi) -swagger ui
logging.basicConfig(level=logging.INFO)

# Handle CORS
# https://fastapi.tiangolo.com/tutorial/cors/#origin

# Port 8501 for streamlit, and 8000 for backend(I think)
origins = ["http://localhost:8501", "http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def send_to_api(files):
    # Send files to FastAPI (FastAPI = middleman)
    # Check link: https://www.w3schools.com/python/module_requests.asp
    try:
        response = requests.post("http://localhost:8000/analyze/", files=files)
        # Check if -> Success
        if response.status_code == 200:
            result = response.json()
            return result.get('ai_grade'), result.get('insights')
        else:
            st.error("Fel i analysen (på backendsidan)")
    except requests.exceptions.RequestException as e:
        st.error(f"Fel vid anslutning till API: {e}")


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


@app.post("/analyze/")
async def analyze_files(cv: UploadFile = File(...), profile: UploadFile = File(...)):
    cv_content = await cv.read()
    profile_content = await profile.read()

    # LOGGING filename and size so we know -> files handled correctly
    logging.info(f"CV mottaget: {cv.filename}, storlek: {len(cv_content)} bytes")
    logging.info(f"Kravprofil mottaget: {profile.filename}, storlek: {len(profile_content)} bytes")

    # Create the state (input) for the LLM process
    state = {
        "messages": [
            ("user", cv_content.decode("utf-8")),
            ("user", profile_content.decode("utf-8"))
        ]
    }

    # Call the LLMs "microservice" function to process the CV and job req.
    response = requests.post("http://localhost:8001/llm_process/", json=state)

    # Process the response
    if response.status_code == 200:
        result = response.json()
        return {
            "ai_grade": result["numerical_score"],
            "insights": result["reasoning"]
        }
    else:
        return {"error": "kan vara måns fel"}
