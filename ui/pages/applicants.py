import streamlit as st
import requests

# Create columns for buttons and file uploader
grade_analyze_column, upload_column = st.columns([2, 1])

# This is needed as we have to save the profile from page recruitment.py to this page (applicants.py)
uploaded_profile = st.session_state.processed_text

# COLUMN 1
with grade_analyze_column:
    AI_grade_column, analyze_column = st.columns([1, 1])

    # When pressing "AI-Grade Selected"
    if AI_grade_column.button("AI-Grade Selected"):
        # Files to [FastAPI]
        files = {
            'cv': (uploaded_cv.name, uploaded_cv, uploaded_cv.type),
            'profile': (uploaded_profile.name, uploaded_profile, uploaded_profile.type),
        }
        # Send files to FastAPI (FastAPI = middleman)
        # Check link: https://www.w3schools.com/python/module_requests.asp
        try:
            response = requests.post("http://localhost:8000/analyze/", files=files)
            # Check if -> Success
            if response.status_code == 200:
                result = response.json()
                grade = result.get('ai_grade')
                insights = result.get('insights')
                st.write(f"AI betyg: {grade}")
                st.write(f"AI insikter: {insights}")
            else:
                st.error("Fel i analysen (på backendsidan)")
        except requests.exceptions.RequestException as e:
            st.error(f"Fel vid anslutning till API: {e}")

    # When pressing "Analyze Selected"
    if analyze_column.button("Analyze Selected"):
        st.switch_page("pages/insights.py")

# COLUMN 2
with upload_column:
    uploaded_cv = st.file_uploader("Upload CV", type=['pdf', 'docx'], accept_multiple_files=True)

