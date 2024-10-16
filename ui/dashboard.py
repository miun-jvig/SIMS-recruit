import streamlit as st
from sqlalchemy.orm import Session
from config.config_loader import api_cfg, colors_cfg
from db.db import get_db
from db.repositories import CVJobRepository
from ui.utils import set_status_color

API_URL = api_cfg['api_url']
red, blue, green, yellow = colors_cfg['red'], colors_cfg['blue'], colors_cfg['green'], colors_cfg['yellow']
profile_icon = "ui/profile_icon.png"


# Gets db-session
db: Session = next(get_db())
repository = CVJobRepository(db)

pending_counter = str(repository.get_status_count("Pending"))
db_entries = repository.get_all_entries()

pending_column, _, help_column = st.columns([1.5, 0.2, 1.5])
with pending_column:
    st.markdown("<br><br>", unsafe_allow_html=True)  # Adds 2 lines of vertical space
    with st.container(border=True):
        st.subheader(f'Pending Applications: &nbsp;&nbsp;&nbsp; :red[{pending_counter}]')

with help_column:
    st.subheader("📍 Info", divider="gray")
    st.markdown("""
        <p style="margin: 0;">1️⃣ Upload a job profile and CV in "Applicants"</p>
        <p style="margin: 0;">2️⃣ Use AI to grade the CV in "Applicants" with the button "AI-Grade Selected"</p>
        <p style="margin: 0;">3️⃣ Review and validate or adjust the grade in "Insights" with the button "Analyze Selected"</p>
        <p style="margin: 0;">✅ Done!</p>
    """, unsafe_allow_html=True)


applicants_header_column, status_header_column, _ = st.columns([1, 1, 2])
with applicants_header_column:
    st.header('Latest Applicants:')
with status_header_column:
    st.header("Status")

with st.container(border=True, height=350):
    for entry in db_entries:
        # Create two columns for each entry: one for the applicant and one for the status
        cols = st.columns([1, 1, 2])

        # Display applicant info in the first column
        if entry.cv_filename:
            with cols[0]:
                left_column = st.columns([0.2, 0.8])
                left_column[0].image(profile_icon, width=60)
                left_column[1].text("")
                left_column[1].text(entry.cv_filename)

            # Display status in the second column
            with cols[1]:
                status_color = set_status_color(entry.status)
                st.text("")
                st.markdown(f"<span style='{status_color}'>{entry.status}</span>", unsafe_allow_html=True)
