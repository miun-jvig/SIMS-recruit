from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db.db import get_db
from db.repositories import CVJobRepository
import logging
import requests
from graphs.graph import process_graph
from processing.extract_from_pdf import extract_text_from_pdf
from processing.result_parser import parse_results

app = FastAPI()

# LOG settings
logging.basicConfig(level=logging.INFO)

# Handle CORS
origins = ["http://localhost:8501", "http://localhost:8000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Repository initialization (using dependency injection)
# This function injects the repository into API endpoints, handling interactions with the database.
def get_repository(db: Session = Depends(get_db)):
    return CVJobRepository(db)

# Endpoint to upload a job profile
@app.post("/upload/job_profile/")
async def upload_job_profile(profile: UploadFile = File(...), repository: CVJobRepository = Depends(get_repository)):
    # Read the uploaded job profile content
    profile_content = await profile.read()

    # Save the job profile to the database (no CV yet)
    db_entry = repository.add_cv_and_job(
        cv_filename="",
        cv_content=b"",
        job_filename=profile.filename,
        job_content=profile_content
    )
    return {"message": f"Job profile '{profile.filename}' uploaded successfully", "entry_id": db_entry.id}

# Endpoint to upload a CV
@app.post("/upload/cv/")
async def upload_cv(entry_id: int, cv: UploadFile = File(...), repository: CVJobRepository = Depends(get_repository)):
    # Read the uploaded CV content
    cv_content = await cv.read()

    # Retrieve the existing job profile entry
    db_entry = repository.get_entry_by_id(entry_id)
    if not db_entry:
        raise HTTPException(status_code=404, detail="Job profile not found")

    # Update the entry with the uploaded CV data
    db_entry.cv_filename = cv.filename
    db_entry.cv_content = cv_content
    #db_entry.status = "uploaded"
    repository.db.commit()
    repository.db.refresh(db_entry)

    # Return a success message and the entry ID
    return {"message": f"CV '{cv.filename}' uploaded successfully", "entry_id": db_entry.id}


@app.post("/llm_process/")
async def process_cv_and_profile(data: dict):
    # Extract the CV and requirement profile from the request
    cv_content = data['messages'][0][1]
    profile_content = data['messages'][1][1]

    # State for processing
    state = {
        "messages": [
            {"role": "user", "content": cv_content},
            {"role": "user", "content": profile_content}
        ]
    }

    # Process the CV and profile
    result = process_graph(state)

    # Parse the results
    parsed_result = parse_results(result)

    return parsed_result



# Endpoint to analyze the CV and job profile using an external LLM service
@app.post("/analyze/{entry_id}")
async def analyze_files(entry_id: int, repository: CVJobRepository = Depends(get_repository)):
    # Retrieve the CV-job profile pair from the database
    db_entry = repository.get_entry_by_id(entry_id)

    # If either the CV or job profile content is missing, return an error
    if not db_entry or not db_entry.cv_content or not db_entry.job_content:
        raise HTTPException(status_code=404, detail="Job profile or CV not found")

    job_text_content = ""
    if db_entry.job_filename.endswith(".pdf"):
        job_text_content = extract_text_from_pdf(db_entry.job_content)
    elif db_entry.job_filename.endswith(".txt"):
        job_text_content = db_entry.job_content.decode("utf-8")

    cv_text_content = ""
    if db_entry.cv_filename.endswith(".pdf"):
        cv_text_content = extract_text_from_pdf(db_entry.cv_content)
    elif db_entry.cv_filename.endswith(".txt"):
        cv_text_content = db_entry.cv_content.decode("utf-8")


    #test
    logging.info(f"Extracted job profile: {job_text_content}")
    logging.info(f"Extracted CV profile: {cv_text_content}")

    # Create the state (input) for the LLM process
    state = {
        "messages": [
            ("user", cv_text_content),
            ("user", job_text_content)
        ]
    }
    # Log the state being sent to the LLM for easier debugging
    # logging.info(f"Sending data to LLM for entry ID {entry_id}: {state}")

    # Send the state to the LLM microservice (running on localhost:8001)
    try:
        response = requests.post("http://localhost:8001/llm_process/", json=state)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred during LLM processing: {e}")
        raise HTTPException(status_code=500, detail="Unable to connect to LLM service")

    # Process the response
    if response.status_code == 200:
        result = response.json()
        # Update the database with the LLM analysis result (grade, insights, matching details)
        repository.update_grade_and_insights(entry_id, result.get("numerical_score"), result.get("reasoning"))
        repository.update_matching_details(entry_id, result.get("matching"), result.get("not_matching"))

        # Return the results back to the client
        return {
            "message": "Analysis completed and saved successfully",
            "ai_grade": result.get("numerical_score"),
            "insights": result.get("reasoning"),
            "matching": result.get("matching"),
            "not_matching": result.get("not_matching")
        }
    # If LLM response is unsuccessful, raise an error with the response code
    else:
        raise HTTPException(status_code=response.status_code, detail="Error occurred during LLM processing")
