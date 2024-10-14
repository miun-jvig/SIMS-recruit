import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd

st.set_page_config(layout="wide")

# Initialization of states that will be sent across pages
st.session_state.setdefault('requirement_profile', None)
st.session_state.setdefault('applicant_name', None)
st.session_state.setdefault('grade', None)
st.session_state.setdefault('reasoning', None)
st.session_state.setdefault('matching', None)
st.session_state.setdefault('not_matching', None)
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["Name", "Date", "Role", "Grade", "Status", "Select"])
API_URL = "http://localhost:8000"

# Load external CSS file
def load_css():
    with open("ui/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Adding a logo using streamlit extras
add_logo("ui/logo.png", height=180)

# Load the CSS file
load_css()

# Initialize the different pages
recruitment_page = st.Page("dashboard.py", title="Dashboard", icon=":material/house:")
applicant_page = st.Page("applicants.py", title="Applicants", icon=":material/search:")
insights_page = st.Page("insights.py", title=" ")  # Hidden page as title is blank

# Initialize navigation and run the pages
pages = st.navigation([recruitment_page, applicant_page, insights_page])
pages.run()