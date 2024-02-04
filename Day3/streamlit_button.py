import streamlit as st

st.header('Day3; st.button')

if st.button('Say hello!'):
    st.write('Why, hello there!')
else:
    st.write('Goodbye!')