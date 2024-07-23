import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET

st.set_page_config(layout = "centered", 
                    page_title='Geographic Bias Tool',
                    page_icon="",
                    initial_sidebar_state="auto") 
pd.set_option('display.max_colwidth', None)

with st.sidebar:
    # st.image(path2, width=150)
    st.subheader("Geographic Bias Tool",anchor=None)  
    with st.expander('About'):  
        st.write('Note here')
        components.html(
"""
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/80x15.png" /></a><br />This tool is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
"""
)

dois = ["10.1136/bmjgh-2023-013696", "10.1097/jac.0b013e31822cbdfd", '10.1080/02684527.2022.2055936', '10.1126/scitranslmed.aad9460']  # Add more DOIs as needed

df_dois = pd.DataFrame(dois, columns=['doi'])
df_dois