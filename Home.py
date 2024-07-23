import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET
import streamlit.components.v1 as components
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(layout = "wide", 
                    page_title='Geographic Bias Tool',
                    page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTtoX76TyVQs-o1vEvNuAnYX0zahtSui173gg&s",
                    initial_sidebar_state="auto") 
pd.set_option('display.max_colwidth', None)

with st.sidebar:
    st.image('https://upload.wikimedia.org/wikipedia/commons/0/06/Imperial_College_London_new_logo.png', width=150)
    st.subheader("Geographic Bias Tool",anchor=False)  
    with st.expander('About'):  
        st.write('Note here')
        components.html(
"""
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/80x15.png" /></a><br />This tool is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
"""
)
st.markdown(
    """
    <a href="https://www.imperial.ac.uk">
        <img src="https://upload.wikimedia.org/wikipedia/commons/0/06/Imperial_College_London_new_logo.png" width="300">
    </a>
    """,
    unsafe_allow_html=True
)
st.title('Geographic Bias Tool', anchor=False)

with st.popover('About this tool'):
    st.subheader('What is Geographic Bias Tool?')
    st.write('''
    Geographic Bias Tool aims to present data on the diversity of countries and country income level of authors.
    You can submit DOIs of publications to see the authors' country affiliations and country income statuses.
    '''
    )

    st.subheader('Who developed?')
    st.write('''
    Geographic Bias Tool has been developed by [Imperial College London](https://www.imperial.ac.uk/admin-services/library/learning-support/geo-bias/).
    '''
    )

    st.subheader('What is Citation Source Index (CSI)?')
    st.write('''
    Citation Source Index (CSI) is a weighted average of the World Bank rankings for Gross National Income (GNI) per capita of the countries where the authors in that citation are from. 

    The CSI ranges from 0 to 1, so a CSI closer to 1 means the overall development index of the countries represented by the authors that published the article is high or vice versa. 
    If the authors on an article were all from Afghanistan then the CSI would be 0.01. 
    If the authors on an article were all from the UK then the CSI would be 0.88. 
    The CSI for the reading list as a whole is the average of all the CSI scores for the readings provided on that list and that are available for analysis through this platform.

    For more information, the following article: https://link.springer.com/article/10.1007/s11192-021-04231-3
    '''
    )

dois = st.text_area(
    'Type or paste in one DOI per line in this box, then press Ctrl+Enter.', 
    help='DOIs will be without a hyperlink such as 10.1136/bmjgh-2023-013696',
    placeholder=''' e.g.
    10.1136/bmjgh-2023-013696
    10.1097/jac.0b013e31822cbdfd
    '''
    )
if dois:
    # Split the input text into individual DOIs based on newline character
    doi_list = dois.split('\n')
    
    # Remove any empty strings that may result from extra newlines
    doi_list = [doi.strip() for doi in doi_list if doi.strip()]
    
    # Create a DataFrame
    df_dois = pd.DataFrame(doi_list, columns=["doi"])
    df_dois['doi'] = df_dois['doi'].str.replace('https://doi.org/', '')
    df_dois = df_dois.drop_duplicates().reset_index(drop=True)
    no_dois = len(df_dois)
    st.info(f'You entered {no_dois} unique DOIs')
    with st.expander(f'See the DOIs you entered'):
        df_dois

    submit = st.button('Calculate Citation Source Index')

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
                        source = 'found through author page'
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

            # Remove duplicate rows
            df_authorships = df_authorships.drop_duplicates()
            openalex_found_dois = len(df_authorships)
            if openalex_found_dois == 0:
                st.warning('''
                No DOIs found! 

                Check your DOIs and submit them again. 

                If you are sure that the DOIs are correct, they may not be available in the [OpenAlex](https://openalex.org/) database.
                ''')
                status.update(label=f"Calculation complete without any results!", state="complete", expanded=True)
            else:
                # Add 'api.' between 'https://' and 'openalex' in the 'author_id' column
                df_authorships['author_id'] = df_authorships['author_id'].apply(lambda x: x.replace('https://', 'https://api.') if x else x)

                # Function to update country_code if missing and mark the source
                def update_country_code(row):
                    if not row['Country Code 2'] and row['author_id']:
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



                ## WORLD BANK API
                # Add 'api.' between 'https://' and 'openalex' in the 'author_id' column
                df_authorships['author_id'] = df_authorships['author_id'].apply(lambda x: x.replace('https://', 'https://api.') if x else x)

                # Function to update country_code if missing and mark the source
                def update_country_code(row):
                    if not row['Country Code 2'] and row['author_id']:
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
                df_final = df_authorships[['Citation Source Index', 'doi', 'title', 'all_authors', 'Countries', 'author_count']].drop_duplicates().reset_index(drop=True)
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
                        with col1:
                            income_level_counts = df_authorships['incomeLevel'].value_counts().reset_index()
                            income_level_counts.columns = ['Income Level', 'Count']
                            fig2 = px.pie(income_level_counts, names='Income Level', values='Count', title='Income Level Counts')
                            col2.plotly_chart(fig2, use_container_width = True)
                
                gbi_tool()
                df_final    
                status.update(label=f"Calculation complete! Results found for {no_doi_found} DOIs", state="complete", expanded=True)
else:
    st.warning("Enter DOIs in the text area to calculate the Citation Source Index.")

