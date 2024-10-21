import streamlit as st
from requests import Session
from config.config_loader import insights_cfg
from db.db import get_db
from db.repositories import CVJobRepository
from utils import visualize_grade, get_feedback

# Hämta databas-session
db: Session = next(get_db())
repository = CVJobRepository(db)

height_insight = int(insights_cfg['height_insight'])


@st.dialog("Manually Grade Candidate")
def manually_enter_grade():
    st.write(f"Current Grade: {grade} / 5")
    # Visualize using colours 🟢⚪
    st.write(visualize_grade(grade))
    valid_grades = ["1", "2", "3", "4", "5"]
    new_grade = st.text_input("Enter new grade:")

    if st.button("Set Grade"):
        if new_grade in valid_grades:
            #st.session_state.grade = new_grade
            #SKAPA EN NY UPDATE FUNKTION FÖR UPDATE GRADE I REPOS.py
            #repository.update_grade_and_insights(entry_id, int(new_grade), insights="")
            try:
                repository.update_grade(entry_id, new_grade)
                st.toast("Grade Updated!")
                st.session_state.grade = new_grade
                st.switch_page("applicants.py")
            except Exception as e:
                st.error(f"An error occured updating grade: {e}")
        else:
            st.error("Grade must be one of '1', '2', '3', '4', or '5'.")


# Fetch the candidate data from the database using the entry ID
if "entry_id" in st.session_state and st.session_state["entry_id"] is not None:
    try:
        # Ensure entry_id is an integer
        entry_id = int(st.session_state["entry_id"])

        # Fetch the candidate entry
        candidate_entry = repository.get_entry_by_id(entry_id)

        if candidate_entry:
            # Extract necessary fields
            cv_filename = candidate_entry.cv_filename
            grade = candidate_entry.grade
            matching = candidate_entry.matching
            not_matching = candidate_entry.not_matching
            reasoning = candidate_entry.insights
        else:
            st.error(f"Candidate data not found for Entry ID: {entry_id}")
            st.stop()
    except Exception as e:
        st.error(f"An error occurred while fetching candidate data: {e}")
        st.stop()
else:
    st.error("Please choose a candidate from 'Applicants'.")
    st.stop()

# Candidate container
with st.container():
    back_column, title_column, download_column = st.columns([1, 4, 1])
    with back_column:
        st.write("")  # Blank to get linebreak
        if st.button("Back", use_container_width=True):
            st.switch_page("applicants.py")
    with title_column:
        st.title(f"Candidate: :blue[{cv_filename}]")
    with download_column:
        # Use the actual CV content from the database for download
        if candidate_entry.cv_content:
            st.download_button(
                label="Download CV",
                data=candidate_entry.cv_content,
                file_name=cv_filename,
                mime="application/octet-stream"
            )
        else:
            st.error("No CV available for download.")


# Container for the grades
with st.container(border=True):
    score, color_visualization, text_visualization = st.columns([1, 1, 1])
    with score:
        st.title(f"Score: :green[{grade}/5]")
    with color_visualization:
        # Visualize grade using colours 🟢⚪
        st.title(visualize_grade(grade))
    #with text_visualization:
        # Visualize grade using text
       # st.title(get_feedback(grade))

# Insights, i.e. matching/not matching qualifications and reasoning for the AI-grade
matching_col, not_matching_col, reasoning_col = st.columns([1, 1, 2])
with matching_col:
    st.header("Matching")
    with st.container(border=True, height=height_insight):
        st.write(matching)
with not_matching_col:
    st.header("Not Matching")
    with st.container(border=True, height=height_insight):
        st.write(not_matching)
with reasoning_col:
    st.header("Reasoning")
    with st.container(border=True, height=height_insight):
        st.write(reasoning)

# Validate or manually grade
validate_column, manual_column, _ = st.columns([1, 1, 2])

with validate_column:
    # If user press "Validate Grade", then the st.session_state.grade stays the same
    if st.button("Validate Grade"):
        try:
            repository.validate_grade(entry_id)
            st.toast("Grade Validated!")
            st.switch_page("applicants.py")
        except Exception as e:
            st.error(f"An error occured validating grade: {e}")

with manual_column:
    # If user press "Manually Grade", then we look to change st.session_state.grade
    if st.button("Manually Grade"):
        # Popup window where user can enter grade, if successful -> st.switch_page(applicants)
        manually_enter_grade()
