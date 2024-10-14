import streamlit as st
import requests
import pandas as pd
from db.db import get_db
from db.repositories import CVJobRepository
from sqlalchemy.orm import Session
from ui.gui import API_URL

# Gets db-session
db: Session = next(get_db())
repository = CVJobRepository(db)


# Function to get and update from db
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

st.session_state.df = get_table_data()

# RIGHT COLUMN - For uploading the CV
uploaded_profile = st.file_uploader("Upload Requirement Profile", type=["pdf", "docx", "txt"])
if uploaded_profile is not None:
    # Send the uploaded file to the backend to store it in the database
    with st.spinner("Uploading profile..."):
        files = {"profile": (uploaded_profile.name, uploaded_profile, uploaded_profile.type)}
        response = requests.post(f"{API_URL}/upload/job_profile/", files=files)

    if response.status_code == 200:
        data = response.json()
        entry_id = data.get("entry_id")
        st.toast("Requirement profile uploaded!")

        # Store the entry_id in session_state for use when uploading a CV
        st.session_state["entry_id"] = entry_id
        st.session_state["requirement_profile"] = uploaded_profile
    else:
        st.error("Something went wrong while uploading the profile.")
uploaded_cv = st.file_uploader("Upload CV", type=['pdf', 'docx', 'txt'])
if uploaded_cv is not None:
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
            st.toast("CV uploaded!")
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
    #if "cv_uploaded" in st.session_state and st.session_state["cv_uploaded"]:
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
        #st.error("Upload CV first.")
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

    # Check if user has marked a post
    #if selected_rows['Select'].any():  # Kolla om någon rad är markerad
        #selected_indices = selected_rows[selected_rows['Select']].index  # Få index för valda rader
        #if len(selected_indices) > 0:
            #selected_entry_id = df.loc[selected_indices[0], "ID"]  # Ta ID från första markerade raden
            #st.session_state["entry_id"] = selected_entry_id
else:
    st.info("No data available yet. Please upload a requirement profile or a CV.")
