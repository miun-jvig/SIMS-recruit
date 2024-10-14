import pandas as pd
from db.repositories import CVJobRepository
from db.db import get_db
from sqlalchemy.orm import Session

# Gets db-session
db: Session = next(get_db())
repository = CVJobRepository(db)
# Initialize API_URL
API_URL = "http://localhost:8000"


def get_feedback(score):
    feedback = {"1": "Bad!", "2": "Subpar!", "3": "Average!", "4": "Good!", "5": "Excellent!"}
    return feedback.get(score, "Invalid input")


def visualize_grade(grade):
    return "🟢" * int(grade) + "⚪" * (5 - int(grade))


def get_table_data():
    all_entries = repository.get_all_entries()
    if all_entries:
        df = pd.DataFrame([{
            "ID": entry.id,
            "Job Profile": entry.job_filename,
            "CV": entry.cv_filename,
            "Upload Date": entry.created_at,
            "Grade": entry.grade,
            "Status": entry.status
        } for entry in all_entries])
        return df
    else:
        return pd.DataFrame()
