import streamlit as st
from config.config_loader import insights_cfg
from utils import visualize_grade

height_insight = int(insights_cfg['height_insight'])


@st.dialog("Manually Grade Candidate")
def manually_enter_grade():
    st.write(f"Current Grade: {st.session_state.get('grade', '')} / 5")
    # Visualize using colours 🟢⚪
    st.write(visualize_grade(st.session_state.grade))
    valid_grades = ["1", "2", "3", "4", "5"]
    new_grade = st.text_input("Enter new grade:")

    if st.button("Set Grade"):
        if new_grade in valid_grades:
            st.session_state.grade = new_grade
            st.switch_page("applicants.py")
        else:
            st.error("Grade must be one of '1', '2', '3', '4', or '5'.")


# Candidate container
with st.container():
    back_column, title_column = st.columns([1, 5])
    with back_column:
        st.write("")  # Blank to get linebreak
        if st.button("Back", use_container_width=True):
            st.switch_page("applicants.py")
    with title_column:
        st.title(f"Candidate: :blue[{st.session_state.applicant_name}], Score: :green[{st.session_state.grade}/5]")

# Grade visualization
_, middle, _ = st.columns([1, 1, 1])  # This is just used to get the visualization to the middle
with middle:
    # Visualize using colours 🟢⚪
    st.title(visualize_grade(st.session_state.grade))

# Insights, i.e. matching/not matching qualifications and reasoning for the AI-grade
matching_column, not_matching_column, reasoning_column = st.columns([1, 1, 2])

with matching_column:
    st.header("Matching")
    with st.container(border=True, height=height_insight):
        st.write(st.session_state.matching)

with not_matching_column:
    st.header("Not Matching")
    with st.container(border=True, height=height_insight):
        st.write(st.session_state.not_matching)

with reasoning_column:
    st.header("Reasoning")
    with st.container(border=True, height=height_insight):
        st.write(st.session_state.reasoning)

# Validate or manually grade
validate_column, manual_column, _ = st.columns([1, 1, 2])

with validate_column:
    # If user press "Validate Grade", then the st.session_state.grade stays the same
    if st.button("Validate Grade"):
        st.switch_page("applicants.py")

with manual_column:
    # If user press "Manually Grade", then we look to change st.session_state.grade
    if st.button("Manually Grade"):
        # Popup window where user can enter grade, if successful -> st.switch_page(applicants)
        manually_enter_grade()
