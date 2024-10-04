from datetime import datetime
import streamlit as st
import pandas as pd


def update_row(name, profile, grade, status):
    # Incoming new data to be updated in the table
    new_data = {'Name': name, 'Date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'Role': profile, 'Grade': grade, 'Status': status, 'Select': True}

    if 'df' in st.session_state and not st.session_state.df.empty:
        # Update the row if it exists, else append it
        if name in st.session_state.df['Name'].values:
            # Update existing row using loc
            st.session_state.df.loc[st.session_state.df['Name'] == name, ['Grade', 'Status', 'Date']] = [
                grade, status, new_data['Date']]
        else:
            # Append a new row if not found
            st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_data])], ignore_index=True)
    else:
        # If DataFrame is empty, just add the new row
        st.session_state.df = pd.DataFrame([new_data])
