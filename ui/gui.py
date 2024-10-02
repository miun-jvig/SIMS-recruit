import streamlit as st
import base64
from style import load_styles  # Importera CSS-stylingen

# Konfigurera sidlayout
st.set_page_config(page_title="RecruitIT", layout="wide")
# Använd CSS-stylingen från style.py
st.markdown(load_styles(), unsafe_allow_html=True)

# Funktion för att läsa och visa en PDF-fil i en iframe
def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

# CSS för att skapa en sidomeny som matchar din design och lägga till ikoner och funktioner


# Top menu with profile picture and mail icon
st.markdown("""
    <div class="top-menu">
        <a href="#">Recruitment</a>
        <a href="#">Applicants</a>
        <a href="#">Insights</a>
        <span class="profile">
            <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" alt="profile pic">
            <img src="https://cdn-icons-png.flaticon.com/512/725/725643.png" alt="mail icon" class="icon">
           Alaa Ourabi
        </span>
    </div>
    """, unsafe_allow_html=True)

# Layout med två kolumner
col1, col2 = st.columns([1, 3])

# Sidomeny som drop-down meny i vänstra kolumnen
with col1:
    with st.expander("Template drop-down-meny "):
        # Knappar som öppnar specifika PDF-filer
        if st.button("System Developer"):
            st.session_state.selected_pdf = "C:/Users/AlaaO/Downloads/Advertisement (14).pdf"

        if st.button("Systems Analyst"):
            st.session_state.selected_pdf = "C:/Users/AlaaO/Downloads/Advertisement (12).pdf"

        if st.button("Data Science"):
            st.session_state.selected_pdf = "C:/Users/AlaaO/Downloads/Advertisement (13).pdf"

        if st.button("Cloud Engineer"):
            st.session_state.selected_pdf = "C:/Users/AlaaO/Downloads/Advertisement (14).pdf"

        if st.button("Network Engineer"):
            st.session_state.selected_pdf = "C:/Users/AlaaO/Downloads/Advertisement (15).pdf"

        if st.button("IT Analyst"):
            st.session_state.selected_pdf = "C:/Users/AlaaO/Downloads/Advertisement (10).pdf"

        if st.button("Technician"):
            st.session_state.selected_pdf = "C:/Users/AlaaO/Downloads/Advertisement (17).pdf"

        if st.button("Support Specialist"):
            st.session_state.selected_pdf = "C:/Users/AlaaO/Downloads/Advertisement (18).pdf"

        # Lägg till en knapp för "Add Role"
        st.button("Add Role")

# PDF-visning i högra kolumnen (innehållsdelen)
with col2:
    st.markdown("""
        <div class="content">
            <h2>Preview Template</h2>
    """, unsafe_allow_html=True)

    # Visa vald PDF-fil i den högra kolumnen om en PDF har valts
    if 'selected_pdf' in st.session_state:
        show_pdf(st.session_state.selected_pdf)

    # Knappar för "Upload Template" och "Use Template"
    st.markdown("""
        <div style="margin-top: 20px;">
            <button style="padding: 10px 90px; background-color: #6C4FA1; color: white; border: none; border-radius: 5px;">Upload Template</button>
            <button style="padding: 10px 90px; background-color: #6C4FA1; color: white; border: none; border-radius: 5px; margin-left: 10px;">Use Template</button>
        </div>
    """, unsafe_allow_html=True)