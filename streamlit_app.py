import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET
import streamlit.components.v1 as components
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import plotly.express as px
from copyright import display_custom_license
import numpy as np
import plotly.express as px
import time

# home_page = st.Page('Home.py', title='Affiliation finder')

affiliation_finder = st.Page('tools/Affiliation_finder.py', title='Publication affiliation finder')
reference_finder = st.Page('tools/Reference_finder.py', title='Reference affiliation finder')
intro = st.Page('home/Home.py', title='Home')

pg = st.navigation(
    {
        'Home':[intro],
        'Tools':[affiliation_finder, reference_finder]
    }
)
    
pg.run()
