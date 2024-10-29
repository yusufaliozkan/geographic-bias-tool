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
from sidebar_content import sidebar_content

st.set_page_config(layout = "wide", 
                    page_title='Geographic Bias Tool',
                    page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTtoX76TyVQs-o1vEvNuAnYX0zahtSui173gg&s",
                    initial_sidebar_state="auto") 
pd.set_option('display.max_colwidth', None)

# home_page = st.Page('Home.py', title='Affiliation finder')
# reference_finder = st.Page('Reference_finder.py', title='Reference finder')
# reference_finder2 = st.Page('Reference_finder copy.py', title='Reference finder2')

# pg = st.navigation([home_page, reference_finder, reference_finder2])

# pg.run()

sidebar_content() 

st.markdown(
    """
    <a href="https://www.imperial.ac.uk">
        <img src="https://upload.wikimedia.org/wikipedia/commons/0/06/Imperial_College_London_new_logo.png" width="300">
    </a>
    """,
    unsafe_allow_html=True
)
st.title('Geographic Bias Tool', anchor=False)

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

st.subheader('Welcome!', anchor=False)
st.write('''
    Welcome to the Geographic Bias Tool!

    Geographic Bias Tool aims to present data on the diversity of countries and country income level of authors for the selected publications or references of a work.

    The following tools are available on this platform: 

    1. **Publication affiliation finder**: This tool helps you identify the country affiliations of authors for multiple publications. 
    You can enter multiple DOIs to discover the affiliations.
    2. **Reference affiliation finder**: This tool allows you to identify the country affiliations of authors in the references of a selected work by entering a single DOI.

''')
st.subheader('Navigate to the tools:', anchor=False)

if st.button(
    "Publication affiliation finder",
    help='This tool helps you identify the country affiliations of authors for multiple publications.'
    ):
    st.switch_page("tools/Affiliation_finder.py")
if st.button(
    "Reference affiliation finder", 
    help='This tool allows you to identify the country affiliations of authors in the references of a selected work.'
    ):
    st.switch_page("tools/Reference_finder.py")

st.subheader('More information', anchor=False)

col1, col2, col3 = st.columns(3)
with col1:
    with st.expander('Who developed the Geographic Bias Tool?'):
        st.write('''
        Geographic Bias Tool has been developed by [Imperial College London](https://www.imperial.ac.uk/admin-services/library/learning-support/geo-bias/).
        It was first developed to understand the geographical diversity of publications in Imperial reading lists. 
        Another version of the same tool is available on a Power BI dashboard for Imperial staff and students only.
        '''
        )
    with st.expander('What is the Citation Source Index (CSI)?'):
        st.write('''
        Citation Source Index (CSI) is a weighted average of the World Bank rankings for Gross National Income (GNI) per capita of the countries where the authors in that citation are from. 

        The CSI ranges from 0 to 1, so a CSI closer to 1 means the overall development index of the countries represented by the authors that published the article is high or vice versa. 
        If the authors on an article were all from Afghanistan then the CSI would be 0.01. 
        If the authors on an article were all from the UK then the CSI would be 0.88. 
        The CSI for the reading list as a whole is the average of all the CSI scores for the readings provided on that list and that are available for analysis through this platform.

        For more information, the following article: https://link.springer.com/article/10.1007/s11192-021-04231-3
        '''
        )
with col2:
    with st.expander('Where does the data come from?'):
        st.write('''
        Publications data (title, author name(s), country affiliations) are retrieved through [OpenAlex API](https://docs.openalex.org/how-to-use-the-api/api-overview).

        Countries are ranked by using [World Bank GNI per capita, Atlas method](https://data.worldbank.org/indicator/NY.GNP.PCAP.CD).

        Country income statuses are retrieved from [World Bank API](https://api.worldbank.org/v2/country/?per_page=1000).
        '''
        )
    with st.expander('Limitations and caveats of the tool'):
        st.write(f'''
        * The tool searches author affiliations with DOIs. Items without a DOI will be excluded from the search. 
        Some output types (such as journal articles) are usually assigned more DOIs than other types. 
        So, for instance, you may not be able to find author affiliations for books or book chapters.

        * This tool identifies affiliations from the [OpenAlex database](https://openalex.org/).
        OpenAlex may not be able to identify all DOIs or author affiliations for various reasons. 

        * Where the affiliation information is not available for an author on the article page, the tool goes to the author's profile page on OpenAlex and checks the affiliation from there.
        This may not always give the best result as similar names can be listed under the same author profile page. 
        Check the note section at the bottom after performing your search.

        * The World Bank's GNI per capita ranking is considered as a robust indicator of country income level. However, there are some caveats on the data. 
        The classification terms can be arbitraty or outdated.

        * Citation Source Index (CSI) and this tool should not be used to compare research outputs or the datasets. 
        Having a low or high CSI does not signify the quality of individual paper or a set of outputs.
        The tool should be used to understand the nature of sources from the affiliation point of view.

        * Bear in mind that this tool does not show authors' country of origin or background but shows the affiliated country where the author wrote the paper.
        For instance, the author affiliation of the United Kingdom doesn't necessarily mean that the author is originally from the United Kingdom.  

        * The country information is sourced from OpenAlex and may be adjusted to align with the country names used by the World Bank to generate the CSI. 
        As a result, certain country names and disputed territories might be displayed differently or not be displayed in this tool. 
        The creator of this tool assumes no responsibility for any omissions or inaccuracies.
        '''
        )
with col3:
    with st.expander('Reading list about the project'):
        st.caption(f'''
        Harris, Matthew. *Decolonizing Healthcare Innovation: Low-Cost Solutions from Low-Income Countries*. Routledge, 2024, https://www.routledge.com/Decolonizing-Healthcare-Innovation-Low-Cost-Solutions-from-Low-Income-Countries/Harris/p/book/9781032284958.

        Harris, Matthew, Joachim Marti, et al. ‘Explicit Bias Toward High-Income-Country Research: A Randomized, Blinded, Crossover Experiment Of English Clinicians’. *Health Affairs*, vol. 36, no. 11, Nov. 2017, pp. 1997–2004. DOI.org (Crossref), https://doi.org/10.1377/hlthaff.2017.0773.

        Harris, Matthew, James Macinko, et al. ‘Measuring the Bias against Low-Income Country Research: An Implicit Association Test’. *Globalization and Health*, vol. 13, no. 1, Nov. 2017, p. 80. BioMed Central, https://doi.org/10.1186/s12992-017-0304-y.

        Pan, Raj Kumar, et al. ‘World Citation and Collaboration Networks: Uncovering the Role of Geography in Science’. *Scientific Reports*, vol. 2, no. 1, Nov. 2012, p. 902. www.nature.com, https://doi.org/10.1038/srep00902.

        Price, Robyn, et al. ‘A Novel Data Solution to Inform Curriculum Decolonisation: The Case of the Imperial College London Masters of Public Health’. *Scientometrics*, vol. 127, no. 2, Feb. 2022, pp. 1021–37. Springer Link, https://doi.org/10.1007/s11192-021-04231-3.

        Skopec, Mark, et al. ‘Decolonization in a higher education STEMM institution – is “epistemic fragility” a barrier?’ *London Review of Education*, vol. 19, no. 1, June 2021. journals.uclpress.co.uk, https://doi.org/10.14324/LRE.19.1.18.

        ''')
st.divider()

display_custom_license()