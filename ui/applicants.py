import streamlit as st
from api.api import send_to_api
from utils import update_row


# Create columns for buttons and file uploader
grade_analyze_column, upload_column = st.columns([2, 1])

# This is needed as we have to save the profile from page recruitment.py to this page (applicants.py)
uploaded_profile = st.session_state.requirement_profile

# RIGHT COLUMN
with upload_column:
    uploaded_cv = st.file_uploader("Upload CV", type=['pdf', 'docx', 'txt'])
    if uploaded_cv is not None and uploaded_profile is not None:
        # Update the table
        update_row(uploaded_cv.name, uploaded_profile.name, "-", "Pending")

# LEFT COLUMN
with grade_analyze_column:
    AI_grade_column, analyze_column = st.columns([1, 1])

    # When pressing "AI-Grade Selected"
    if AI_grade_column.button("AI-Grade Selected"):
        if uploaded_cv is not None and uploaded_profile is not None:
            # Files to [FastAPI]
            files = {
                'cv': (uploaded_cv.name, uploaded_cv, uploaded_cv.type),
                'profile': (uploaded_profile.name, uploaded_profile, uploaded_profile.type),
            }

            # Send to API, receive AI grade, reasoning, matching and not_matching qualifications
            result = dict(zip(['grade', 'reasoning', 'matching', 'not_matching'], send_to_api(files)))
            # Update the session states for grade, reasoning, matching and not_matching
            st.session_state.update(result)

            # Update the table
            update_row(uploaded_cv.name, uploaded_profile.name, st.session_state.grade, "Graded")
        else:
            st.error("Please upload a requirement profile and CV.")

    # When pressing "Analyze Selected"
    if analyze_column.button("Analyze Selected"):
        if st.session_state.grade is not None:
            st.switch_page("insights.py")
        else:
            st.error("Please ensure that you analyze an AI-graded profile.")

# Create a table in the bottom of the page, can edit checkboxes
st.session_state.df = st.data_editor(st.session_state.df, use_container_width=True,
                                     disabled=("Name", "Date", "Role", "Grade", "Status"))
