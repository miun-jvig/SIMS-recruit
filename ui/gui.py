import streamlit as st
import random
from fpdf import FPDF
import requests
from ui.style import button_styles  # Import the button styles from style.py


# Anropa stilmallen
st.markdown(button_styles(), unsafe_allow_html=True)

# Konfigurera sidlayouten direkt efter import
st.set_page_config(page_title="CV Graderingssystem", layout="wide")

# Initialize session state variables if they don't exist yet
if 'cv_id' not in st.session_state:
    st.session_state.cv_id = ""  # Initialize cv_id as an empty string

if 'ai_grade' not in st.session_state:
    st.session_state.ai_grade = random.randint(1, 5)  # Simulated AI grading score


# Funktion för att skapa PDF
def export_to_pdf(grade, insights, cv_id, req_profile):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="CV Graderingsrapport", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"CV ID: {cv_id}", ln=True)
    pdf.cell(200, 10, txt=f"Kravprofil: {req_profile}", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Gradering: {grade}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt="Insikter:", ln=True)
    for insight in insights:
        pdf.cell(200, 10, txt=f"- {insight}", ln=True)
    pdf.output(f"cv_report_{cv_id}.pdf")


# Funktion för att skicka filer för analys
def analyze_files(cv, profile):
    st.success("Filer skickade för analys!")
    # Här kan du lägga till kod för att analysera filer, t.ex.:
    # agent.analyze(cv, profile)


# Skapa Streamlit-app med sidomeny
st.sidebar.title("Meny")
option = st.sidebar.radio("Navigera", ["Ladda upp filer", "Se resultat"])

# Variabler
manual_grade = None
user_chooses_manual_grading = False

# Huvudsidan - Ladda upp filer
if option == "Ladda upp filer":
    st.title("CV Graderingssystem")
    st.write("Ladda upp både ditt CV och en kravprofil för gradering.")

    # Ladda upp CV och Kravprofil
    uploaded_cv = st.file_uploader("Ladda upp ditt CV", type=["pdf", "docx", "txt"], key="cv_uploader")
    uploaded_profile = st.file_uploader("Ladda upp kravprofil", type=["pdf", "docx", "txt"], key="profile_uploader")

    if uploaded_cv and uploaded_profile:
        st.success("Båda filer uppladdade!")
        st.session_state.cv_id = st.text_input("Ange CV ID", placeholder="Ex: CV_1234")

        if st.button("Skicka till analys"):
            # Files to [FastAPI]
            files = {
                'cv': (uploaded_cv.name, uploaded_cv, uploaded_cv.type),
                'profile': (uploaded_profile.name, uploaded_profile, uploaded_profile.type),
            }

            # Send files to FastAPI (FastAPI = middleman)
            # Check link: https://www.w3schools.com/python/module_requests.asp

            try:
                response = requests.post("http://localhost:8000/analyze/", files=files)

                # Check if -> Success
                if response.status_code == 200:
                    result = response.json()
                    grade = result.get('ai_grade')
                    insights = result.get('insights')

                    st.write(f"AI betyg: {grade}")
                    st.write(f"AI insikter: {insights}")

                else:
                    st.error("Fel i analysen(på backendsidan)")

            except requests.exceptions.RequestException as e:
                st.error(f"Fel vid anslutning till API: {e}")

            # Visa AI-graderingen (simulerad AI-gradering)
            st.write(f"AI har graderat detta CV: {st.session_state.cv_id}")
            ai_grade = st.session_state.ai_grade  # Retrieve the AI grade from session state
            st.write(f"AI-gradering: [{ai_grade}/5]")
            st.write("🟢" * ai_grade + "⚪" * (5 - ai_grade))

            # Länk för att öppna CV
            st.markdown("[Öppna CV (länk)](https://example.com/cv)")

        # Initiera session state för att hålla koll på graderingstillstånd
        if 'manual_grade' not in st.session_state:
            st.session_state.manual_grade = ""
        if 'user_chooses_manual_grading' not in st.session_state:
            st.session_state.user_chooses_manual_grading = False

        # Rubrik för avsnittet
        st.title("Gradering och Validering")

        # Skapa två kolumner med jämn fördelning
        col1, col2 = st.columns(2)

        # Första kolumnen: Validera gradering
        with col1:
            st.subheader("Validera gradering")
            if st.button("Validera gradering", key="validate"):
                st.success("Gradering validerad!")

        # Andra kolumnen: Ändra gradering
        with col2:
            st.subheader("Ändra gradering")
            if st.button("Ändra gradering", key="change"):
                st.session_state.user_chooses_manual_grading = True
                st.info("Du vill gradera själv! Fyll i en siffra manuellt mellan 1 och 5.")

            # Om användaren har valt att gradera själv
            if st.session_state.user_chooses_manual_grading:
                # Textbox för manuell gradering
                st.session_state.manual_grade = st.text_input("Fyll i gradering (1-5)",
                                                              value=st.session_state.manual_grade)

                # Kontrollera att inmatningen är en siffra och inom intervallet 1-5
                if st.session_state.manual_grade.isdigit():
                    grade = int(st.session_state.manual_grade)
                    if 1 <= grade <= 5:
                        st.success(f"Du har valt gradering: {st.session_state.manual_grade}")
                        st.success("Gradering validerad manuellt!")
                    else:
                        st.error("Graderingen måste vara mellan 1 och 5. Försök igen!")
                elif st.session_state.manual_grade != "":
                    st.error("Vänligen fyll i en giltig siffra.")

        # Lägg till en linje för att separera sektioner och ge bättre layout
        st.markdown("---")

        # Extra avstånd mellan knappen och rutan
        st.markdown("<br><br>", unsafe_allow_html=True)

        # Rapportknapp för att skapa en PDF
        import os
        from types import SimpleNamespace
        import streamlit as st

        # Simulera funktionen export_to_pdf (du kan ersätta med din faktiska implementering)
        def export_to_pdf(grade, insights, cv_id, profile_name):
            file_path = f"report_{cv_id}.pdf"
            # Här simulerar vi att PDF-filen skapas
            with open(file_path, "w") as f:
                f.write(f"Report for {profile_name}\nGrade: {grade}\nInsights: {insights}\nCV ID: {cv_id}")
            return file_path

        if st.button("Testa skapa PDF"):
            manual_grade = "3"
            uploaded_profile = SimpleNamespace(name="test_profile")  # Dummy kravprofil
            st.session_state.cv_id = "1234"  # Dummy CV ID
            file_path = export_to_pdf(manual_grade, ["Testinsikter"], st.session_state.cv_id, uploaded_profile.name)

            # Lägg till en skrivutskrift för att kontrollera om filvägen är korrekt
            st.write(f"Generated file path: {file_path}")

            if os.path.exists(file_path):
                st.success(f"PDF skapad som '{file_path}'!")
                with open(file_path, "rb") as file:
                    st.download_button(label="Ladda ner rapport", data=file, file_name=file_path)
            else:
                st.error("Misslyckades med att skapa PDF.")

    # Resultatsida
    if option == "Se resultat":
        st.title("Resultat och tidigare rapporter")
        st.write("Här kan du visa och hantera tidigare skapade rapporter.")
