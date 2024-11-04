# SIMS-recruit

## System Requirements
To run this project, you need the following software and tools installed:

- Pip: To install Python packages
- Python 3.9 or higher: Required to run the backend and the Streamlit frontend.
- SQLite: Used as the database for storing CVs and job profiles.
- Ollama: Required for LLM-based processing.
- LangChain: To facilitate interaction between LLMs and other components.
- FastAPI: The backend API to connect frontend and backend.
- Streamlit: The frontend for the user interface.
- Uvicorn: ASGI server to run FastAPI.

## Running the Application
After completing the installations, cloning the project and setting up the database, run the application with the following commands:

- python -m uvicorn api.api:app --reload
- python -m streamlit run ui/gui.py
- python -m uvicorn api.api:app --host 0.0.0.0 --port 8001 --reload

## Usage
- Upload Job Profile: Use the "Upload Requirement Profile" button to upload job profiles.
- Upload CV: Use the "Upload CV" button to upload CVs to match against a job profile.
- Analyze CV: After uploading, use the AI grading button to analyze the CV against the job profile.
- Manual Grading: You can also manually grade a CV and validate the analysis.