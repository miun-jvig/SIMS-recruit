import streamlit as st
from streamlit_extras.app_logo import add_logo

st.set_page_config(layout="wide")

if "processed_text" not in st.session_state:
    st.session_state.processed_text = None


# Load external CSS file
def load_css():
    with open("ui/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


add_logo("ui/logo.png", height=180)

# Load the CSS file
load_css()

recruitment_page = st.Page("pages/recruitment.py", title="Recruitment", icon=":material/house:")
applicant_page = st.Page("pages/applicants.py", title="Applicants", icon=":material/search:")
insights_page = st.Page("pages/insights.py", title=" ")

pages = st.navigation([recruitment_page, applicant_page, insights_page])
pages.run()
