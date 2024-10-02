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
    <div class="top-menu" style="display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; align-items: center;">
            <span style="font-size: 24px; font-weight: bold; color: white; margin-right: 20px;">RecruitIT</span>
            <a href="#" style="margin-right: 10px;">Recruitment</a>
            <a href="#" style="margin-right: 10px;">Applicants</a>
        </div>
        <span class="profile">
            <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" alt="profile pic">
<img src="https://cdn-icons-png.flaticon.com/512/561/561188.png" alt="mail icon" class="icon">
  <path d="M4.5 4H19.5C20.8807 4 22 5.11929 22 6.5V17.5C22 18.8807 20.8807 20 19.5 20H4.5C3.11929 20 2 18.8807 2 17.5V6.5C2 5.11929 3.11929 4 4.5 4Z"></path>
  <path d="M22 6L12 13L2 6"></path>
</svg>
           Alaa Ourabi
        </span>
    </div>
    """, unsafe_allow_html=True)

# RECRUITMENT PAGE LAYOUT
layout_recruitment()
