import streamlit as st

st.header('st.latex')

st.write('The relationship between the orbital period and mass of a planet. *a* is the semi-major axis (max radius of orbit):')
st.latex(r'''
     T_{p}^{2} = \left[\frac{4\pi ^2}{G(M_{\star} + M_p)}\right] a^3
     ''')

