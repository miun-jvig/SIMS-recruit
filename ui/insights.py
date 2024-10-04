import streamlit as st

grade = st.session_state['grade']
reasoning = st.session_state['reasoning']

st.write(grade)
st.write(reasoning)
