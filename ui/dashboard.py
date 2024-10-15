import streamlit as st
from sqlalchemy.orm import Session

from db.db import get_db
from db.repositories import CVJobRepository

API_URL = "http://localhost:8000"

# Gets db-session
db: Session = next(get_db())
repository = CVJobRepository(db)

with open("ui/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

pending_counter = repository.get_pending_count()

# Display the counter
st.markdown(f"""
    <div class="pending-applicants-container">
        <div class="pending-applicants-label">Pending Applicants</div>
        <div class="pending-applicants-value">{pending_counter}</div>
    </div>
""", unsafe_allow_html=True)
