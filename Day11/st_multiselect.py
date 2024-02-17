import streamlit as st

st.header('st.multiselect')

options = st.multiselect(
     label='What are your favorite colors',
     options=['Green', 'Yellow', 'Red', 'Blue'],
     default=['Yellow', 'Red'],
     max_selections=2)

st.write('You selected:', options)