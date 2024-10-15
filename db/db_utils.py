import requests
import pandas as pd
import streamlit as st

# Not implemented yet!!!!!!!!
def update_row_from_db():

    response = requests.get("http://localhost:8000/get_all_entries/")

    if response.status_code == 200:
        all_entries = response.json()
        st.session_state.df = pd.DataFrame(columns=["Name", "Date", "Role", "Grade", "Status", "Select"])

        for entry in all_entries:
            st.session_state.df = st.session_state.df.append({
                "Name": entry["cv_filename"],
                "Date": entry["created_at"],
                "Role": entry["job_filename"],
                "Grade": entry['grade'] if entry['grade'] else "-",
                "Status": "Graded" if entry['grade'] else "pending",
                "Select": False
            }, ignore_index=True)

        # Lägg till loggning för att visa alla entries
        st.write("Alla entries från databasen: ", all_entries)
    else:
        st.error("Failed to retrieve data from the API")
