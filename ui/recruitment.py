import streamlit as st
import base64


# Function to display a PDF file inside an iframe
def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700px" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)


# Recruitment page layout with two columns
def layout_recruitment():
    col1, col2 = st.columns([1, 3])

    # Side menu as a drop-down in the left column
    with col1:
        with st.expander("Choose Profile"):
            # Buttons that open specific PDF files
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

    # PDF display in the right column (content area)
    with col2:
        st.markdown("""
            <div class="content">
                <h2>Preview Profile</h2>
        """, unsafe_allow_html=True)

        # Display the selected PDF in the right column if one is chosen
        if 'selected_pdf' in st.session_state:
            show_pdf(st.session_state.selected_pdf)

        # Upload Template and Use Template buttons (styled via external CSS)
        st.markdown("""
            <div class="upload-buttons">
            <div style="margin-top: 20px; text-align: center;">
                <button style="padding: 10px 105px; background-color: #6C4FA1; color: white; border: none; border-radius: 5px; margin-right: 10px;">Use Requirement Profile</button>
            <button style="padding: 10px 105px; background-color:  #00BFFF; color: white; border: none; border-radius: 5px;">Upload New Profile</button>
            </div>
        """, unsafe_allow_html=True)
