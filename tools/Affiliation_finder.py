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
from countryinfo import CountryInfo
import pydeck as pdk
from concurrent.futures import ThreadPoolExecutor, as_completed

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

st.header('Publication affiliation finder')
st.write('''
This tool helps you identify the author-country affiliations of publications. 
Get your DOIs ready and find the affiliations and the Citation Source Index.
''')

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

col1, col2 = st.columns([3,2])
with col1:
    col1, col2 = st.columns(2)
    with col1:
        with st.popover('About this tool', use_container_width=False, icon=":material/info:"):
    
            st.write('''
            Geographic Bias Tool aims to present data on the diversity of countries and country income level of authors. 
            You can submit DOIs of publications to see the authors' country affiliations and country income statuses. 
            The tool aims to identify authors of given DOIs and found their country affiliations. Countries are ranked based on [World Bank GNI per capita, Atlas method](https://data.worldbank.org/indicator/NY.GNP.PCAP.CD). 
            The Citation Source Index is calculated to show the geographic bias of the given publication set.
            '''
            )
            with st.expander('Who developed the Geographic Bias Tool?'):
                st.write('''
                Geographic Bias Tool has been developed by [Imperial College London](https://www.imperial.ac.uk/admin-services/library/learning-support/geo-bias/).
                It was first developed to understand the geographical diversity of publications in Imperial reading lists. 
                Another version of the same tool is available on a Power BI dashboard for Imperial staff and students only.                
                ''')
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
            with st.expander('Reading list about the project'):
                st.caption(f'''
                Harris, Matthew. *Decolonizing Healthcare Innovation: Low-Cost Solutions from Low-Income Countries*. Routledge, 2024, https://www.routledge.com/Decolonizing-Healthcare-Innovation-Low-Cost-Solutions-from-Low-Income-Countries/Harris/p/book/9781032284958.

                Harris, Matthew, Joachim Marti, et al. ‘Explicit Bias Toward High-Income-Country Research: A Randomized, Blinded, Crossover Experiment Of English Clinicians’. *Health Affairs*, vol. 36, no. 11, Nov. 2017, pp. 1997–2004. DOI.org (Crossref), https://doi.org/10.1377/hlthaff.2017.0773.

                Harris, Matthew, James Macinko, et al. ‘Measuring the Bias against Low-Income Country Research: An Implicit Association Test’. *Globalization and Health*, vol. 13, no. 1, Nov. 2017, p. 80. BioMed Central, https://doi.org/10.1186/s12992-017-0304-y.

                Pan, Raj Kumar, et al. ‘World Citation and Collaboration Networks: Uncovering the Role of Geography in Science’. *Scientific Reports*, vol. 2, no. 1, Nov. 2012, p. 902. www.nature.com, https://doi.org/10.1038/srep00902.

                Price, Robyn, et al. ‘A Novel Data Solution to Inform Curriculum Decolonisation: The Case of the Imperial College London Masters of Public Health’. *Scientometrics*, vol. 127, no. 2, Feb. 2022, pp. 1021–37. Springer Link, https://doi.org/10.1007/s11192-021-04231-3.

                Skopec, Mark, et al. ‘Decolonization in a higher education STEMM institution – is “epistemic fragility” a barrier?’ *London Review of Education*, vol. 19, no. 1, June 2021. journals.uclpress.co.uk, https://doi.org/10.14324/LRE.19.1.18.

                ''')
    with col2:
        if st.button(
            "Home", 
            help='Go to Home page',
            icon=":material/home:"
            ):
            st.switch_page("home/Home.py")
st.divider()

st.markdown("""
    <style>
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #E87722;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        color: #555;
    }
    </style>
""", unsafe_allow_html=True)

df_dois = None

radio = st.radio('Select an option', ['Insert DOIs', 'Upload a file with DOIs'])
if radio == 'Insert DOIs':
    st.write('Please insert [DOIs](https://www.doi.org/) (commencing "10.") in separarate rows. Maximum **500 DOIs permitted**!')
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
    st.write('Please upload and submit a .csv file of [DOIs](https://www.doi.org/) (commencing “10.") in separate rows. **Maximum 500 DOIs permitted**!')
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
            submit = st.button('Calculate Citation Source Index', icon=":material/search:")
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
                MAX_WORKERS = 10

                def fetch_authorship_info_and_count(doi, session=None):
                    url = f"https://api.openalex.org/works/doi:{doi}"

                    for attempt in range(4):
                        try:
                            response = (session or requests).get(url, timeout=15)

                            if response.status_code == 200:
                                data = response.json()
                                title = data.get('title', '')
                                authorship_info = data.get('authorships', [])
                                author_count = len(authorship_info)
                                return {
                                    "doi": doi,
                                    "title": title,
                                    "authorship_info": authorship_info,
                                    "author_count": author_count,
                                    "error": None
                                }

                            if response.status_code == 404:
                                return {
                                    "doi": doi,
                                    "title": '',
                                    "authorship_info": [],
                                    "author_count": 0,
                                    "error": "not_found"
                                }

                            if response.status_code == 429:
                                time.sleep(2 * (attempt + 1))
                                continue

                            return {
                                "doi": doi,
                                "title": '',
                                "authorship_info": [],
                                "author_count": 0,
                                "error": f"status_{response.status_code}"
                            }

                        except requests.exceptions.Timeout:
                            if attempt < 3:
                                time.sleep(2 * (attempt + 1))
                                continue
                            return {
                                "doi": doi,
                                "title": '',
                                "authorship_info": [],
                                "author_count": 0,
                                "error": "timeout"
                            }

                        except requests.RequestException as e:
                            if attempt < 3:
                                time.sleep(2 * (attempt + 1))
                                continue
                            return {
                                "doi": doi,
                                "title": '',
                                "authorship_info": [],
                                "author_count": 0,
                                "error": str(e)
                            }

                    return {
                        "doi": doi,
                        "title": '',
                        "authorship_info": [],
                        "author_count": 0,
                        "error": "unknown_error"
                    }

                # Fetch authorship information for each DOI and store it in a new DataFrame
                authorship_data = []
                failed_dois = []

                unique_dois = df_dois['doi'].dropna().unique().tolist()

                def fetch_batch(doi_batch, session=None):
                    filter_str = "|".join(doi_batch)
                    url = f"https://api.openalex.org/works?filter=doi:{filter_str}&per-page=50"
                    for attempt in range(4):
                        try:
                            response = (session or requests).get(url, timeout=15)
                            if response.status_code == 200:
                                return response.json().get('results', [])
                            if response.status_code == 429:
                                time.sleep(2 * (attempt + 1))
                                continue
                            return []
                        except requests.exceptions.Timeout:
                            if attempt < 3:
                                time.sleep(2 * (attempt + 1))
                            continue
                        except requests.RequestException:
                            return []
                    return []

                def chunks(lst, n):
                    for i in range(0, len(lst), n):
                        yield lst[i:i + n]

                BATCH_SIZE = 50

                with requests.Session() as session:
                    session.headers.update({"User-Agent": "mailto:your@email.ac.uk"})
                    batches = list(chunks(unique_dois, BATCH_SIZE))
                    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                        futures = {
                            executor.submit(fetch_batch, batch, session): batch
                            for batch in batches
                        }
                        progress_bar = st.progress(0, text="Fetching DOIs...")
                        completed = 0
                        total = len(batches)

                        for future in as_completed(futures):
                            batch = futures[future]
                            results = future.result()
                            found_dois = {r.get('doi', '').replace('https://doi.org/', '') for r in results}
                            for doi in batch:
                                if doi not in found_dois:
                                    failed_dois.append({"doi": doi, "error": "not_found_in_batch"})
                            for data in results:
                                doi = data.get('doi', '').replace('https://doi.org/', '')
                                title = data.get('title', '')
                                authorship_info = data.get('authorships', [])
                                author_count = len(authorship_info)
                                for author in authorship_info:
                                    country_codes = author.get('countries', [])
                                    source = 'article page'
                                    if not country_codes:
                                        country_codes = ['']
                                        source = 'author profile page'
                                    for country_code in country_codes:
                                        authorship_data.append({
                                            'doi': doi,
                                            'title': title,
                                            'author_position': author.get('author_position', ''),
                                            'author_name': author.get('author', {}).get('display_name', ''),
                                            'author_id': author.get('author', {}).get('id', ''),
                                            'Country Code 2': country_code,
                                            'source': source,
                                            'author_count': author_count
                                        })
                            # ✅ Increment and update ONCE per batch, after all its data is processed
                            completed += 1
                            progress_bar.progress(completed / total, text=f"Processed batch {completed} of {total}...")

                        progress_bar.empty()
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




                    def fetch_author_details(author_id, session=None):
                        try:
                            response = (session or requests).get(author_id, timeout=15)
                            if response.status_code == 200:
                                return response.json()
                            return None
                        except requests.RequestException:
                            return None

                    if not exclude_author_profile_page:
                        missing_mask = df_authorships['Country Code 2'].isna() & df_authorships['author_id'].notna()
                        unique_author_ids = df_authorships.loc[missing_mask, 'author_id'].dropna().unique().tolist()

                        author_country_map = {}

                        with requests.Session() as session:
                            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                                futures = {
                                    executor.submit(fetch_author_details, author_id, session): author_id
                                    for author_id in unique_author_ids
                                }

                                for future in as_completed(futures):
                                    author_id = futures[future]
                                    author_details = future.result()

                                    country_code = None
                                    if author_details:
                                        affiliations = author_details.get('affiliations', [])
                                        if affiliations:
                                            country_code = affiliations[0].get('institution', {}).get('country_code')

                                    author_country_map[author_id] = country_code

                        df_authorships.loc[missing_mask, 'Country Code 2'] = (
                            df_authorships.loc[missing_mask, 'author_id'].map(author_country_map)
                        )

                        df_authorships.loc[
                            missing_mask & df_authorships['Country Code 2'].notna(),
                            'source'
                        ] = 'author profile page'

                        # Update country codes for rows where country_code is missing
                        def fetch_author_details(author_id, session=None):
                            for attempt in range(4):
                                try:
                                    response = (session or requests).get(author_id, timeout=15)

                                    if response.status_code == 200:
                                        return response.json()

                                    if response.status_code == 404:
                                        return None

                                    if response.status_code == 429:
                                        time.sleep(2 * (attempt + 1))
                                        continue

                                    return None

                                except requests.exceptions.Timeout:
                                    if attempt < 3:
                                        time.sleep(2 * (attempt + 1))
                                        continue
                                    return None

                                except requests.RequestException:
                                    if attempt < 3:
                                        time.sleep(2 * (attempt + 1))
                                        continue
                                    return None

                            return None
                                            
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


                    df_authorships['Country Name'] = df_authorships['Country Name'].fillna('No country info')
                    df_authorships['Rank'] = pd.to_numeric(df_authorships['Rank'], errors='coerce')
                    df_authorships['Rank Label'] = df_authorships['Rank'].apply(
                        lambda v: str(int(v)) if pd.notna(v) else 'N/A'
                    )
                    df_authorships['all_authors'] = df_authorships.groupby('doi')['author_name'].transform(lambda x: ' | '.join(x))
                    countries_combined = (
                        df_authorships.groupby('doi')
                        .apply(lambda x: ' | '.join(
                            x['Country Name'].astype(str) + " (" + x['Rank Label'] + ")"
                        ))
                        .reset_index(name='Countries')
                    )

                    df_authorships = pd.merge(df_authorships, countries_combined, on='doi', how='left')


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

                    csv = df_final.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download results as CSV",
                        data=csv,
                        file_name='affiliation_results.csv',
                        mime='text/csv',
                        icon=":material/download:"
                    )

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
                        st.markdown(
                            '##### Author country affiliations, country ranks, and income statuses',
                            help='Countries are ranked in reverse order, with wealthier countries having lower ranks. For instance, the UK is ranked 180. This inverse ranking is intentional for calculating the CSI.'
                        )
                        country_counts
                    with col2:
                        if not np.isnan(citation_source_index):
                            fig3 = px.box(df_final, y= 'Citation Source Index', title='Box Plot of Citation Source Index')
                            col2.plotly_chart(fig3, use_container_width = True) 

                    @st.experimental_fragment
                    def gbi_tool():
                        col1, col2 = st.columns([3,2])
                        with col1:
                            country_counts = df_authorships['Country Name'].value_counts().reset_index()
                            country_counts.columns = ['Country Name', 'Count']
                            fig = px.bar(
                                country_counts,
                                x='Country Name',
                                y='Count',
                                title='Author Countries',
                                color='Count',
                                color_continuous_scale='Oranges',
                                template='plotly_white'
                            )
                            fig.update_layout(
                                xaxis_title='',
                                yaxis_title='Number of Authors',
                                coloraxis_showscale=False,
                                title_font_size=16
                            )
                            fig.update_xaxes(tickangle=-45)
                            col1.plotly_chart(fig, use_container_width = True)
                            country_counts = pd.merge(country_counts, df_result, on='Country Name')
                            country_counts = country_counts.drop(columns=['Unnamed: 0', 'Country Code 3', 'Country Code 2', 'name', 'Year','GNI'])
                            columns = ['Country Name', 'Rank', 'incomeLevel', 'Count']
                            country_counts = country_counts[columns]
                            country_counts = country_counts.sort_values(by='Rank', ascending=True).reset_index(drop=True)
                        with col1:
                            income_level_counts = df_authorships['incomeLevel'].value_counts().reset_index()
                            income_level_counts.columns = ['Income Level', 'Count']
                            fig2 = px.pie(
                                income_level_counts,
                                names='Income Level',
                                values='Count',
                                title='Author Income Levels',
                                hole=0.4,
                                color_discrete_sequence=[
                                    '#2E86AB',  # blue - High income
                                    '#E84855',  # red - Upper middle income
                                    '#F4A261',  # orange - Lower middle income
                                    '#2A9D8F',  # teal - Low income
                                    '#AAAAAA',  # grey - No country info
                                ],
                                template='plotly_white'
                            )
                            fig2.update_traces(textposition='outside', textinfo='percent+label')
                            fig2.update_layout(showlegend=False)
                            col2.plotly_chart(fig2, use_container_width = True)

                        st.subheader('Author country affiliations', anchor=False)
                        col1, col2 = st.columns([5,2])
                        with col1:
                            # Function to get coordinates
                            def get_coordinates(country_name):
                                try:
                                    country = CountryInfo(country_name)
                                    return country.info().get('latlng', (None, None))
                                except KeyError:
                                    return None, None

                            # Apply the function to each country to get latitude and longitude
                            country_counts[['Latitude', 'Longitude']] = country_counts['Country Name'].apply(lambda x: pd.Series(get_coordinates(x)))

                            # Set a scaling factor and minimum radius to make circles larger
                            scaling_factor = 5000  # Adjust this to control the overall size of the circles
                            minimum_radius = 100000  # Minimum radius for visibility of all points

                            # Calculate the circle size based on `Count`
                            country_counts['size'] = country_counts['Count'] * scaling_factor + minimum_radius

                            # Filter out rows where coordinates were not found
                            country_counts = country_counts.dropna(subset=['Latitude', 'Longitude'])

                            # ScatterplotLayer to show countries and their mentions count
                            scatterplot_layer = pdk.Layer(
                                "ScatterplotLayer",
                                data=country_counts,
                                get_position=["Longitude", "Latitude"],
                                get_radius="size",
                                get_fill_color="[255, 140, 0, 160]",  # Adjusted color with opacity
                                pickable=True,
                                auto_highlight=True,
                                id="country-mentions-layer",
                            )

                            # Define the view state of the map
                            view_state = pdk.ViewState(
                                latitude=20, longitude=0, zoom=1, pitch=30
                            )

                            # Create the Deck with the layer, view state, and map style
                            chart = pdk.Deck(
                                layers=[scatterplot_layer],
                                initial_view_state=view_state,
                                tooltip={"text": "{Country Name}\n# Authors: {Count}"},
                                map_style="mapbox://styles/mapbox/light-v9"  # Use a light map style
                            )
                            st.pydeck_chart(chart, use_container_width=False)
                        with col2:
                            country_counts = df_authorships['Country Name'].value_counts().reset_index()
                            country_counts.columns = ['Country Name', 'Count']
                            country_counts = pd.merge(country_counts, df_result, on='Country Name')
                            country_counts = country_counts.drop(columns=['Unnamed: 0', 'Country Code 3', 'Country Code 2', 'name', 'Year','GNI'])
                            columns = ['Country Name', 'incomeLevel', 'Count']
                            country_counts = country_counts[columns]
                            new_column_names = {
                                'incomeLevel': 'Income Level',
                                'Count': 'Author Count',
                            }
                            country_counts = country_counts.rename(columns=new_column_names)
                            country_counts = country_counts.sort_values(by='Author Count', ascending=False).reset_index(drop=True)
                            st.dataframe(country_counts, hide_index=True, use_container_width=True, height=500)
                    gbi_tool()
 
                    @st.experimental_fragment
                    def display_table():
                        display = st.checkbox('Display publications')
                        if display:
                            df_final['Hyperlinked DOI'] = 'https://doi.org/' + df_final['DOI']
                            st.data_editor(
                                df_final,
                                column_config={
                                    "Hyperlinked DOI": st.column_config.LinkColumn(
                                        "Hyperlinked DOI",
                                        help="Click to open the publication",
                                        display_text="Open article ↗",
                                        disabled=True
                                    )
                                },
                                hide_index=True,
                                disabled=True
                            )
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

st.divider()

display_custom_license()