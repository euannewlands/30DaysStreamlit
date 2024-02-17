import streamlit as st

def upper_case_it(opt: str) -> str:
    return opt.upper()

st.header('st.selectbox')

option = st.selectbox(
     'What is your favorite color?',
     ('Blue', 'Red', 'Green'),
     format_func=upper_case_it,
     label_visibility='collapsed',
     disabled = False,
     index = None,
     placeholder='Choose a colour...')

if option is not None:
    st.write('Your favorite color is ', option)