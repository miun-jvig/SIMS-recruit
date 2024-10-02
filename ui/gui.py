import streamlit as st
from recruitment import layout_recruitment

# Konfigurera sidlayout
st.set_page_config(page_title="RecruitIT", layout="wide")


# Load external CSS file
def load_css():
    with open("ui/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Load the CSS file
load_css()

# Top menu with profile picture and mail icon
st.markdown("""
    <div class="top-menu">
        <a href="#">Recruitment</a>
        <a href="#">Applicants</a>
        <span class="profile">
            <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" alt="profile pic">
            <img src="https://cdn-icons-png.flaticon.com/512/725/725643.png" alt="mail icon" class="icon">
           Alaa Ourabi
        </span>
    </div>
""", unsafe_allow_html=True)

# RECRUITMENT PAGE LAYOUT
layout_recruitment()
