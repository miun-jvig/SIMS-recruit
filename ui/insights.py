import streamlit as st

grade = st.session_state['grade']
reasoning = st.session_state['reasoning']
matching = st.session_state['matching']
not_matching = st.session_state['not_matching']

st.write(grade)
st.write(reasoning)
st.write(matching)
st.write(not_matching)
