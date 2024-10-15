import pandas as pd
from db.repositories import CVJobRepository
from db.db import get_db
from sqlalchemy.orm import Session
from config.config_loader import api_cfg, colors_cfg

# Gets db-session
db: Session = next(get_db())
repository = CVJobRepository(db)

# Data from config
API_URL = api_cfg['api_url']
red, blue, green, yellow = colors_cfg['red'], colors_cfg['blue'], colors_cfg['green'], colors_cfg['yellow']


def get_feedback(score):
    feedback = {"1": "Bad!", "2": "Subpar!", "3": "Average!", "4": "Good!", "5": "Excellent!"}
    return feedback.get(score, "Invalid input")


def visualize_grade(grade):
    return "🟢" * int(grade) + "⚪" * (5 - int(grade))


def set_status_color(status):
    # Colors picked from https://davidmathlogic.com/colorblind to ensure accessibility for colorblind
    color_map = {
        'Pending': red,
        'AI-Graded': yellow,
        'Manually Graded': green,
        'Validated': green
    }
    return f"color: {color_map.get(str(status), 'white')}"


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
