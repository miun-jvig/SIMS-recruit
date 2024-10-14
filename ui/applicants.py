import streamlit as st
import requests
from db.repositories import CVJobRepository
from db.db import get_db
from sqlalchemy.orm import Session
from ui.utils import get_table_data
from config.config_loader import api_cfg

# Data from config
API_URL = api_cfg['api_url']

# Gets db-session
db: Session = next(get_db())
repository = CVJobRepository(db)

# Initialize table
st.session_state.df = get_table_data()

# Two columns, one for uploading profile, and one for uploading CV
upload_profile_col, upload_cv_col = st.columns([1, 1])

with upload_profile_col:
    uploaded_profile = st.file_uploader("Upload Requirement Profile", type=["txt"])

    if uploaded_profile is not None and (st.session_state["requirement_profile"] is None or
                                         st.session_state["requirement_profile"] != uploaded_profile):
        st.session_state["requirement_profile"] = uploaded_profile
        # Send the uploaded file to the backend to store it in the database
        with st.spinner("Uploading profile..."):
            files = {"profile": (uploaded_profile.name, uploaded_profile, uploaded_profile.type)}
            response = requests.post(f"{API_URL}/upload/job_profile/", files=files)

        if response.status_code == 200:
            data = response.json()
            st.session_state["entry_id"] = data.get("entry_id")
            # Update dataframe in session_state
            st.session_state.df = get_table_data()
        else:
            st.error("Something went wrong while uploading the profile.")


with upload_cv_col:
    uploaded_cv = st.file_uploader("Upload CV", type=['txt'])

    if uploaded_cv is not None and (st.session_state["cv"] is None or st.session_state["cv"] != uploaded_cv):
        st.session_state["cv"] = uploaded_cv
        # Check if entry_id exist before upload of cv
        if 'entry_id' not in st.session_state:
            st.warning("Please upload a requirement profile before uploading a CV.")
        else:
            # Save the applicant name to session state
            st.session_state.applicant_name = uploaded_cv.name

            # Display a spinner while uploading the CV to the backend
            with st.spinner("Laddar upp CV..."):
                # Prepare the file to send to the backend
                files = {"cv": (uploaded_cv.name, uploaded_cv, uploaded_cv.type)}

                # Make a post request to upload the CV and link it to the job profile using the entry_id
                response = requests.post(f"{API_URL}/upload/cv/", params={"entry_id": st.session_state["entry_id"]},
                                         files=files)

            if response.status_code == 200:
                # Update the session state to indicate CV was uploaded
                st.session_state["cv_uploaded"] = True

                # Update dataframe in session_state
                st.session_state.df = get_table_data()
            else:
                st.error("Något gick fel vid uppladdningen av CV:t.")

# LEFT COLUMN - For grading and analyzing the CV
AI_grade_column, analyze_column = st.columns([1, 1])

# When pressing "AI-Grade Selected"
if AI_grade_column.button("AI-Grade Selected"):
    # Ensure the CV has been uploaded before proceeding with the AI analysis
    if "entry_id" in st.session_state:
        with st.spinner("Analyserar med AI..."):
            # Make a POST request to trigger the analysis process on the backend
            response = requests.post(f"{API_URL}/analyze/{st.session_state['entry_id']}")

        if response.status_code == 200:
            result = response.json()
            st.session_state.update({
                "grade": result.get("ai_grade"),
                "reasoning": result.get("insights"),
                "matching": result.get("matching"),
                "not_matching": result.get("not_matching")
            })

            # Update the database with the analysis results
            repository.update_grade_and_insights(st.session_state["entry_id"], result['ai_grade'], result['insights'])
            repository.update_matching_details(st.session_state["entry_id"], result['matching'], result['not_matching'])
            db.commit()

            # Update df in session_state
            st.session_state.df = get_table_data()
            st.toast("AI-grade done!")
        else:
            st.error("Something went wrong with AI-analyze.")
    else:
        st.error("Please select a row from the table to analyze.")

# When pressing "Analyze Selected"
if analyze_column.button("Analyze Selected"):
    if "grade" in st.session_state:
        st.switch_page("insights.py")
    else:
        st.error("The post must be AI graded before manually analyzing.")

# Show updated table
df = st.session_state.df

if not df.empty:
    # A column with selectable checkboxes
    df['Select'] = False
    selected_rows = st.data_editor(df, use_container_width=True,
                                   disabled=("ID", "Job Profile", "CV", "Grade", "Status"), hide_index=True)
    # User can only mark one post
    if selected_rows['Select'].sum() > 1:
        st.error("You can only select one row at a time.")
    elif selected_rows['Select'].sum() == 1:
        selected_index = selected_rows[selected_rows['Select']].index[0]
        selected_entry_id = df.loc[selected_index, "ID"]
        st.session_state["entry_id"] = selected_entry_id
else:
    st.info("No data available yet. Please upload a requirement profile or a CV.")