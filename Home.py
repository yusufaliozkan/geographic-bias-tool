import pandas as pd
import requests
import xml.etree.ElementTree as ET

st.set_page_config(layout = "wide", 
                    page_title='Geographic Bias Tool',
                    page_icon="",
                    initial_sidebar_state="auto") 
pd.set_option('display.max_colwidth', None)

dois = ["10.1136/bmjgh-2023-013696", "10.1097/jac.0b013e31822cbdfd", '10.1080/02684527.2022.2055936', '10.1126/scitranslmed.aad9460']  # Add more DOIs as needed

df_dois = pd.DataFrame(dois, columns=['doi'])
df_dois