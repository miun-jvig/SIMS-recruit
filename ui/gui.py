import streamlit as st
from style import css_gui, css_main_menu
from recruitment import layout_recruitment

# Konfigurera sidlayout
st.set_page_config(page_title="RecruitIT", layout="wide")
# Använd CSS-stylingen från style.py
st.markdown(css_gui(), unsafe_allow_html=True)

# Top menu with profile picture and mail icon
st.markdown(css_main_menu(), unsafe_allow_html=True)

# RECRUITMENT
layout_recruitment()
