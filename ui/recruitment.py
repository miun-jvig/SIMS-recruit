from style import css_upload
import streamlit as st
import base64


# Funktion för att läsa och visa en PDF-fil i en iframe
def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)


# Layout med två kolumner
def layout_recruitment():
    col1, col2 = st.columns([1, 3])
    # Sidomeny som drop-down meny i vänstra kolumnen
    with col1:
        with st.expander("Choose Profile"):
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

    # PDF-visning i högra kolumnen (innehållsdelen)
    with col2:
        st.markdown("""
            <div class="content">
                <h2>Preview Profile</h2>
        """, unsafe_allow_html=True)

        # Visa vald PDF-fil i den högra kolumnen om en PDF har valts
        if 'selected_pdf' in st.session_state:
            show_pdf(st.session_state.selected_pdf)

        # Knappar för "Upload Template" och "Use Template"
        st.markdown(css_upload(), unsafe_allow_html=True)
