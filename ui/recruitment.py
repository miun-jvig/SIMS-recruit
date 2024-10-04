import streamlit as st
import base64


# Function to display a PDF file inside an iframe
def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = (f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700px" '
                       f'type="application/pdf"></iframe>')
        st.markdown(pdf_display, unsafe_allow_html=True)


# Recruitment page layout with two columns
dropdown_column, profile_column = st.columns([1, 3])

# Side menu as a drop-down in the left column
with dropdown_column:
    template_option = st.selectbox(
        "Choose Requirement Profile:",
        ("System Developer", "Systems Analyst", "Data Science", "Cloud Engineer", "Network Engineer", "IT Analyst",
         "Technician", "Support Specialist")
    )

# PDF display in the right column (content area)
with profile_column:
    st.markdown("""
        <div class="content">
            <h2 id="preview">Preview Profile</h2>
    """, unsafe_allow_html=True)

    # Display the selected PDF in the right column if one is chosen
    if 'selected_pdf' in st.session_state:
        show_pdf(st.session_state.selected_pdf)

    st.write("")

    use_profile, upload_profile = st.columns(2)
    if use_profile.button("Use Requirement Profile"):
        st.switch_page("applicants.py")

    with upload_profile:
        uploaded_profile = st.file_uploader("Upload Profile", type=["pdf", "docx", "txt"])
        if uploaded_profile is not None:
            st.session_state.requirement_profile = uploaded_profile
