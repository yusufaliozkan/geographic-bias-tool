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

st.set_page_config(layout = "wide", 
                    page_title='Geographic Bias Tool',
                    page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTtoX76TyVQs-o1vEvNuAnYX0zahtSui173gg&s",
                    initial_sidebar_state="auto") 
pd.set_option('display.max_colwidth', None)

with st.sidebar:
    st.markdown(
        """
        <a href="https://www.imperial.ac.uk">
            <img src="https://upload.wikimedia.org/wikipedia/commons/0/06/Imperial_College_London_new_logo.png" width="150">
        </a>
        """,
        unsafe_allow_html=True
    )
    st.header("Geographic Bias Tool",anchor=False)  
    with st.expander('Licence'):  
        display_custom_license()
    with st.expander('Source code'):
        st.write('Source code and datasets used for this tool are available here:')
        st.caption(
            "[![GitHub repo](https://img.shields.io/badge/GitHub-Geographic_Bias_Tool_repo-0a507a?logo=github)](https://github.com/yusufaliozkan/geographic-bias-tool) "
        )
    with st.expander('Disclaimer'):
        st.warning('''
        There are some limitations of this tool (check the Limitations section under 'About this tool'). 
        Therefore, this tool should not be used to compare articles or a set of publications and never be used for any research performance assessment purposes.

        Although every effort is made to ensure accuracy and the tool is operational, the support may not be guaranteed. 
        Bear in mind that there might be some technical issues caused by OpenAlex or Streamlit.
        ''')
    with st.expander('Contact'):
        st.write('For your questions, you can contact [Yusuf Ozkan, Research Outputs Analyst](https://profiles.imperial.ac.uk/y.ozkan) at Imperial College London.')

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

col1, col2 = st.columns([3,2])
with col1:
    with st.popover('About this tool', use_container_width=False):
    
        st.write('''
        Geographic Bias Tool aims to present data on the diversity of countries and country income level of authors. 
        You can submit DOIs of publications to see the authors' country affiliations and country income statuses. 
        The tool aims to identify authors of given DOIs and found their country affiliations. Countries are ranked based on [World Bank GNI per capita, Atlas method](https://data.worldbank.org/indicator/NY.GNP.PCAP.CD). 
        The Citation Source Index is calculated to show the geographic bias of the given publication set.
        '''
        )

        with st.expander('Who developed?'):
            st.write('''
            Geographic Bias Tool has been developed by [Imperial College London](https://www.imperial.ac.uk/admin-services/library/learning-support/geo-bias/).
            '''
            )

        with st.expander('What is Citation Source Index (CSI)?'):
            st.write('''
            Citation Source Index (CSI) is a weighted average of the World Bank rankings for Gross National Income (GNI) per capita of the countries where the authors in that citation are from. 

            The CSI ranges from 0 to 1, so a CSI closer to 1 means the overall development index of the countries represented by the authors that published the article is high or vice versa. 
            If the authors on an article were all from Afghanistan then the CSI would be 0.01. 
            If the authors on an article were all from the UK then the CSI would be 0.88. 
            The CSI for the reading list as a whole is the average of all the CSI scores for the readings provided on that list and that are available for analysis through this platform.

            For more information, the following article: https://link.springer.com/article/10.1007/s11192-021-04231-3
            '''
            )

        with st.expander('Where the data comes from?'):
            st.write('''
            Publications data (title, author name(s), country affiliations) are retrieved through [OpenAlex API](https://docs.openalex.org/how-to-use-the-api/api-overview).

            Countries are ranked by using [World Bank GNI per capita, Atlas method](https://data.worldbank.org/indicator/NY.GNP.PCAP.CD).

            Country income statuses are retrieved from [World Bank API](https://api.worldbank.org/v2/country/?per_page=1000).
            '''
            )
        with st.expander('Limitations'):
            st.write(f'''
            * The tool searches author affiliations with DOIs. Items without a DOI will be excluded from the search. 
            Some output types (such as journal articles) are usually assigned more DOIs than other types. 
            So, for instance, you may not be able to find author affiliations for books or book chapters.

            * This tool identifies affiliations from the [OpenAlex database](https://openalex.org/).
            OpenAlex may not be able to identify all DOIs or author affiliations for various reasons. 

            * Where the affiliation information is not available for an author on the article page, the tool goes to the author's profile page on OpenAlex and checks the affiliation from there.
            This may not always give the best result as similar names can be listed under the same author profile page. 
            Check the note section at the bottom after performing your search.

            * The World Bank's GNI per capita ranking is considered as a robust indicator of country income level. . However, there are some caveats on the data. 
            The classification terms can be arbitraty or outdated.

            * Citation Source Index (CSI) and this tool should not be used to compare research outputs or the datasets. 
            Having a low or high CSI does not signify the quality of individual paper or a set of outputs.
            The tool should be used to understand the nature of sources from the affiliation point of view.
            '''
            )
        with st.expander('Reading list about the project'):
            st.caption(f'''
            Harris, Matthew. *Decolonizing Healthcare Innovation: Low-Cost Solutions from Low-Income Countries*. Routledge, 2024, https://www.routledge.com/Decolonizing-Healthcare-Innovation-Low-Cost-Solutions-from-Low-Income-Countries/Harris/p/book/9781032284958.

            Harris, Matthew, Joachim Marti, et al. ‘Explicit Bias Toward High-Income-Country Research: A Randomized, Blinded, Crossover Experiment Of English Clinicians’. *Health Affairs*, vol. 36, no. 11, Nov. 2017, pp. 1997–2004. DOI.org (Crossref), https://doi.org/10.1377/hlthaff.2017.0773.

            Harris, Matthew, James Macinko, et al. ‘Measuring the Bias against Low-Income Country Research: An Implicit Association Test’. *Globalization and Health*, vol. 13, no. 1, Nov. 2017, p. 80. BioMed Central, https://doi.org/10.1186/s12992-017-0304-y.

            Pan, Raj Kumar, et al. ‘World Citation and Collaboration Networks: Uncovering the Role of Geography in Science’. *Scientific Reports*, vol. 2, no. 1, Nov. 2012, p. 902. www.nature.com, https://doi.org/10.1038/srep00902.

            Price, Robyn, et al. ‘A Novel Data Solution to Inform Curriculum Decolonisation: The Case of the Imperial College London Masters of Public Health’. *Scientometrics*, vol. 127, no. 2, Feb. 2022, pp. 1021–37. Springer Link, https://doi.org/10.1007/s11192-021-04231-3.

            Skopec, Mark, et al. ‘Decolonization in a higher education STEMM institution – is “epistemic fragility” a barrier?’ *London Review of Education*, vol. 19, no. 1, June 2021. journals.uclpress.co.uk, https://doi.org/10.14324/LRE.19.1.18.

            ''')

df_dois = None

radio = st.radio('Select an option', ['Insert DOIs', 'Upload a file with DOIs'])
if radio == 'Insert DOIs':
    st.write('Please insert DOIs (commencing "10.") in separarate rows. Maximum **500 DOIs permitted**!')
    dois = st.text_area(
        'Type or paste in one DOI per line in this box, then press Ctrl+Enter.', 
        help='DOIs will be without a hyperlink such as 10.1136/bmjgh-2023-013696',
        placeholder=''' e.g.
        10.1136/bmjgh-2023-013696
        10.1097/jac.0b013e31822cbdfd
        '''
        )
    # Split the input text into individual DOIs based on newline character
    doi_list = dois.split('\n')
    
    # Remove any empty strings that may result from extra newlines
    doi_list = [doi.strip() for doi in doi_list if doi.strip()]
    
    # Create a DataFrame
    df_dois = pd.DataFrame(doi_list, columns=["doi"])
else:
    st.write('Please upload and submit a .csv file of DOIs (commencing “10.") in separate rows. **Maximum 500 DOIs permitted**!')
    st.warning('The title of the column containing DOIs should be one of the followings: doi, DOI, dois, DOIs, Hyperlinked DOI. Otherwise the tool will not identify DOIs.')
    dois = st.file_uploader("Choose a CSV file", type="csv")

    if dois is not None:
        # Read the uploaded CSV file into a DataFrame
        df = pd.read_csv(dois)
        
        # List of possible DOI column names
        doi_columns = ['doi', 'DOI', 'dois', 'DOIs', 'Hyperlinked DOI']
        
        # Find the first matching DOI column
        doi_column = None
        for col in doi_columns:
            if col in df.columns:
                doi_column = col
                break
        
        if doi_column:
            # Create a DataFrame with DOIs only
            df_dois = df[[doi_column]]
            df_dois.columns = ['doi']  # Standardize column name to 'DOI'
        
        else:
            st.error('''
            No DOI column in the file.
            
            Make sure that the column listing DOIs have one of the following alternative names:
            'doi', 'DOI', 'dois', 'DOIs', 'Hyperlinked DOI'
            ''')
            st.stop()
    else:
        st.write("Please upload a CSV file to calculate CSI.")

if df_dois is not None and len(df_dois) > 500:
    st.error('Please enter 500 or fewer DOIs')

else:
    if dois:
        df_dois['doi'] = df_dois['doi'].str.replace('https://doi.org/', '')
        df_dois = df_dois.drop_duplicates().reset_index(drop=True)
        no_dois = len(df_dois)
        if len(df_dois) > 100:
            st.toast('You entered over 100 DOIs. It may take some time to retrieve results. Please wait.')
        if len(df_dois) >100:
            st.warning('You entered over 100 DOIs. It may take some time to retrieve results.')
        st.info(f'You entered {no_dois} unique DOIs')
        with st.expander(f'See the DOIs you entered'):
            df_dois

        col1, col2 = st.columns(2)
        with col1:
            submit = st.button('Calculate Citation Source Index')
        with col2:
            exclude_author_profile_page = st.checkbox(
                'Do not show affiliations from the author profile page',
                help='''
                Author affiliation may not always be present on the article page. 
                In that case, the tool will go to the author profile and try to identify author affiliation from there.
                However, country affiliations found on author profile pages may not be reliable because author profile pages can contain different author information for similar names.
                '''
                )

        if submit or st.session_state.get('status_expanded', False):

            if submit:
                st.session_state['status_expanded'] = True
            with st.status("Finding sources and calculating CSI...", expanded=st.session_state.get('status_expanded', True)) as status:
                ## OPENALEX DATA RETRIEVAL
                def fetch_authorship_info_and_count(doi):
                    url = f"https://api.openalex.org/works/doi:{doi}"
                    response = requests.get(url)
                    if response.status_code == 200:
                        data = response.json()
                        title = data.get('title', '')
                        authorship_info = data.get('authorships', [])
                        author_count = len(authorship_info)
                        return title, authorship_info, author_count
                    else:
                        return '', [], 0
                if not exclude_author_profile_page:
                    # Function to fetch author details using author ID
                    def fetch_author_details(author_id):
                        response = requests.get(author_id)
                        if response.status_code == 200:
                            data = response.json()
                            return data
                        else:
                            return None

                # Fetch authorship information for each DOI and store it in a new DataFrame
                authorship_data = []

                for doi in df_dois['doi']:
                    title, authorship_info, author_count = fetch_authorship_info_and_count(doi)
                    for author in authorship_info:
                        country_codes = author.get('countries', [])
                        source = 'article page'
                        if not country_codes:
                            country_codes = ['']
                            source = 'author profile page'
                        for country_code in country_codes:
                            author_record = {
                                'doi': doi,
                                'title': title,
                                'author_position': author.get('author_position', ''),
                                'author_name': author.get('author', {}).get('display_name', ''),
                                'author_id': author.get('author', {}).get('id', ''),
                                'Country Code 2': country_code,
                                'source': source,
                                'author_count': author_count
                            }
                            authorship_data.append(author_record)

                df_authorships = pd.DataFrame(authorship_data)
                openalex_found_dois = len(df_authorships)
                if openalex_found_dois == 0:
                    st.error('''
                    No DOIs found! 

                    Check your DOIs and submit them again. 

                    If you are sure that the DOIs are correct, they may not be available in the [OpenAlex](https://openalex.org/) database.
                    ''')
                    status.update(label=f"Calculation complete without any results!", state="complete", expanded=True)
                else:
                    df_authorships['Country Code 2'] = df_authorships['Country Code 2'].str.strip()
                    df_authorships['Country Code 2'].replace('', pd.NA, inplace=True)
                    
                    # Remove duplicate rows
                    df_authorships = df_authorships.drop_duplicates()
                    # Add 'api.' between 'https://' and 'openalex' in the 'author_id' column
                    df_authorships['author_id'] = df_authorships['author_id'].apply(lambda x: x.replace('https://', 'https://api.') if x else x)

                    if not exclude_author_profile_page:
                        # Function to update country_code if missing and mark the source
                        def update_country_code(row):
                            if pd.isna(row['Country Code 2']) and row['author_id']:
                                author_details = fetch_author_details(row['author_id'])
                                if author_details:
                                    affiliations = author_details.get('affiliations', [])
                                    if affiliations:
                                        country_code = affiliations[0].get('institution', {}).get('country_code', '')
                                        if country_code:
                                            row['Country Code 2'] = country_code
                                            row['source'] = 'author profile page'
                            return row

                        # Update country codes for rows where country_code is missing
                        df_authorships = df_authorships.apply(update_country_code, axis=1)
                    
                        # df_authorships = df_authorships[df_authorships['source']!='author profile page']
                        df_authorships
                        
                    df_authorships['Country Code 2'] = df_authorships['Country Code 2'].fillna('No country info')
                    df_authorships['Country Code 2'] = df_authorships['Country Code 2'].replace('TW', 'CN')
                    df_authorships['Country Code 2'] = df_authorships['Country Code 2'].replace('RE', 'FR')


                    ## WORLD BANK API
                    # # Add 'api.' between 'https://' and 'openalex' in the 'author_id' column
                    # df_authorships['author_id'] = df_authorships['author_id'].apply(lambda x: x.replace('https://', 'https://api.') if x else x)

                    # ### THE BELOW IS DUPLICATE
                    # # Function to update country_code if missing and mark the source
                    # def update_country_code(row):
                    #     if not row['Country Code 2'] and row['author_id']:
                    #         author_details = fetch_author_details(row['author_id'])
                    #         if author_details:
                    #             affiliations = author_details.get('affiliations', [])
                    #             if affiliations:
                    #                 country_code = affiliations[0].get('institution', {}).get('country_code', '')
                    #                 if country_code:
                    #                     row['Country Code 2'] = country_code
                    #                     row['source'] = 'author profile page'
                    #     return row

                    # # Update country codes for rows where country_code is missing
                    # df_authorships = df_authorships.apply(update_country_code, axis=1)
                    ### DUPLICATE ENDS

                    # world_bank_api_url = "https://api.worldbank.org/v2/country/?per_page=1000"
                    # response = requests.get(world_bank_api_url)
                    # root = ET.fromstring(response.content)

                    # # Extract relevant data and store it in a list
                    # country_data = []
                    # for country in root.findall(".//{http://www.worldbank.org}country"):
                    #     country_id = country.get('id')
                    #     iso2Code = country.find("{http://www.worldbank.org}iso2Code").text
                    #     name = country.find("{http://www.worldbank.org}name").text
                    #     income_level = country.find("{http://www.worldbank.org}incomeLevel").text
                        
                    #     country_record = {
                    #         'Country Code 3': country_id,
                    #         'Country Code 2': iso2Code,
                    #         'name': name,
                    #         'incomeLevel': income_level
                    #     }
                    #     country_data.append(country_record)

                    # # Create a DataFrame from the list
                    # df_countries = pd.DataFrame(country_data)
                    df_countries = pd.read_csv('world_bank_api_results.csv')

                    ## GNI CALCULATIONS
                    df = pd.read_csv(
                        'API_NY.GNP.PCAP.CD_DS2_en_csv_v2_1519779.csv',
                        skiprows=4,  # Example: skipping the first 4 rows if they are not needed
                        delimiter=',',  # Adjust delimiter if it's not a comma
                    )
                    df = df.drop(columns=['Indicator Name', 'Indicator Code'])

                    # Melt the DataFrame to make it long-form
                    df_melted = df.melt(id_vars=['Country Name', 'Country Code'], var_name='Year', value_name='GNI')
                    df_melted = df_melted.rename(columns={'Country Code':'Country Code 3'})
                    # Drop rows with missing GNI values
                    df_melted = df_melted.dropna(subset=['GNI'])

                    # Convert 'Year' to integer
                    df_melted['Year'] = df_melted['Year'].astype(int)

                    # Sort by 'Country Name' and 'Year' to get the latest GNI for each country
                    df_sorted = df_melted.sort_values(by=['Country Name', 'Year'], ascending=[True, False])

                    # Drop duplicates to keep the most recent GNI for each country
                    df_most_recent = df_sorted.drop_duplicates(subset=['Country Name'])

                    # Select the desired columns
                    df_result = df_most_recent[['Country Name', 'Country Code 3', 'Year', 'GNI']].reset_index(drop=True)
                    df_result = pd.merge(df_result, df_countries, on='Country Code 3', how='left')
                    df_result = df_result[df_result['incomeLevel']!='Aggregates'].reset_index(drop=True)
                    df_result = df_result.sort_values(by='GNI', ascending=True).reset_index(drop=True)
                    df_result.index = df_result.index + 1
                    df_result = df_result.rename_axis('Rank').reset_index()
                    new_row = pd.DataFrame([{
                        'Rank': np.nan,
                        'Country Name': 'No country info',
                        'Country Code 3': 'No country info',
                        'Year': 2023,
                        'GNI': np.nan,  # Use NaN for missing numerical data
                        'Country Code 2': 'No country info',
                        'name': 'No country info',
                        'incomeLevel': 'No country info'
                    }])

                    df_result = pd.concat([df_result, new_row], ignore_index=True)
                    df_authorships = pd.merge(df_authorships, df_result, on='Country Code 2', how='left')


                    df_authorships['author_weighting'] = 1 / df_authorships['author_count']
                    df_authorships['author_weighting_score'] = df_authorships['Rank']*df_authorships['author_weighting']
                    df_authorships['all_authors'] = df_authorships.groupby('doi')['author_name'].transform(lambda x: ' | '.join(x))
                    countries_combined = df_authorships.groupby('doi').apply(lambda x: ' | '.join(x['Country Name'] + " (" + x['Rank'].astype(str) + ")")).reset_index()
                    countries_combined.columns = ['doi', 'Countries']
                    df_authorships = pd.merge(df_authorships, countries_combined, on='doi', how='left')
                    # df_authorships['Countries'] = df_authorships.groupby('doi')['Country Name'].transform(lambda x: ' | '.join(x))


                    ## CSI CALCULATION
                    country_count = df_result['Country Code 3'].nunique()

                    df_authorships_mean_rank = df_authorships.groupby('doi')['Rank'].mean()
                    csi = round(df_authorships_mean_rank/country_count, 2)

                    df_authorships = df_authorships.merge(csi.rename('Citation Source Index'), on='doi', how='left')
                    average_rank = df_authorships['Rank'].mean()
                    country_count = df_result['Country Code 3'].nunique()
                    citation_source_index = average_rank / country_count
                    df_final = df_authorships[['Citation Source Index', 'doi', 'title', 'Countries', 'all_authors', 'author_count']].drop_duplicates().reset_index(drop=True)
                    df_final = df_final.rename(columns={
                        'doi': 'DOI',
                        'title': 'Title',
                        'all_authors': 'All Authors',
                        'Countries': 'Countries with Ranks',
                        'author_count':'Author count'
                    })

                    no_authors = df_authorships['author_name'].nunique()
                    no_doi_found = df_final['DOI'].nunique()
                    no_country = df_authorships['Country Code 3'].nunique()

                    st.info(f'Results found for {no_doi_found} DOIs out of {no_dois}')
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(
                            label=f'Citation Source Index', 
                            value=f'{round(citation_source_index, 2)}',
                            help='''
                            Citation Source Index (CSI) is a weighted average of the World Bank rankings for Gross National Income (GNI) per capita of the countries where the authors in that citation are from. 
                            ''')
                    with col2:
                        st.metric(label=f'Number of unique authors', value=f'{no_authors}')
                    with col3:
                        st.metric(label=f'Number of unique author countries', value=f'{no_country}')
                    
                    @st.experimental_fragment
                    def gbi_tool():
                        on = st.toggle('Display dashboard for country breakdown')
                        if on:
                            col1, col2 = st.columns([3,2])
                            with col1:
                                st.write('Dashboard')
                                country_counts = df_authorships['Country Name'].value_counts().reset_index()
                                country_counts.columns = ['Country Name', 'Count']
                                fig = px.bar(country_counts, x='Country Name', y='Count', title='Country Counts')
                                col1.plotly_chart(fig, use_container_width = True)
                                country_counts = pd.merge(country_counts, df_result, on='Country Name')
                                country_counts = country_counts.drop(columns=['Unnamed: 0', 'Country Code 3', 'Country Code 2', 'name', 'Year','GNI'])
                                columns = ['Country Name', 'Rank', 'incomeLevel', 'Count']
                                country_counts = country_counts[columns]
                                country_counts = country_counts.sort_values(by='Rank', ascending=True).reset_index(drop=True)
                            with col1:
                                income_level_counts = df_authorships['incomeLevel'].value_counts().reset_index()
                                income_level_counts.columns = ['Income Level', 'Count']
                                fig2 = px.pie(income_level_counts, names='Income Level', values='Count', title='Income Level Counts')
                                col2.plotly_chart(fig2, use_container_width = True)
                            col1, col2 = st.columns([3,1])
                            with col1:
                                fig = px.choropleth(
                                    country_counts,
                                    locations='Country Name',
                                    locationmode='country names',
                                    color='Count',
                                    hover_name='Country Name',
                                    color_continuous_scale='Viridis',
                                    title='Author Affiliations on Map'
                                )
                                fig.update_layout(
                                    width=1200,  # Set the width as per your requirement
                                    height=700   # Set the height as per your requirement
                                )
                                col1.plotly_chart(fig, use_container_width=True)
                            with col2:
                                fig3 = px.box(df_final, y= 'Citation Source Index', title='Box Plot of Citation Source Index')
                                col2.plotly_chart(fig3, use_container_width = True)                   
                    gbi_tool()

                    col1, col2 = st.columns([3,2])
                    with col1:
                        country_counts = df_authorships['Country Name'].value_counts().reset_index()
                        country_counts.columns = ['Country Name', 'Count']
                        country_counts = pd.merge(country_counts, df_result, on='Country Name')
                        country_counts = country_counts.drop(columns=['Unnamed: 0', 'Country Code 3', 'Country Code 2', 'name', 'Year','GNI'])
                        columns = ['Country Name', 'Rank', 'incomeLevel', 'Count']
                        country_counts = country_counts[columns]
                        new_column_names = {
                            'incomeLevel': 'Income Level',
                            'Count': 'Author Count',
                        }
                        country_counts = country_counts.rename(columns=new_column_names)
                        country_counts = country_counts.sort_values(by='Rank', ascending=True).reset_index(drop=True)
                        st.markdown('###### Author country affiliations, country ranks, and income statuses')
                        country_counts
                    with col2:
                        if not np.isnan(citation_source_index):
                            fig3 = px.box(df_final, y= 'Citation Source Index', title='Box Plot of Citation Source Index')
                            col2.plotly_chart(fig3, use_container_width = True)  
                    @st.experimental_fragment
                    def display_table():
                        display = st.checkbox('Display publications')
                        if display:
                            df_final['Hyperlinked DOI']='https://doi.org/'+df_final['DOI']

                            # st.data_editor(
                            #     df_final,
                            #     column_config={
                            #         "DOI": st.column_config.LinkColumn(
                            #             "DOI",
                            #             help="Click to access the DOI link",
                            #             display_text="https://doi.org/(.*?)$",
                            #             disabled=True
                            #         )
                            #     },
                            #     hide_index=True,
                            #     disabled=True
                            # )
                            # column_configuration = {'Hyperlinked':st.column_config.LinkColumn('Hyperlinked', help='Got to publication page')}
                            df_final
                    display_table()
                    source =   df_authorships['source'].value_counts().reset_index()
                    result_text = ", ".join([f"**{row['count']}** country affiliations found on **{row['source']}**" for index, row in source.iterrows()])
                    if not exclude_author_profile_page:
                        st.write(f'''**Note:** {result_text}. 
                    Country affiliations found on author profile page may not be reliable because author profile pages can contain different author information for similar names.
                    ''')

                    status.update(label=f"Calculation complete! Results found for {no_doi_found} DOIs", state="complete", expanded=True)
    else:
        st.warning("Enter DOIs in the text area or upload a file to calculate the Citation Source Index.")
display_custom_license()